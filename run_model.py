from snake_gym_environment import SnakeGymEnvironment
from stable_baselines3 import PPO

environment = SnakeGymEnvironment()
environment.render()

model_path = f"models/saved_models/PPO_v3_non_linear_step_reward_1654672523_40770000"
loaded_model = PPO.load(model_path, environment)

environment.snake_game.GAME_SPEED = 30
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
