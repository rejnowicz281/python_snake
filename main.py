import random

import pygame
from pygame.math import Vector2

# Initialize pygame
pygame.init()

# Title and Icon
pygame.display.set_caption("Snake")
icon = pygame.image.load('icon.png')
pygame.display.set_icon(icon)

# Create screen
CELL_SIZE = 35
ROWS = 20
COLS = 20
SCREEN_WIDTH = CELL_SIZE * COLS
SCREEN_HEIGHT = CELL_SIZE * ROWS
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))


class Snake:
    def __init__(self):
        self.body = [Vector2(15, 5), Vector2(16, 5), Vector2(17, 5)]
        self.direction = Vector2(-1, 0)

    def draw(self):
        for cell in self.body:
            x = cell.x * CELL_SIZE
            y = cell.y * CELL_SIZE
            rect = pygame.Rect(x, y, CELL_SIZE, CELL_SIZE)
            pygame.draw.rect(screen, (0, 255, 0), rect)

    def head(self):
        return self.body[0] + self.direction

    def add_block(self):
        self.body.insert(0, Vector2(self.head()))


class Fruit:
    def __init__(self):
        self.pos = Vector2(0, 0)
        self.random_pos()

    def random_pos(self):
        x = (random.randint(0, COLS - 1))
        y = (random.randint(0, ROWS - 1))
        self.pos = Vector2(x, y)

    def draw(self):
        x = self.pos.x * CELL_SIZE
        y = self.pos.y * CELL_SIZE
        rect = pygame.Rect(x, y, CELL_SIZE, CELL_SIZE)
        pygame.draw.rect(screen, (255, 0, 0), rect)


class Game:
    def __init__(self):
        self.state = "running"
        self.snake = Snake()
        self.fruit = Fruit()
        self.score = 0
        self.high_score = 0
        self.load_high_score()

    def load_high_score(self):
        try:
            with open("high_score.txt", "r") as high_score_file:
                self.high_score = int(high_score_file.read())
        except FileNotFoundError:
            self.high_score = 0

    def draw_text(self, x, y, text, font=pygame.font.Font('freesansbold.ttf', 32)):
        content = font.render(text, True, (255, 255, 255))
        screen.blit(content, (x, y))

    def show_score(self):
        self.draw_text(10, 50, f"Score: {str(self.score)}")

    def show_high_score(self):
        self.draw_text(10, 10, f"High Score: {str(self.high_score)}")

    def show_game_over(self):
        self.draw_text(50, 310, "GAME OVER", pygame.font.Font('freesansbold.ttf', 100))

    def save_high_score(self):
        if self.score > self.high_score:
            self.high_score = self.score
            with open("high_score.txt", "w") as high_score_file:
                high_score_file.write(str(self.high_score))

    def update_snake(self):
        snake_head = self.snake.body[0] + self.snake.direction
        self.snake.add_block()

        # Fruit eating and tail popping
        if snake_head == self.fruit.pos:
            self.score += 1
            self.save_high_score()
            self.fruit.random_pos()
            while self.fruit.pos in self.snake.body:
                self.fruit.random_pos()
        else:
            self.snake.body.pop()

    def update_state(self):
        snake_head = self.snake.head()
        snake_body = self.snake.body

        if snake_head in snake_body or snake_head.x < 0 or snake_head.x > (COLS - 1) or snake_head.y < 0 or \
                snake_head.y > (ROWS - 1):
            self.state = "game_over"
            self.save_high_score()


# Game
game = Game()
running = True
while running:
    # Ensure 15 FPS
    pygame.time.Clock().tick(15)

    # Background
    screen.fill((0, 0, 0))

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            game.save_high_score()
            running = False

    keys = pygame.key.get_pressed()

    if keys[pygame.K_LEFT] and game.snake.direction.x != 1:
        game.snake.direction = Vector2(-1, 0)
    elif keys[pygame.K_RIGHT] and game.snake.direction.x != -1:
        game.snake.direction = Vector2(1, 0)
    elif keys[pygame.K_UP] and game.snake.direction.y != 1:
        game.snake.direction = Vector2(0, -1)
    elif keys[pygame.K_DOWN] and game.snake.direction.y != -1:
        game.snake.direction = Vector2(0, 1)

    if game.state == "running":
        game.update_snake()

        game.update_state()

    game.snake.draw()
    game.fruit.draw()

    if game.state == "game_over":
        game.show_game_over()

    game.show_score()
    game.show_high_score()
    pygame.display.update()
