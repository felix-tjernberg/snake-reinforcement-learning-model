print('Remember to start tensorboard "pipenv shell" "tensorboard --logdir=logs/train_sessions/"')
from snake_gym_environment import SnakeGymEnvironment, SnakeGymEnvironmentCallback
from stable_baselines3 import PPO
import time
import os


# Change these values before running script
MODEL_TYPE = PPO
MODEL_NAME_PREFIX = "PPO_v3_non_linear_between_food_reward"
TOTAL_TIMESTEPS_PER_EPISODE = 1000000
EXISTING_MODEL_NAME = "PPO_v3_non_linear_between_food_reward_1_1654770013_143770000"
MODEL_NUMBER = 1
episode = 14377  # change this to EXISTING_MODEL_NAME episode number


START_TIME = int(time.time())
SAVED_MODEL_PATH = f"models/saved_models/{EXISTING_MODEL_NAME}"
MODEL_NAME = f"{MODEL_NAME_PREFIX}_{MODEL_NUMBER}_{START_TIME}"
MODELS_DIRECTORY = f"models/train_sessions/{MODEL_NAME}/"
if not os.path.exists(MODELS_DIRECTORY):
    os.makedirs(MODELS_DIRECTORY)


environment = SnakeGymEnvironment()
environment.reset()
loaded_model = MODEL_TYPE.load(SAVED_MODEL_PATH, environment)


while True:
    episode += 1
    loaded_model.learn(
        total_timesteps=TOTAL_TIMESTEPS_PER_EPISODE,
        reset_num_timesteps=False,
        tb_log_name=f"{MODEL_NAME}",
        callback=SnakeGymEnvironmentCallback(),
    )
    if environment.scored_high_score:
        print(f"Model saved with a high score of {environment.high_score}")
        loaded_model.save(
            f"{MODELS_DIRECTORY}/{MODEL_NAME}_{episode}_{TOTAL_TIMESTEPS_PER_EPISODE}_{environment.high_score}"
        )
        environment.scored_high_score = False
