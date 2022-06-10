print('Remember to start tensorboard "pipenv shell" "tensorboard --logdir=logs/train_sessions/"')
from snake_gym_environment import SnakeGymEnvironment, SnakeGymEnvironmentCallback
from stable_baselines3 import PPO
import time
import os


# Change these values before running script
model_type = PPO
model_name_prefix = "PPO_v3_non_linear_between_food_reward"
total_timesteps_per_episode = 1000000
starting_episode = 14377
existing_model_name = "PPO_v3_non_linear_between_food_reward_1_1654770013_143770000"
model_number = 1


start_time = int(time.time())
saved_model_path = f"models/saved_models/{existing_model_name}"
model_name = f"{model_name_prefix}_{model_number}_{start_time}"
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
    loaded_model.save(f"{models_directory}/{model_name}_{starting_episode}_{total_timesteps_per_episode}")
