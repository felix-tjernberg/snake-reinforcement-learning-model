print('Remember to start tensorboard "pipenv shell" "tensorboard --logdir=logs"')
from snake_gym_environment import SnakeGymEnvironment
from stable_baselines3 import PPO
import time
import os

start_time = int(time.time())
model_name = f"PPO_v1_{start_time}"
log_directory = f"logs/{start_time}/"
models_directory = f"models/{model_name}/"
if not os.path.exists(models_directory):
    os.makedirs(models_directory)
if not os.path.exists(log_directory):
    os.makedirs(log_directory)

environment = SnakeGymEnvironment()
environment.reset()
model = PPO("MlpPolicy", environment, verbose=1, tensorboard_log=log_directory)

TIMESTEPS = 10000
episode = 0  # Change this if you are continuing training a model
# while True:
# for episode in range(10):
while True:
    episode += 1
    model.learn(total_timesteps=TIMESTEPS, reset_num_timesteps=False, tb_log_name=f"{model_name}")
    model.save(f"{models_directory}/{TIMESTEPS*episode}")
