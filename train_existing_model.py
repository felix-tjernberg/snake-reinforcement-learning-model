print('Remember to start tensorboard "pipenv shell" "tensorboard --logdir=logs/train_sessions/"')
from snake_gym_environment import SnakeGymEnvironment, SnakeGymEnvironmentCallback
from stable_baselines3 import PPO
import time
import os

start_time = int(time.time())

# Change these values before running script
model_type = PPO
model_name_prefix = "PPO_v3_non_linear_step_reward"
total_timesteps_per_episode = 100000
starting_episode = 4077  # 4077 * 100000 = 407700000
existing_model_name = "PPO_v3_non_linear_step_reward_1654672523_40770000"
saved_model_path = f"models/saved_models/{existing_model_name}"
model_number = 1


model_name = f"{new_model_prefix}_{start_time}_{model_number}"
models_directory = f"models/train_sessions/{model_name}/"
if not os.path.exists(models_directory):
    os.makedirs(models_directory)

environment = SnakeGymEnvironment()
environment.reset()
loaded_model = model_type.load(saved_model_path, environment)

while True:
    starting_episode += 1
    loaded_model.learn(
        total_timesteps=total_timesteps_per_episode,
        reset_num_timesteps=False,
        tb_log_name=f"{model_name}",
        callback=SnakeGymEnvironmentCallback(),
    )
    loaded_model.save(f"{models_directory}/{model_name}_{total_timesteps_per_episode*starting_episode}")
