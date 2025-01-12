import pygame
import random

# Initialize pygame
pygame.init()

# Initialize mixer for music
pygame.mixer.init()

# load the music
pygame.mixer.music.load("music/retro-game-music-245230.mp3")
# set the volume to 20%
pygame.mixer.music.set_volume(0.1)
pygame.mixer.music.play(-1)  # to looping the music

# Initialize colors that will be used
white = (255, 255, 255)
yellow = (255, 255, 102)
black = (0, 0, 0)
red = (213, 50, 80)
green = (0, 255, 0)
blue = (50, 153, 213)

# Set screen size
dis_width = 600
dis_height = 400

# Create screen with the specified size
dis = pygame.display.set_mode((dis_width, dis_height))

# Set title for the screen
pygame.display.set_caption("Snake Game")

# Create clock object
clock = pygame.time.Clock()

# Set snake block size and snake speed
snake_block = 10
snake_speed = 5

# Set font style to be used
font_style = pygame.font.SysFont("bahnschrift", 25)
score_font = pygame.font.SysFont("comicsansms", 25)


# Define function to display score
def your_score(score):
    value = score_font.render("Your Score: " + str(score), True, yellow)
    dis.blit(value, [0, 0])


# Define function to draw snake
def our_snake(snake_block, snake_list):
    for x in snake_list:
        pygame.draw.rect(dis, black, [x[0], x[1], snake_block, snake_block])


# Define function to display message
def message(msg, color):
    mesg = font_style.render(msg, True, color)
    dis.blit(mesg, [dis_width / 6, dis_height / 3])


# Main game function
def gameLoop():
    # Check if the game is over or not
    game_over = False
    game_close = False

    # x1 and y1 are the initial coordinates of the snake's head
    x1 = dis_width / 2
    y1 = dis_height / 2

    # Variables used to change the position of the snake's head
    x1_change = 0
    y1_change = 0

    # Empty list that will be used to store the coordinates of the snake's body
    snake_List = []

    # Initial length of the snake
    Length_of_snake = 1

    # Coordinates of the food that the snake must eat to grow
    foodx = round(random.randrange(0, dis_width - snake_block) / 10.0) * 10.0
    foody = round(random.randrange(0, dis_height - snake_block) / 10.0) * 10.0

    # Loop to keep the game running
    while not game_over:
        # Loop for game close
        while game_close == True:
            # Fill the screen with blue color
            dis.fill(blue)
            # Display message for losing the game
            message("You Lost! Press C-Play Again or Q-Quit", red)
            # Display score
            your_score(Length_of_snake - 1)
            # Update display
            pygame.display.update()

            # Check events
            for event in pygame.event.get():
                # If user presses Q, the game ends
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_q:
                        game_over = True
                        game_close = False
                    # If user presses C, the game restarts
                    if event.key == pygame.K_c:
                        gameLoop()

        # Check events with loop
        for event in pygame.event.get():
            # If user closes the window, the game ends
            if event.type == pygame.QUIT:
                game_over = True
            # If user presses a key on the keyboard, the snake moves in the specified direction
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_LEFT:
                    x1_change = -snake_block
                    y1_change = 0
                elif event.key == pygame.K_RIGHT:
                    x1_change = snake_block
                    y1_change = 0
                elif event.key == pygame.K_UP:
                    y1_change = -snake_block
                    x1_change = 0
                elif event.key == pygame.K_DOWN:
                    y1_change = snake_block
                    x1_change = 0

        # Check if the snake hits the wall
        if x1 >= dis_width or x1 < 0 or y1 >= dis_height or y1 < 0:
            game_close = True
        # Move the snake
        x1 += x1_change
        y1 += y1_change
        # Fill the screen with blue color
        dis.fill(blue)
        # Draw food
        pygame.draw.rect(dis, green, [foodx, foody, snake_block, snake_block])
        # Add snake's head to the snake list
        snake_Head = []
        snake_Head.append(x1)
        snake_Head.append(y1)
        snake_List.append(snake_Head)
        # If the length of the snake is greater than the specified length, remove the snake's tail
        if len(snake_List) > Length_of_snake:
            del snake_List[0]

        # Check if the snake hits itself
        for x in snake_List[:-1]:
            if x == snake_Head:
                game_close = True
        # Draw the snake
        our_snake(snake_block, snake_List)
        your_score(Length_of_snake - 1)
        # Update display
        pygame.display.update()

        # If the snake eats the food, generate new food and add length to the snake
        if x1 == foodx and y1 == foody:
            foodx = round(random.randrange(0, dis_width - snake_block) / 10.0) * 10.0
            foody = round(random.randrange(0, dis_height - snake_block) / 10.0) * 10.0
            Length_of_snake += 1

        # Set game speed
        clock.tick(snake_speed)

    pygame.quit()
    quit()


gameLoop()
