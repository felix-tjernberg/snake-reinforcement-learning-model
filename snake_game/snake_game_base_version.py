import pygame
from random import randint
from enum import Enum
from collections import namedtuple


Coordinate = namedtuple("Coordinate", "x, y")


class Direction(Enum):
    RIGHT = 0
    LEFT = 1
    UP = 2
    DOWN = 3


class SnekGame:
    COLORS = {"background": (154, 197, 2), "foreground": (1, 2, 0)}
    GRID_SIZE = 10  # Snake body, head and food size
    GAME_SPEED = 10  # Changes game difficulty for humans ;)

    def __init__(self, display_height=420, display_width=420):
        pygame.init()
        pygame.display.set_caption("snek_game")

        # User Interface
        self.display_border = False
        self.display_height = display_height
        self.display_width = display_width
        self.display = pygame.display.set_mode((self.display_height, self.display_width), pygame.NOFRAME)

        # Game State
        self.clock = pygame.time.Clock()
        self.direction = Direction.RIGHT
        self.game_over = False
        self.food = None
        self.score = 0
        self.quit_game = False

        self.head = Coordinate(self.display_height / 2, self.display_width / 2)
        self.body = [
            self.head,
            Coordinate(self.head.x - self.GRID_SIZE, self.head.y),
            Coordinate(self.head.x - self.GRID_SIZE * 2, self.head.y),
        ]
        self._place_food()

    def game_tick(self):
        self._move_snake()
        self._check_collision()
        if self.game_over or self.quit_game:
            pygame.quit()
            return self.game_over, self.score

        self._update_display()
        self.clock.tick(self.GAME_SPEED)

        self._get_user_input()
        return self.game_over, self.score

    def _check_collision(self):
        if (
            self.head.x > self.display_width - self.GRID_SIZE
            or self.head.x < 0
            or self.head.y > self.display_height - self.GRID_SIZE
            or self.head.y < 0
            or self.head in self.body[1:]
        ):
            self.game_over = True
            return
        self._check_head_position()

    def _check_head_position(self):
        if self.head == self.food:
            self.score += 1
            self._place_food()
        else:
            self.body.pop()

    def _get_user_input(self):
        change_to_direction = None
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.quit_game = True
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_DOWN:
                    change_to_direction = Direction.DOWN
                elif event.key == pygame.K_LEFT:
                    change_to_direction = Direction.LEFT
                elif event.key == pygame.K_RIGHT:
                    change_to_direction = Direction.RIGHT
                elif event.key == pygame.K_UP:
                    change_to_direction = Direction.UP
                elif event.key == pygame.K_ESCAPE:
                    self.quit_game = True
                elif event.key == pygame.K_b:
                    pygame.display.set_mode((self.display_height, self.display_width), pygame.SHOWN)
                elif event.key == pygame.K_n:
                    pygame.display.set_mode((self.display_height, self.display_width), pygame.NOFRAME)

        # Check if input makes snake go back into itself and prevent that
        if change_to_direction == Direction.UP and self.direction != Direction.DOWN:
            self.direction = Direction.UP
        if change_to_direction == Direction.DOWN and self.direction != Direction.UP:
            self.direction = Direction.DOWN
        if change_to_direction == Direction.LEFT and self.direction != Direction.RIGHT:
            self.direction = Direction.LEFT
        if change_to_direction == Direction.RIGHT and self.direction != Direction.LEFT:
            self.direction = Direction.RIGHT

    def _move_snake(self):
        x = self.head.x
        y = self.head.y
        if self.direction == Direction.RIGHT:
            x += self.GRID_SIZE
        elif self.direction == Direction.LEFT:
            x -= self.GRID_SIZE
        elif self.direction == Direction.UP:
            y -= self.GRID_SIZE
        elif self.direction == Direction.DOWN:
            y += self.GRID_SIZE
        self.head = Coordinate(x, y)
        self.body.insert(0, self.head)

    def _place_food(self):
        x = randint(0, (self.display_height - self.GRID_SIZE) // self.GRID_SIZE) * self.GRID_SIZE
        y = randint(0, (self.display_width - self.GRID_SIZE) // self.GRID_SIZE) * self.GRID_SIZE
        self.food = Coordinate(x, y)
        if self.food in self.body:
            self._place_food()

    def _update_display(self):
        self.display.fill(self.COLORS["background"])

        for coordinate in self.body:
            pygame.draw.rect(
                self.display,
                self.COLORS["foreground"],
                pygame.Rect(coordinate.x, coordinate.y, self.GRID_SIZE, self.GRID_SIZE),
            )

        pygame.draw.circle(
            self.display,
            self.COLORS["foreground"],
            (self.food.x + self.GRID_SIZE / 2, self.food.y + self.GRID_SIZE / 2),
            self.GRID_SIZE / 2,
        )

        pygame.display.flip()


if __name__ == "__main__":
    snake_game_instance = SnekGame()

    while True:
        game_over, score = snake_game_instance.game_tick()
        if game_over:
            break
    print(f"Score: {score}")
