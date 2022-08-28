from snake_gym_environment import SnakeGymEnvironment
from stable_baselines3 import PPO

environment = SnakeGymEnvironment()


# Change before running model
environment.snake_game.GAME_SPEED = 30
MODEL_NAME = f"PPO_v4.2_head_position_1764_float_xy_observations_3_1661703048_5_1000000"


model_path = f"models/saved_models/{MODEL_NAME}.zip"
environment.render()
loaded_model = PPO.load(model_path, environment)


for episode in range(1, 11):
    observation = environment.reset()
    done = False
    while not done:
        action, _ = loaded_model.predict(observation)
        _, _, done, _ = environment.step(action)
    print(f"Episode {episode} finished with a score of {environment.snake_game.score}")
environment.close()
