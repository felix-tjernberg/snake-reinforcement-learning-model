from snake_gym_environment import SnakeGymEnvironment
from snake_game.snake_game_agent_version import Coordinate

environment = SnakeGymEnvironment()

done = False
environment.render()
observation = environment.reset()
environment.snake_game.GAME_SPEED = 1


# Test eat food reward and 10 random actions
environment.snake_game.food = Coordinate((environment.snake_game.head.x + 10), environment.snake_game.head.y)
_, reward, done, _ = environment.step(environment.snake_game.DIRECTION["right"])
print("reward eating food", reward)
for _ in range(10):
    random_action = environment.action_space.sample()
    # print("action", random_action)
    observation, reward, done, _ = environment.step(random_action)
    print("reward", reward)
    print("observation", observation)


# Test kill self punishment
environment.reset()
environment.snake_game.body = [
    environment.snake_game.head,
    Coordinate(environment.snake_game.head.x - environment.snake_game.GRID_SIZE, environment.snake_game.head.y),
    Coordinate(environment.snake_game.head.x - environment.snake_game.GRID_SIZE * 2, environment.snake_game.head.y),
    Coordinate(environment.snake_game.head.x - environment.snake_game.GRID_SIZE * 3, environment.snake_game.head.y),
    Coordinate(environment.snake_game.head.x - environment.snake_game.GRID_SIZE * 4, environment.snake_game.head.y),
]
environment.step(environment.snake_game.DIRECTION["down"])
environment.step(environment.snake_game.DIRECTION["left"])
_, reward, _, _ = environment.step(environment.snake_game.DIRECTION["up"])
print("reward kill self", reward)


# Test max steps punishment
environment.reset()
environment.snake_game.GAME_SPEED = 300
while environment.amount_of_steps_taken_between_foods < environment.max_amount_of_steps_allowed_between_foods:
    environment.step(environment.snake_game.DIRECTION["down"])
    environment.step(environment.snake_game.DIRECTION["left"])
    environment.step(environment.snake_game.DIRECTION["up"])
    environment.step(environment.snake_game.DIRECTION["right"])
environment.snake_game.GAME_SPEED = 1
environment.step(environment.snake_game.DIRECTION["up"])
environment.step(environment.snake_game.DIRECTION["up"])
_, reward, _, _ = environment.step(environment.snake_game.DIRECTION["up"])
print("reward max steps", reward)
