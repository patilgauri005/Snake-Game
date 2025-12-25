##step 01 : Import Libraries
import pygame
import random
import sys

#step 02 : initialize pygame and setup display
pygame.init()
HEIGHT = 400
WIDTH = 600
CELL_SIZE = 20

screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Snake Game🐍")

#Step 03 : Colors and Clock
WHITE = (255, 255, 255)
SNAKE_COLOR = (102, 255, 178)    # bright teal
FOOD_COLOR = (255, 102, 102)     # bright red
BG_COLOR = (30, 30, 40)          # dark bluish background
GRID_COLOR = (50, 50, 60)        # subtle grid color

clock = pygame.time.Clock()

# Fonts
font = pygame.font.SysFont('Arial', 24)
game_over_font = pygame.font.SysFont('Arial', 36)

#Step 04 : Define Snake and food
def init_game():
    snake = [(100, 100), (90, 100), (80, 100)]
    snake_direction = "RIGHT"
    food = (
        random.randrange(0, WIDTH // CELL_SIZE) * CELL_SIZE,
        random.randrange(0, HEIGHT // CELL_SIZE) * CELL_SIZE
    )
    return snake, snake_direction, food

snake, snake_direction, food = init_game()

#Step 05 : Drawing co-ordinates
def draw_grid():
    for x in range(0, WIDTH, CELL_SIZE):
        pygame.draw.line(screen, GRID_COLOR, (x, 0), (x, HEIGHT))
    for y in range(0, HEIGHT, CELL_SIZE):
        pygame.draw.line(screen, GRID_COLOR, (0, y), (WIDTH, y))

def draw_snake(snake):
    for i, block in enumerate(snake):
        # Gradient effect on snake blocks
        color_value = 255 - i*10 if 255 - i*10 > 50 else 50
        color = (color_value, 255, 180)
        pygame.draw.rect(screen, color, pygame.Rect(block[0], block[1], CELL_SIZE, CELL_SIZE), border_radius=6)

def draw_food(food):
    pygame.draw.rect(screen, FOOD_COLOR, pygame.Rect(food[0], food[1], CELL_SIZE, CELL_SIZE), border_radius=6)
    # small glow effect
    pygame.draw.rect(screen, (255, 150, 150), pygame.Rect(food[0]+4, food[1]+4, CELL_SIZE-8, CELL_SIZE-8), border_radius=3)

def draw_score(score):
    score_text = font.render("Score : " + str(score), True, WHITE)
    screen.blit(score_text, (WIDTH - 150, 10))

#Step 06 : Snake Movement
def move_snake(snake, snake_direction):
    headX, headY = snake[0]

    if snake_direction == "UP":
        new_head = (headX, headY - CELL_SIZE)
    elif snake_direction == "DOWN":
        new_head = (headX, headY + CELL_SIZE)
    elif snake_direction == "RIGHT":
        new_head = (headX + CELL_SIZE, headY)
    elif snake_direction == "LEFT":
        new_head = (headX - CELL_SIZE, headY)

    snake.insert(0, new_head)

    #STEP 07 : check if snake has eaten the food
    if new_head == food:
        return True
    else:
        snake.pop()
        return False

#STEP 08 : check for collision
def collision(snake):
    snake_head = snake[0]
    if (snake_head[0] < 0 or snake_head[0] >= WIDTH or
        snake_head[1] < 0 or snake_head[1] >= HEIGHT):
        return True
    if snake_head in snake[1:]:
        return True
    return False

def show_game_over():
    game_over_text = game_over_font.render("Game Over!", True, (255, 102, 102))
    restart_text = font.render("Press SPACE to Play Again | ESC to Quit", True, WHITE)

    screen.blit(game_over_text, (WIDTH // 2 - 90, HEIGHT // 2 - 40))
    screen.blit(restart_text, (WIDTH // 2 - 170, HEIGHT // 2 + 10))
    pygame.display.update()

# Step 09 : Game Loop
Game_running = True
Game_over = False

while Game_running:

    screen.fill(BG_COLOR)
    draw_grid()  # optional grid for better look
    score = len(snake) - 3

    for KeyPressed in pygame.event.get():
        if KeyPressed.type == pygame.QUIT:
            Game_running = False

        elif KeyPressed.type == pygame.KEYDOWN and KeyPressed.key == pygame.K_ESCAPE:
            Game_running = False

        # Step 10 : Key handling
        elif KeyPressed.type == pygame.KEYDOWN and not Game_over:
            if KeyPressed.key == pygame.K_UP and snake_direction != "DOWN":
                snake_direction = "UP"
            elif KeyPressed.key == pygame.K_DOWN and snake_direction != "UP":
                snake_direction = "DOWN"
            elif KeyPressed.key == pygame.K_LEFT and snake_direction != "RIGHT":
                snake_direction = "LEFT"
            elif KeyPressed.key == pygame.K_RIGHT and snake_direction != "LEFT":
                snake_direction = "RIGHT"

        elif KeyPressed.type == pygame.KEYDOWN and Game_over:
            if KeyPressed.key == pygame.K_SPACE:
                snake, snake_direction, food = init_game()
                Game_over = False

    if not Game_over:
        # Step 11 : Move the snake
        food_eaten = move_snake(snake, snake_direction)

        # Step 12 : Generate new food if eaten
        if food_eaten:
            food = (
                random.randrange(0, WIDTH // CELL_SIZE) * CELL_SIZE,
                random.randrange(0, HEIGHT // CELL_SIZE) * CELL_SIZE
            )

        # Step 13 : Check for collisions
        if collision(snake):
            Game_over = True

        # Step 14 : Draw snake, food and score
        draw_snake(snake)
        draw_food(food)
        draw_score(score)
    else:
        show_game_over()

    pygame.display.update()
    clock.tick(7)  # slightly faster for fun

pygame.quit()
sys.exit()
