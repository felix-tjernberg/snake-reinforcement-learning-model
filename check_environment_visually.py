from snake_gym_environment import SnakeGymEnvironment
from snake_game.snake_game_agent_version import Coordinate

environment = SnakeGymEnvironment()
environment.render()
environment.reset()
environment.snake_game.GAME_SPEED = 1

# Test check body float observation
environment.step(environment.action_space.sample())
observation, _, _, _ = environment.step(environment.action_space.sample())
print(environment.snake_game.body[:10])
print(observation[4:10])
environment.step(environment.action_space.sample())
observation, _, _, _ = environment.step(environment.action_space.sample())
print(environment.snake_game.body[:10])
print(observation[4:10])


# Test keeping direction reward
_, reward, _, _ = environment.step(environment.snake_game.DIRECTION["right"])
print("Reward for keeping direction:", reward)
_, reward, _, _ = environment.step(environment.snake_game.DIRECTION["right"])
print("Reward for keeping direction:", reward)
_, reward, _, _ = environment.step(environment.snake_game.DIRECTION["right"])
print("Reward for keeping direction:", reward)
environment.reset()


# Test eat food reward
environment.snake_game.food = Coordinate((environment.snake_game.head.x + 10), environment.snake_game.head.y)
_, reward, _, _ = environment.step(environment.snake_game.DIRECTION["right"])
print("Reward eating food", reward)


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
print("Reward kill self", reward)


# Test max steps punishment
environment.reset()
environment.snake_game.GAME_SPEED = 300
while environment.steps_taken_between_foods < environment.max_allowed_steps_between_foods:
    environment.step(environment.snake_game.DIRECTION["down"])
    environment.step(environment.snake_game.DIRECTION["left"])
    environment.step(environment.snake_game.DIRECTION["up"])
    environment.step(environment.snake_game.DIRECTION["right"])
environment.snake_game.GAME_SPEED = 1
environment.step(environment.snake_game.DIRECTION["up"])
environment.step(environment.snake_game.DIRECTION["up"])
_, reward, _, _ = environment.step(environment.snake_game.DIRECTION["up"])
print("Reward max steps", reward)
