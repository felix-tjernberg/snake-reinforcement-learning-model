from snake_gym_environment_old import SnakeGymEnvironment
from stable_baselines3 import PPO

environment = SnakeGymEnvironment()


# Change before running model
environment.snake_game.GAME_SPEED = 30
MODEL_NAME = f"current_best_50_high_score_PPO_v3_keep_direction_reward_4_actions_3_1654867981_305_1000000"


model_path = f"models/saved_models/{MODEL_NAME}"
environment.render()
loaded_model = PPO.load(model_path, environment)


for episode in range(1, 11):
    observation = environment.reset()
    done = False
    while not done:
        action, _ = loaded_model.predict(observation)
        observation, _, done, _ = environment.step(action)
    print(f"Episode {episode} finished with a score of {environment.snake_game.score}")
environment.close()
