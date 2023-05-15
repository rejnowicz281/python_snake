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
CELL_SIZE = 40
ROWS = 18
COLS = 18
SCREEN_WIDTH = CELL_SIZE * COLS
SCREEN_HEIGHT = CELL_SIZE * ROWS
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))


def draw_text(x, y, text, rect_center=False, font=pygame.font.Font('freesansbold.ttf', 32)):
    content = font.render(text, True, (255, 255, 255))
    if rect_center:
        screen.blit(content, content.get_rect(center=(x, y)))
    else:
        screen.blit(content, (x, y))


def draw_background():
    color1 = (0, 220, 0)
    color2 = (0, 200, 0)
    for i in range(ROWS):
        for j in range(COLS):
            if i % 2 == 0:
                if j % 2 == 0:
                    pygame.draw.rect(screen, color1, (j * CELL_SIZE, i * CELL_SIZE, CELL_SIZE, CELL_SIZE))
                else:
                    pygame.draw.rect(screen, color2, (j * CELL_SIZE, i * CELL_SIZE, CELL_SIZE, CELL_SIZE))
            else:
                if j % 2 == 0:
                    pygame.draw.rect(screen, color2, (j * CELL_SIZE, i * CELL_SIZE, CELL_SIZE, CELL_SIZE))
                else:
                    pygame.draw.rect(screen, color1, (j * CELL_SIZE, i * CELL_SIZE, CELL_SIZE, CELL_SIZE))


class Snake:
    def __init__(self):
        self.body = [Vector2(15, 5), Vector2(16, 5), Vector2(17, 5)]
        self.direction = Vector2(-1, 0)

    def draw(self):
        body_bottomleft = pygame.image.load("graphics/snake/body_bottomleft.png")
        body_bottomright = pygame.image.load("graphics/snake/body_bottomright.png")
        body_horizontal = pygame.image.load("graphics/snake/body_horizontal.png")
        body_vertical = pygame.image.load("graphics/snake/body_vertical.png")
        body_topleft = pygame.image.load("graphics/snake/body_topleft.png")
        body_topright = pygame.image.load("graphics/snake/body_topright.png")

        head_down = pygame.image.load("graphics/snake/head_down.png")
        head_up = pygame.image.load("graphics/snake/head_up.png")
        head_left = pygame.image.load("graphics/snake/head_left.png")
        head_right = pygame.image.load("graphics/snake/head_right.png")

        tail_down = pygame.image.load("graphics/snake/tail_down.png")
        tail_left = pygame.image.load("graphics/snake/tail_left.png")
        tail_right = pygame.image.load("graphics/snake/tail_right.png")
        tail_up = pygame.image.load("graphics/snake/tail_up.png")

        for index, cell in enumerate(self.body):
            x = cell.x * CELL_SIZE
            y = cell.y * CELL_SIZE

            previous_cell_distance = cell - self.body[index - 1]

            if index == 0:  # Head image selection
                next_cell_distance = cell - self.body[index + 1]
                if next_cell_distance == Vector2(1, 0):
                    image = head_right
                elif next_cell_distance == Vector2(-1, 0):
                    image = head_left
                elif next_cell_distance == Vector2(0, -1):
                    image = head_up
                elif next_cell_distance == Vector2(0, 1):
                    image = head_down
            elif index == len(self.body) - 1:  # Tail image selection
                if previous_cell_distance == Vector2(-1, 0):
                    image = tail_left
                elif previous_cell_distance == Vector2(1, 0):
                    image = tail_right
                elif previous_cell_distance == Vector2(0, 1):
                    image = tail_down
                elif previous_cell_distance == Vector2(0, -1):
                    image = tail_up
            else:  # Body image selection
                next_cell_distance = cell - self.body[index + 1]

                if next_cell_distance == Vector2(1, 0) and previous_cell_distance == Vector2(0, -1) \
                        or next_cell_distance == Vector2(0, -1) and previous_cell_distance == Vector2(1, 0):
                    image = body_bottomleft

                elif next_cell_distance == Vector2(-1, 0) and previous_cell_distance == Vector2(0, -1) \
                        or next_cell_distance == Vector2(0, -1) and previous_cell_distance == Vector2(-1, 0):
                    image = body_bottomright

                elif next_cell_distance == Vector2(1, 0) and previous_cell_distance == Vector2(0, 1) \
                        or next_cell_distance == Vector2(0, 1) and previous_cell_distance == Vector2(1, 0):
                    image = body_topleft

                elif next_cell_distance == Vector2(0, 1) and previous_cell_distance == Vector2(-1, 0) \
                        or next_cell_distance == Vector2(-1, 0) and previous_cell_distance == Vector2(0, 1):
                    image = body_topright

                elif previous_cell_distance == Vector2(-1, 0) or previous_cell_distance == Vector2(1, 0):
                    image = body_horizontal

                elif previous_cell_distance == Vector2(0, -1) or previous_cell_distance == Vector2(0, 1):
                    image = body_vertical

            screen.blit(image, (x, y))

    def input(self):
        keys = pygame.key.get_pressed()

        if keys[pygame.K_LEFT] and self.direction.x != 1:
            self.direction = Vector2(-1, 0)
        elif keys[pygame.K_RIGHT] and self.direction.x != -1:
            self.direction = Vector2(1, 0)
        elif keys[pygame.K_UP] and self.direction.y != 1:
            self.direction = Vector2(0, -1)
        elif keys[pygame.K_DOWN] and self.direction.y != -1:
            self.direction = Vector2(0, 1)

    def head(self):
        return self.body[0]

    def add_head(self):
        self.body.insert(0, Vector2(self.head() + self.direction))


