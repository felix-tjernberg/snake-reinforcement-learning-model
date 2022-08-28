print('Remember to start tensorboard "pipenv shell" then "tensorboard --logdir=logs/train_sessions/"')
from snake_gym_environment import SnakeGymEnvironment, SnakeGymEnvironmentCallback
from stable_baselines3 import PPO
import time
import os


# Change these values before running script
MODEL_NAME_PREFIX = "PPO_v4.2_head_position_1764_float_xy_observations"
TOTAL_TIMESTEPS_PER_EPISODE = 100000
MODEL_NUMBER = 4


START_TIME = int(time.time())
MODEL_NAME = f"{MODEL_NAME_PREFIX}_{MODEL_NUMBER}_{START_TIME}"
LOGS_DIRECTORY = f"logs/train_sessions/"
MODELS_DIRECTORY = f"models/train_sessions/{MODEL_NAME}/"
if not os.path.exists(MODELS_DIRECTORY):
    os.makedirs(MODELS_DIRECTORY)
if not os.path.exists(LOGS_DIRECTORY):
    os.makedirs(LOGS_DIRECTORY)


environment = SnakeGymEnvironment()
environment.reset()
model = PPO("MlpPolicy", environment, verbose=1, tensorboard_log=LOGS_DIRECTORY)


episode = 0
while True:
    episode += 1
    model.learn(
        total_timesteps=TOTAL_TIMESTEPS_PER_EPISODE,
        reset_num_timesteps=False,
        tb_log_name=f"{MODEL_NAME}",
        callback=SnakeGymEnvironmentCallback(),
    )
    if environment.scored_high_score:
        print(f"Model saved with a high score of {environment.high_score}")
        model.save(f"{MODELS_DIRECTORY}/{MODEL_NAME}_{episode}_{TOTAL_TIMESTEPS_PER_EPISODE}_{environment.high_score}")
        environment.scored_high_score = False
