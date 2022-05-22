from snake_gym_environment import SnakeGymEnvironment

environment = SnakeGymEnvironment()

done = False
environment.render()
observation = environment.reset()
while not done:
    random_action = environment.action_space.sample()
    print("action", random_action)
    _, reward, done, _ = environment.step(random_action)
    print("reward", reward)