class Fruit:
    def __init__(self):
        self.pos = Vector2(0, 0)
        self.random_pos()

    def random_pos(self):
        x = (random.randint(0, COLS - 1))
        y = (random.randint(0, ROWS - 1))
        self.pos = Vector2(x, y)

    def draw(self):
        apple = pygame.image.load("graphics/apple.png").convert_alpha()
        apple = pygame.transform.rotozoom(apple, 0, 1.4)
        x = self.pos.x * CELL_SIZE - 7
        y = self.pos.y * CELL_SIZE - 7
        screen.blit(apple, (x, y))


class Game:
    def __init__(self):
        self.paused = False
        self.snake = Snake()
        self.fruit = self.get_fruit()
        self.score = 0
        self.high_score = self.get_high_score()

    def get_fruit(self):
        fruit = Fruit()
        while fruit.pos in self.snake.body:
            fruit.random_pos()

        return fruit

    @staticmethod
    def get_high_score():
        try:
            with open("high_score.txt", "r") as high_score_file:
                return int(high_score_file.read())
        except FileNotFoundError:
            return 0

    def show_score(self):
        draw_text(10, 50, f"Score: {str(self.score)}")

    def show_high_score(self):
        draw_text(10, 10, f"High Score: {str(self.high_score)}")

    @staticmethod
    def show_game_over():
        draw_text(SCREEN_WIDTH / 2, SCREEN_HEIGHT / 2, "GAME OVER", True, pygame.font.Font('freesansbold.ttf', 100))

    def save_high_score(self):
        if self.score > self.high_score:
            self.high_score = self.score
            with open("high_score.txt", "w") as high_score_file:
                high_score_file.write(str(self.high_score))

    def move_snake(self):
        self.snake.add_head()
        # Fruit eating and tail popping
        if self.snake.head() == self.fruit.pos:
            self.score += 1
            self.save_high_score()
            self.fruit.random_pos()
            while self.fruit.pos in self.snake.body:
                self.fruit.random_pos()
        else:
            self.snake.body.pop()

    def snake_collision_check(self):
        snake_head = self.snake.head()
        snake_head_to_be = self.snake.head() + self.snake.direction
        snake_body = self.snake.body[1:]

        return snake_head in snake_body \
            or snake_head_to_be.x < 0 \
            or snake_head_to_be.x > (COLS - 1) \
            or snake_head_to_be.y < 0 \
            or snake_head_to_be.y > (ROWS - 1)

    def update(self):
        if not game.paused:
            game.snake.input()
            if self.snake_collision_check():
                self.paused = True
                self.save_high_score()
            else:
                self.move_snake()

        draw_background()
        game.snake.draw()
        game.fruit.draw()
        game.show_score()
        game.show_high_score()

        if game.paused:
            game.show_game_over()


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

    game.update()

    pygame.display.update()
