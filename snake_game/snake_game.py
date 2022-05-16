from snake_helper_classes import Coordinate, Direction
import pygame
import random


class SnakeGame:
    def __init__(self, window_height=480, window_width=480):
        pygame.init()
        self.BLOCK_SIZE = 20
        self.FONT = pygame.font.Font("./snake_game/arial.ttf", 25)
        self.GAME_SPEED = 10

        self.BLACK = (0, 0, 0)
        self.BLUE = (0, 0, 237)
        self.RED = (237, 0, 0)
        self.WHITE = (237, 237, 237)

        self.window_height = window_height
        self.window_width = window_width
        self.display = pygame.display.set_mode((self.window_height, self.window_width))
        pygame.display.set_caption("Maskjävel")

        self.clock = pygame.time.Clock()
        self.game_over = False
        self.direction = Direction.RIGHT
        self.head = Coordinate(self.window_height / 2, self.window_width / 2)
        self.body = [
            self.head,
            Coordinate(self.head.x - self.BLOCK_SIZE, self.head.y),
            Coordinate(self.head.x - self.BLOCK_SIZE * 2, self.head.y),
        ]
        self.score = 0
        self.food = None
        self._place_food()

    def game_tick(self):
        self._move()
        self.body.insert(0, self.head)

        self._check_collision()
        if self.game_over:
            pygame.quit()
            return self.game_over, self.score

        self._check_head_position()
        self._update_ui()
        self.clock.tick(self.GAME_SPEED)
        self._get_user_input()
        return self.game_over, self.score

    def _check_collision(self):
        if (
            self.head.x > self.window_width - self.BLOCK_SIZE
            or self.head.x < 0
            or self.head.y > self.window_height - self.BLOCK_SIZE
            or self.head.y < 0
            or self.head in self.body[1:]
        ):
            self.game_over = True

    def _check_head_position(self):
        if self.head == self.food:
            self.score += 1
            self._place_food()
        else:
            self.body.pop()

    def _get_user_input(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self._quit_game()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_DOWN:
                    self.direction = Direction.DOWN
                elif event.key == pygame.K_LEFT:
                    self.direction = Direction.LEFT
                elif event.key == pygame.K_RIGHT:
                    self.direction = Direction.RIGHT
                elif event.key == pygame.K_UP:
                    self.direction = Direction.UP

    def _move(self):
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
            random.randint(0, (self.window_height - self.BLOCK_SIZE) // self.BLOCK_SIZE)
            * self.BLOCK_SIZE
        )
        y = (
            random.randint(0, (self.window_width - self.BLOCK_SIZE) // self.BLOCK_SIZE)
            * self.BLOCK_SIZE
        )
        self.food = Coordinate(x, y)
        if self.food in self.body:
            self._place_food()

    def _update_ui(self):
        self.display.fill(self.BLACK)

        for coordinate in self.body:
            pygame.draw.rect(
                self.display,
                self.BLUE,
                pygame.Rect(
                    coordinate.x, coordinate.y, self.BLOCK_SIZE, self.BLOCK_SIZE
                ),
            )

        pygame.draw.rect(
            self.display,
            self.RED,
            pygame.Rect(self.food.x, self.food.y, self.BLOCK_SIZE, self.BLOCK_SIZE),
        )

        text = self.FONT.render(f"Score: {self.score}", True, self.WHITE)
        self.display.blit(text, [0, 0])
        pygame.display.flip()


if __name__ == "__main__":
    snake_game_instance = SnakeGame()

    while True:
        game_over, score = snake_game_instance.game_tick()
        if game_over:
            break
    print(f"Final score: {score}")
