from snake_gym_environment import SnakeGymEnvironment
from stable_baselines3 import PPO

environment = SnakeGymEnvironment()

ppo_model_path = f"models/saved_models/PPO_v1_1653236185_960000"
loaded_PPO_model = PPO.load(ppo_model_path, environment)

environment.render()
for episode in range(10):
    observation = environment.reset()
    done = False
    while not done:
        action, _ = loaded_PPO_model.predict(observation)
        observation, reward, done, info = environment.step(action)
environment.close()
