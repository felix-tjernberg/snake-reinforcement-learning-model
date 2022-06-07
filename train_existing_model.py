print('Remember to start tensorboard "pipenv shell" "tensorboard --logdir=logs"')
from snake_gym_environment import SnakeGymEnvironment, SnakeGymEnvironmentCallback
from stable_baselines3 import PPO
import time
import os

start_time = int(time.time())
model_name = f"PPO_v2_{start_time}"
log_directory = f"logs/train_sessions"
models_directory = f"models/train_sessions/{model_name}/"
if not os.path.exists(models_directory):
    os.makedirs(models_directory)
if not os.path.exists(log_directory):
    os.makedirs(log_directory)

environment = SnakeGymEnvironment()
environment.reset()

model_path = f"models/saved_models/PPO_v2_1654588851_40760000"
loaded_model = PPO.load(model_path, environment)

TIMESTEPS = 100000
episode = 4076  # 4076 * 10000 = 40760000
while True:
    episode += 1
    loaded_model.learn(
        total_timesteps=TIMESTEPS,
        reset_num_timesteps=False,
        tb_log_name=f"{model_name}",
        callback=SnakeGymEnvironmentCallback(),
    )
    loaded_model.save(f"{models_directory}/{model_name}_{TIMESTEPS*episode}")
