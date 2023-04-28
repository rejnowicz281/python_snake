import random

import pygame

# Initialize pygame
pygame.init()

# Create screen
CELL_SIZE = 35
ROWS = 20
COLS = 20
SCREEN_WIDTH = CELL_SIZE * COLS
SCREEN_HEIGHT = CELL_SIZE * ROWS
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))

# Score

score_value = 0
score_font = pygame.font.Font('freesansbold.ttf', 32)
score_x = 10
score_y = 50


def show_score(x, y):
    score = score_font.render("Score: " + str(score_value), True, (255, 255, 255))
    screen.blit(score, (x, y))


# High Score
try:
    with open("high_score.txt", "r") as file:
        high_score_value = int(file.read())
except FileNotFoundError:
    high_score_value = 0
high_score_x = 10
high_score_y = 10


def show_high_score(x, y):
    high_score = score_font.render("High score: " + str(high_score_value), True, (255, 255, 255))
    screen.blit(high_score, (x, y))


# Game Over
game_over_font = pygame.font.Font('freesansbold.ttf', 100)


def show_game_over():
    over_text = game_over_font.render("GAME OVER", True, (255, 255, 255))
    screen.blit(over_text, (50, 310))


# Title and Icon
pygame.display.set_caption("Snake")
icon = pygame.image.load('icon.png')
pygame.display.set_icon(icon)

# Snake
snake = {
    "body": [(8, 5), (9, 5), (10, 5), (11, 5)],
    "direction": (-1, 0)
}


def draw_snake():
    for cell in snake["body"]:
        x = cell[0] * CELL_SIZE
        y = cell[1] * CELL_SIZE
        rect = pygame.Rect(x, y, CELL_SIZE, CELL_SIZE)
        pygame.draw.rect(screen, (0, 255, 0), rect)


# Fruit
def random_fruit_pos():
    x = (random.randint(0, COLS - 1))
    y = (random.randint(0, ROWS - 1))
    if (x, y) not in snake["body"]:
        return x, y
    else:
        random_fruit_pos()


fruit = {
    "pos": random_fruit_pos()
}


def draw_fruit():
    x = fruit["pos"][0] * CELL_SIZE
    y = fruit["pos"][1] * CELL_SIZE
    rect = pygame.Rect(x, y, CELL_SIZE, CELL_SIZE)
    pygame.draw.rect(screen, (255, 0, 0), rect)


# Game Loop
running = True
while running:
    # Ensure 15 FPS
    pygame.time.Clock().tick(15)

    # Ensure that player can't change two directions at a time
    changed_direction = False

    # Background
    screen.fill((0, 0, 0))

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            high_score_value = score_value if score_value > high_score_value else high_score_value
            with open("high_score.txt", "w") as file:
                file.write(str(high_score_value))
            running = False

        # Arrow movement
        if event.type == pygame.KEYDOWN and not changed_direction:
            if event.key == pygame.K_LEFT and snake["direction"] != (1, 0):
                snake["direction"] = (-1, 0)
                print("direction left")
                changed_direction = True
            elif event.key == pygame.K_RIGHT and snake["direction"] != (-1, 0):
                snake["direction"] = (1, 0)
                print("direction right")
                changed_direction = True
            elif event.key == pygame.K_UP and snake["direction"] != (0, 1):
                snake["direction"] = (0, -1)
                print("direction up")
                changed_direction = True
            elif event.key == pygame.K_DOWN and snake["direction"] != (0, -1):
                snake["direction"] = (0, 1)
                print("direction down")
                changed_direction = True

    snake_head = (snake["body"][0][0] + snake["direction"][0], snake["body"][0][1] + snake["direction"][1])
    snake["body"].insert(0, snake_head)

    if snake_head == fruit["pos"]:
        score_value += 1
        high_score_value = score_value if score_value > high_score_value else high_score_value
        fruit["pos"] = random_fruit_pos()
    else:
        snake["body"].pop()

    draw_snake()
    draw_fruit()
    show_score(score_x, score_y)
    show_high_score(high_score_x, high_score_y)
    pygame.display.update()
