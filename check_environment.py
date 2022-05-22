from stable_baselines3.common.env_checker import check_env
from snake_gym_environment import SnakeGymEnvironment

environment = SnakeGymEnvironment()
check_env(environment)
