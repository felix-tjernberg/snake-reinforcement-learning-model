from snake_helper_classes import Coordinate, Direction
import pygame
from random import randint


class SnakeGame:
    BLOCK_SIZE = 20
    COLORS = {"BACKGROUND": (154, 197, 2), "FOREGROUND": (1, 2, 0)}
    GAME_SPEED = 10

    def __init__(self, display_height=480, display_width=480):
        pygame.init()
        pygame.display.set_caption("Maskjävel")
        self.FONT = pygame.font.Font("./snake_game/8bit.ttf", 32)

        # User Interface
        self.display_border = False
        self.display_height = display_height
        self.display_width = display_width
        self.display = pygame.display.set_mode(
            (self.display_height, self.display_width), pygame.NOFRAME
        )
        self.update_display = True

        # Game State
        self.clock = pygame.time.Clock()
        self.direction = Direction.RIGHT
        self.game_over = False
        self.food = None
        self.score = 0

        self.head = Coordinate(self.display_height / 2, self.display_width / 2)
        self.body = [
            self.head,
            Coordinate(self.head.x - self.BLOCK_SIZE, self.head.y),
            Coordinate(self.head.x - self.BLOCK_SIZE * 2, self.head.y),
        ]
        self._place_food()

    def game_tick(self):
        self._move_snake()
        self.body.insert(0, self.head)

        self._check_collision()
        if self.game_over:
            pygame.quit()
            return self.game_over, self.score

        if self.update_display:
            self._update_display()
            self.clock.tick(self.GAME_SPEED)
        else:
            self.clock.tick()

        self._get_user_input()
        return self.game_over, self.score

    def _check_collision(self):
        if (
            self.head.x > self.display_width - self.BLOCK_SIZE
            or self.head.x < 0
            or self.head.y > self.display_height - self.BLOCK_SIZE
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
                pygame.quit()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_DOWN:
                    change_to_direction = Direction.DOWN
                elif event.key == pygame.K_LEFT:
                    change_to_direction = Direction.LEFT
                elif event.key == pygame.K_RIGHT:
                    change_to_direction = Direction.RIGHT
                elif event.key == pygame.K_UP:
                    change_to_direction = Direction.UP
                elif event.key == pygame.K_SPACE:
                    self.update_display = not self.update_display
                elif event.key == pygame.K_ESCAPE:
                    pygame.quit()
                elif event.key == pygame.K_b:
                    pygame.display.set_mode(
                        (self.display_height, self.display_width), pygame.SHOWN
                    )
                elif event.key == pygame.K_n:
                    pygame.display.set_mode(
                        (self.display_height, self.display_width), pygame.NOFRAME
                    )

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
            x += self.BLOCK_SIZE
        elif self.direction == Direction.LEFT:
            x -= self.BLOCK_SIZE
        elif self.direction == Direction.UP:
            y -= self.BLOCK_SIZE
        elif self.direction == Direction.DOWN:
            y += self.BLOCK_SIZE
        self.head = Coordinate(x, y)

    def _place_food(self):
        x = (
            randint(0, (self.display_height - self.BLOCK_SIZE) // self.BLOCK_SIZE)
            * self.BLOCK_SIZE
        )
        y = (
            randint(0, (self.display_width - self.BLOCK_SIZE) // self.BLOCK_SIZE)
            * self.BLOCK_SIZE
        )
        self.food = Coordinate(x, y)
        if self.food in self.body:
            self._place_food()

    def _update_display(self):
        self.display.fill(self.COLORS["BACKGROUND"])

        for coordinate in self.body:
            pygame.draw.rect(
                self.display,
                self.COLORS["FOREGROUND"],
                pygame.Rect(
                    coordinate.x, coordinate.y, self.BLOCK_SIZE, self.BLOCK_SIZE
                ),
            )

        pygame.draw.rect(
            self.display,
            self.COLORS["FOREGROUND"],
            pygame.Rect(self.food.x, self.food.y, self.BLOCK_SIZE, self.BLOCK_SIZE),
        )

        text = self.FONT.render(f"Score: {self.score}", True, self.COLORS["FOREGROUND"])
        self.display.blit(text, [16, 16])
        pygame.display.flip()


if __name__ == "__main__":
    snake_game_instance = SnakeGame()

    while True:
        game_over, score = snake_game_instance.game_tick()
        if game_over:
            break
    print(f"Score: {score}")
