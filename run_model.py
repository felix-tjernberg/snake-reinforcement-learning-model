from snake_gym_environment import SnakeGymEnvironment
from stable_baselines3 import PPO

environment = SnakeGymEnvironment()

model_name = f"PPO_v3_keep_direction_reward_4_actions_3_1654867981_305_1000000"
environment.snake_game.GAME_SPEED = 30

model_path = f"models/saved_models/{model_name}"
environment.render()
loaded_model = PPO.load(model_path, environment)

for episode in range(1, 11):
    observation = environment.reset()
    done = False
    while not done:
        action, _ = loaded_model.predict(observation)
        observation, reward, done, info = environment.step(action)
    print(f"Episode {episode} finished with a score of {environment.snake_game.score}")
    # print(f"Agent took {environment.steps_taken_between_foods} steps between last two foods")
    # print(f"Agent took {environment.total_steps_taken} steps total")
environment.close()
