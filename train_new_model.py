print('Remember to start tensorboard "pipenv shell" then "tensorboard --logdir=logs/train_sessions/"')
from snake_gym_environment import SnakeGymEnvironment, SnakeGymEnvironmentCallback
from stable_baselines3 import PPO
import time
import os

# Change these values before running script
model_type = PPO
model_name_prefix = "PPO_test"
total_timesteps_per_episode = 100000
model_number = 1


start_time = int(time.time())
model_name = f"{model_name_prefix}_{model_number}_{start_time}"
logs_directory = f"logs/train_sessions/"
models_directory = f"models/train_sessions/{model_name}/"

if not os.path.exists(models_directory):
    os.makedirs(models_directory)
if not os.path.exists(logs_directory):
    os.makedirs(logs_directory)


environment = SnakeGymEnvironment()
environment.reset()
model = PPO("MlpPolicy", environment, verbose=1, tensorboard_log=logs_directory)


episode = 0
while True:
    episode += 1
    model.learn(
        total_timesteps=total_timesteps_per_episode,
        reset_num_timesteps=False,
        tb_log_name=f"{model_name}",
        callback=SnakeGymEnvironmentCallback(),
    )
    model.save(f"{models_directory}/{model_name}_{total_timesteps_per_episode*episode}")
