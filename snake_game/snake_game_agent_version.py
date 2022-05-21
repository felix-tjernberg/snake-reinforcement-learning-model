import pygame
from random import randint
from enum import Enum
from collections import namedtuple
from time import sleep


Coordinate = namedtuple("Coordinate", "x, y")


class Direction(Enum):
    RIGHT = 0
    LEFT = 1
    UP = 2
    DOWN = 3


class SnekGame:
    COLORS = {"background": (154, 197, 2), "foreground": (1, 2, 0)}
    GRID_SIZE = 10  # Snake body, head and food size
    GAME_SPEED = 30  # Agents can play fast :)

    def __init__(
        self,
        *,
        display_height=420,
        display_ui=True,
        display_width=420,
    ):
        pygame.init()
        pygame.display.set_caption("snek_game")

        # User Interface
        self.display_height = display_height
        self.display_ui = display_ui
        self.display_width = display_width
        self.display = pygame.display.set_mode(
            (self.display_height, self.display_width), pygame.NOFRAME
        )

        # Game State
        self.agent_action = None
        self.clock = pygame.time.Clock()
        self.direction = Direction.RIGHT
        self.game_over = False
        self.food = None
        self.score = 0

        self.head = Coordinate(self.display_height / 2, self.display_width / 2)
        self.body = [
            self.head,
            Coordinate(self.head.x - self.GRID_SIZE, self.head.y),
            Coordinate(self.head.x - self.GRID_SIZE * 2, self.head.y),
        ]
        self._place_food()

    def game_tick(self):
        self._check_agent_input()
        self._move_snake()
        self._check_collision()

        if self.display_ui:
            self._update_display()
            self.clock.tick(self.GAME_SPEED)
        else:
            self.clock.tick()

    def reset_game(self):
        self.agent_action = None
        self.direction = Direction.RIGHT
        self.game_over = False
        self.score = 0
        self.head = Coordinate(self.display_height / 2, self.display_width / 2)
        self.body = [
            self.head,
            Coordinate(self.head.x - self.GRID_SIZE, self.head.y),
            Coordinate(self.head.x - self.GRID_SIZE * 2, self.head.y),
        ]
        self._place_food()

    def _check_agent_input(self):
        change_to_direction = None
        if self.agent_action == Direction.DOWN:
            change_to_direction = Direction.DOWN
        elif self.agent_action == Direction.LEFT:
            change_to_direction = Direction.LEFT
        elif self.agent_action == Direction.RIGHT:
            change_to_direction = Direction.RIGHT
        elif self.agent_action == Direction.UP:
            change_to_direction = Direction.UP

        # Check if input makes snake go back into itself and prevent that
        if change_to_direction == Direction.UP and self.direction != Direction.DOWN:
            self.direction = Direction.UP
        if change_to_direction == Direction.DOWN and self.direction != Direction.UP:
            self.direction = Direction.DOWN
        if change_to_direction == Direction.LEFT and self.direction != Direction.RIGHT:
            self.direction = Direction.LEFT
        if change_to_direction == Direction.RIGHT and self.direction != Direction.LEFT:
            self.direction = Direction.RIGHT

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
        x = (
            randint(0, (self.display_height - self.GRID_SIZE) // self.GRID_SIZE)
            * self.GRID_SIZE
        )
        y = (
            randint(0, (self.display_width - self.GRID_SIZE) // self.GRID_SIZE)
            * self.GRID_SIZE
        )
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

    snake_game_instance.game_tick()
    snake_game_instance.agent_action = Direction.DOWN
    snake_game_instance.game_tick()
    snake_game_instance.agent_action = Direction.LEFT
    snake_game_instance.game_tick()
    snake_game_instance.agent_action = Direction.UP
    snake_game_instance.game_tick()
    sleep(2)
    snake_game_instance.reset_game()
    snake_game_instance.game_tick()
    sleep(2)
