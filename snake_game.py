import os
import pygame
import random
import math
import time  # For delaying before closing the game

pygame.init()

try:
    pygame.mixer.init()
    EAT_SOUND = pygame.mixer.Sound("game-point.mp3")
    PLAY_SOUND = pygame.mixer.Sound("game-start.mp3")
    INTRO_SOUND = pygame.mixer.Sound("game-intro.mp3")
    EAT_SOUND.set_volume(0.5)
except Exception as e:
    print("Warning: sound disabled:", e)
    EAT_SOUND = None
# Add this near the top of the file with other imports

# Constants for the game window
WIDTH, HEIGHT = 500, 500  # Updated window size
WINDOW_SIZE = (WIDTH, HEIGHT)
WINDOW_TITLE = "Hungry Snake Game"

# Modify the image path constant to be more specific
INTRO_BG = pygame.image.load(os.path.join("image-snake-game.png"))
INTRO_BG = pygame.transform.scale(
    INTRO_BG, (WIDTH, HEIGHT))  # Scale image to fit window

# Colors
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
BLUE = (52, 107, 235)
RED = (230, 56, 44)

# Create the game window
window = pygame.display.set_mode(WINDOW_SIZE)
pygame.display.set_caption(WINDOW_TITLE)


# Snake class to manage the snake's movement and growth
class Snake:
    def __init__(self, speed):
        self.body = [
            (WIDTH // 2 - i * 20, HEIGHT // 2) for i in range(4)
        ]  # Initial size is 4 segments
        self.direction = (1, 0)  # Start moving towards the right
        self.speed = speed

    def move(self):
        dx, dy = self.direction
        new_head = (
            (self.body[0][0] + dx * 20) % WIDTH,
            (self.body[0][1] + dy * 20) % HEIGHT,
        )
        self.body.pop()  # Remove the tail segment
        self.body.insert(0, new_head)  # Insert the new head

    def grow(self):
        dx, dy = self.direction
        new_tail = (
            (self.body[-1][0] - dx * 20) % WIDTH,
            (self.body[-1][1] - dy * 20) % HEIGHT,
        )
        self.body.append(new_tail)

    def change_direction(self, dx, dy):
        # Avoid reversing direction (e.g., from right to left) to prevent self-collision
        if (dx, dy) != (-self.direction[0], -self.direction[1]):
            self.direction = (dx, dy)

    def get_head(self):
        return self.body[0]

    def get_body(self):
        return self.body[1:]

    def set_speed(self, speed):
        self.speed = speed


# Food class to manage the position and respawn of food
class Food:
    def __init__(self):
        self.position = (
            random.randint(10, WIDTH - 10),
            random.randint(10, HEIGHT - 10),
        )

    def respawn(self):
        self.position = (
            random.randint(10, WIDTH - 10),
            random.randint(10, HEIGHT - 10),
        )

    def get_position(self):
        return self.position


# Function to calculate the distance between two points
def distance(point1, point2):
    return math.sqrt((point1[0] - point2[0]) ** 2 + (point1[1] - point2[1]) ** 2)


def show_intro_screen():
    font_large = pygame.font.Font(None, 50)
    font_small = pygame.font.Font(None, 30)

    title_text = font_large.render("Hungry Snake Game", True, BLACK)
    author_text = font_large.render("by Mr. Halip", True, BLACK)

    button_w, button_h = 150, 40
    cx = WIDTH // 2 - button_w // 2
    buttons = {
        "slow": pygame.Rect(cx, HEIGHT // 2 - 40, button_w, button_h),
        "normal": pygame.Rect(cx, HEIGHT // 2 + 10, button_w, button_h),
        "fast": pygame.Rect(cx, HEIGHT // 2 + 60, button_w, button_h),
    }

    clock = pygame.time.Clock()

    # Intro sound
    if INTRO_SOUND:
        INTRO_SOUND.play()

    while True:
        mouse_pos = pygame.mouse.get_pos()
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                return
            if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
                for name, rect in buttons.items():
                    if rect.collidepoint(event.pos):
                        if PLAY_SOUND:
                            PLAY_SOUND.play()
                            INTRO_SOUND.stop()
                        return name

        # Draw background image instead of filling with color
        window.blit(INTRO_BG, (0, 0))

        # Add semi-transparent overlay to make text more readable
        overlay = pygame.Surface((WIDTH, HEIGHT))
        overlay.fill((255, 255, 255))
        overlay.set_alpha(100)  # 128 is semi-transparent
        window.blit(overlay, (0, 0))

        # title text position "Hungry Snake Game"
        window.blit(
            title_text,
            (
                WIDTH // 2 - title_text.get_width() // 2,
                HEIGHT // 5 - title_text.get_height() // 2,
            ),
        )

        # author text position "by Mr. Halip"
        window.blit(
            author_text,
            (
                WIDTH // 2 - author_text.get_width() // 2,
                HEIGHT // 3 - author_text.get_height(),
            ),
        )

        for name, rect in buttons.items():
            if rect.collidepoint(mouse_pos):
                fill = (200, 200, 200)
            else:
                fill = (230, 230, 230)
            pygame.draw.rect(window, fill, rect)
            pygame.draw.rect(window, BLACK, rect, 2)
            label = font_small.render(name.upper(), True, BLACK)
            window.blit(
                label,
                (rect.x + rect.width // 2 - label.get_width() // 2,
                 rect.y + rect.height // 2 - label.get_height() // 2),
            )

        pygame.display.update()
        clock.tick(60)


# Main game loop
def main():
    speed_level = show_intro_screen()

    if speed_level == "slow":
        snake_speed = 5
    elif speed_level == "normal":
        snake_speed = 10
    else:
        snake_speed = 20

    snake = Snake(snake_speed)
    food = Food()

    clock = pygame.time.Clock()

    score = 0  # Initialize the score to zero

    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                return

            # Handle user input to change the snake's direction
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_UP:
                    snake.change_direction(0, -1)
                elif event.key == pygame.K_DOWN:
                    snake.change_direction(0, 1)
                elif event.key == pygame.K_LEFT:
                    snake.change_direction(-1, 0)
                elif event.key == pygame.K_RIGHT:
                    snake.change_direction(1, 0)

        # Move the snake
        snake.move()

        # Check for collisions with food
        head = snake.get_head()
        if distance(head, food.get_position()) < 20:
            food.respawn()
            snake.grow()
            score += 1  # Increase the score by one when the snake eats the food
            if EAT_SOUND:
                EAT_SOUND.play()

        # Check for self-collision
        if head in snake.get_body():
            # Draw "Game Over" on the screen for 2 seconds
            font = pygame.font.Font(None, 36)
            text = font.render("Game Over", True, RED)
            window.blit(text, (WIDTH // 2 - 70, HEIGHT // 2))
            pygame.display.update()
            time.sleep(2)  # Wait for 2 seconds
            pygame.quit()
            return

        # Clear the window with a white background
        window.fill(WHITE)

        # Draw the snake's body as black rectangles
        for segment in snake.body:
            pygame.draw.rect(window, BLACK, (segment[0], segment[1], 20, 20))

        # Draw the snake's head as a black rectangle
        pygame.draw.rect(window, BLACK, (head[0] + 10, head[1] + 10, 10, 10))

        # Draw the food as a black circle
        pygame.draw.circle(
            window,
            RED,
            (food.get_position()[0] + 10, food.get_position()[1] + 10),
            10,
        )

        # Draw the score on the top left side
        font = pygame.font.Font(None, 30)
        score_text = font.render(f"Score: {score}", True, BLACK)
        window.blit(score_text, (10, 10))

        # Update the display
        pygame.display.update()

        # Set the frame rate
        # Adjust the game speed according to the snake's speed
        clock.tick(snake.speed)


if __name__ == "__main__":
    main()
