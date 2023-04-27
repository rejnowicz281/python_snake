import random

import pygame

# Initialize pygame
pygame.init()

# Create screen
SCREEN_WIDTH = 700
SCREEN_HEIGHT = 700
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

# Player
player = {
    "x": random.randint(100, 600),
    "y": random.randint(100, 600),
    "size_x": 30,
    "size_y": 30,
    "speed": 0.5,
    "direction": None
}


def draw_player(x, y):
    pygame.draw.rect(screen, (0, 255, 0), (x, y, player["size_x"], player["size_y"]))


# Game Loop
running = True
while running:

    # Background
    screen.fill((0, 0, 0))

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

        # Arrow movement
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_LEFT:
                player["direction"] = "left"
                print("direction left")
            elif event.key == pygame.K_RIGHT:
                player["direction"] = "right"
                print("direction right")
            elif event.key == pygame.K_UP:
                player["direction"] = "up"
                print("direction up")
            elif event.key == pygame.K_DOWN:
                player["direction"] = "down"
                print("direction down")

    if player["direction"] == "left":
        player["x"] -= player["speed"]
    elif player["direction"] == "right":
        player["x"] += player["speed"]
    elif player["direction"] == "up":
        player["y"] -= player["speed"]
    elif player["direction"] == "down":
        player["y"] += player["speed"]

    # Game Over
    if player["x"] < 0 or player["x"] > (SCREEN_WIDTH - player["size_x"]) or player["y"] < 0 or \
            player["y"] > (SCREEN_HEIGHT - player["size_y"]):
        player["speed"] = 0
        # Save high score
        with open("high_score.txt", "w") as file:
            file.write(str(high_score_value))
        show_game_over()

    draw_player(player["x"], player["y"])
    show_score(score_x, score_y)
    show_high_score(high_score_x, high_score_y)
    pygame.display.update()
