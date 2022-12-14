import pygame
import time
import random

#game speed
game_speed = 20

#game window size 
window_x = 720
window_y = 480

#colors in RGB format
black = pygame.Color(0,0,0)
white = pygame.Color(255,255,255)
red = pygame.Color(255,0,0)
green = pygame.Color(0,255,0)
blue = pygame.Color(0,0,255)

#initialising pygame so that it creates a window using previous
# variables window_x, window_y

#initialising actual pygame
pygame.init()

#initialising game window with title (set_caption)
pygame.display.set_caption('Self-learning Snake')
# setting display size (window size, window_x, window_y)
game_window = pygame.display.set_mode((window_x, window_y))

#FPS controller 
fps = pygame.time.Clock()

# initial snake position and size 
snake_position = [100, 50]

# giving the snake 2 blocks for body
snake_body = [
    [100,50],
    [90,50]
]

#apple position
# apple position is randomly generated 
# // is division which then rounds the result down
# suppose that one 'block' is 10 pixels wide and tall, then to get the number of length of blocks that
# our window is, we have to divide the window_x by 10 and get the integer. We wont deal with fractional 
# blocks. 
# We then get a random number of blocks between 1 and the window size and then figure out the actual pixel distance
# after to get the actual coordinates 

apple_position = [
    random.randrange(1, (window_x//10)) * 10,
    random.randrange(1, (window_y//10)) * 10
]

# at some point we may stop spawning apples or we may want apples to only spawn sometimes
apple_spawn = True 

# default snake direction which will be towards the right side
default_direction = 'RIGHT'

# what we will use to compare the current direction 
# user will press a key which will be the current direction
current_direction = default_direction

# initialising score
score = 0

# display scoring on screen and styling it
def display_score(color, font, size):
    # font styling
    score_font = pygame.font.SysFont(font, size)

    # create display surface and render
    # render creates new surface with specified text on it
    # pygame.font doesnt let you draw text directly on existing surface which is why we need
    # to create new surface then apply text (text can only be single line)
    score_surface = score_font.render('Score: ' + str(score), True, color)

    # creating and getting the rectangular area of the surface 
    score_area = score_surface.get_rect()

    # now display text
    # blit draws one image onto another (one surface onto another)
    # blit(source, destination, area, special flags)
    # blit is the actual drawing process
    game_window.blit(score_surface, score_area)

    # just to recap, we've styled the font to what we want
    # we've created a small surface containing the score which will be rendered
    # we've defined the area
    # we've then drawn the surface (score surface) onto the window (game_window) by giving it the coordinates (score area)

# how to lose in snake (game over)
def game_over():
    # the font we want to use and its size
    text_style = pygame.font.SysFont('arial', 40)

    # creating display surface and rendering
    game_over_surface = text_style.render('You scored: ' + str(score), True, red)

    # creating and getting the area
    game_over_area = game_over_surface.get_rect()

    # where to place the position of the text
    game_over_area.center = (window_x/2, window_y/2)

    # using blit to actually draw the text
    game_window.blit(game_over_surface, game_over_area)
    # now display by updating the entire screen
    pygame.display.flip()

    # setting a delay before we quit everything
    time.sleep(3)

    # deactivate the library
    pygame.quit()
    # if this fails then we should quit display before quitting library by doing
    # pygame.display.quit() before pygame.quit()

    # now actually quit the entire program
    quit()

# time to create actual game controls
# main function which is always active
# we're listening to keyboard events permanently here
while True: 
    # handling key events
    for event in pygame.event.get():
        # if they've pressed a key 
        if event.type == pygame.KEYDOWN:
            # depending on the key
            # use python 3.10 matching instead of a list of if statements
            # use if statements if you are using python 3.8 or older
            # we're using the typical arrow keys as well as awsd which is used commonly for gaming
            if event.key == pygame.K_UP or event.key == pygame.K_w:
                current_direction = 'UP'
            if event.key == pygame.K_DOWN or event.key == pygame.K_s:
                current_direction = 'DOWN'
            if event.key == pygame.K_LEFT or event.key == pygame.K_a:
                current_direction = 'LEFT'
            if event.key == pygame.K_RIGHT or event.key == pygame.K_d:
                current_direction = 'RIGHT'

    # now we have to handle simultaneous button presses 
    # we want to move in the direction that was pressed first, not both at the same time
    if current_direction == 'UP' and default_direction != 'DOWN':
        default_direction = 'UP'
        # this if you are pressing up and any key other than down, change to up
        # basically priority of key presses
    if current_direction == 'DOWN' and default_direction != 'UP':
        default_direction = 'DOWN'
    if current_direction == 'LEFT' and default_direction != 'RIGHT':
        default_direction = 'LEFT'
    if current_direction == 'RIGHT' and default_direction != 'LEFT':
        default_direction = 'RIGHT'

    # handling movement :)
    if default_direction == 'UP':
        # snake position is (x, y) so moving up is changing y value by -10
        # 10 because thats what we previously defined as 1 block, or 10 pixels
        snake_position[1] -= 10
    if default_direction == 'DOWN':
        snake_position[1] += 10
    if default_direction == 'LEFT':
        # changing the x value of the body
        snake_position[0] -= 10
    if default_direction == 'RIGHT':
        snake_position[0] += 10
    
    # increasing length of snake and score by 10 per apple

    # we've previously changed the snake head position on key press
    # now we have to add that to the body
    # for example, we could go from body coordinates of (100, 50), (90,50)
    # to new position of (100, 40) , (100, 50), (90, 50)
    # ie, we update the body 
    # then later we will remove the tail of snake to get final update
    # (100, 40), (100, 50)
    snake_body.insert(0, list(snake_position))

    # if snake head position same as apple position,
    # ie, x and y coordinates are the same then add score +1
    # reset apple coordinates 
    if snake_position[0] == apple_position[0] and snake_position[1] == apple_position[1]:
        # if snake eats the body then make new snake head permanent, ie body grows because we dont
        # remove the tail of the snake
        score += 1
        apple_spawn = False
    else:
        # if snake isnt eating the apple then on the next move, remove the tail so that body size
        # stays the same 
        snake_body.pop()

    # if spawn is off, generate new apple
    if not apple_spawn:
        apple_position = [
            random.randrange(1, (window_x//10)) * 10,
            random.randrange(1, (window_y//10)) * 10
        ]
    
    # set apple spawn to true again because we just generated a new one
    apple_spawn = True

    # update background every frame
    # we'll have to rerender screen and we'll set background to black
    game_window.fill(black)

    # drawing the snake :)
    for position in snake_body:
        pygame.draw.rect(
            # the surface we draw on
            game_window,

            # the color of the snake body
            green,

            # Rect (left, top, width, height)
            # x and y axis, block height and width
            # drawing the actual blocks on the screen based off of the coordinates of snake body
            pygame.Rect(position[0], position[1], 10, 10),
        )

    # drawing the fruit
    pygame.draw.rect(
        # surface
        game_window,

        # color
        red,

        # again Rect(left, top, width, height)
        pygame.Rect(apple_position[0], apple_position[1], 10, 10)
    )

    # losing conditions which includes touching the outside of the window
    # or the snake head eating its own body

    # touching window border (we only care about snake head position)
    # if snake head touches the left border or right border
    if snake_position[0] < 0 or snake_position[0] > window_x-10:
        game_over()
    # if snake head touches top border or bottom border respectively
    if snake_position[1] < 0 or snake_position[1] > window_y-10:
        game_over()
    
    # snake head eating its own body
    # get all coordinates/blocks of body and exclude the snake head
    for block in snake_body[1:]:
        # if snake head position eating one of its body
        # we compare x coordinates and y coordinates
        if snake_position[0] == block[0] and snake_position[1] == block[1]:
            game_over()

    # continously updating the scoreboard
    display_score(white, 'Arial', 20)

    # refresh entire screen with all its updates
    pygame.display.update()

    # set refresh rate
    fps.tick(game_speed)










