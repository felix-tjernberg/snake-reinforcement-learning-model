from snake_gym_environment import SnakeGymEnvironment
from stable_baselines3 import PPO

environment = SnakeGymEnvironment()
environment.render()

ppo_model_path = f"models/saved_models/PPO_v2_1654532675_6440000"
loaded_PPO_model = PPO.load(ppo_model_path, environment)

environment.snake_game.GAME_SPEED = 30
for episode in range(10):
    observation = environment.reset()
    done = False
    while not done:
        action, _ = loaded_PPO_model.predict(observation)
        observation, reward, done, info = environment.step(action)
    print(f"Episode {episode} finished with a score of {environment.snake_game.score}")
environment.close()
