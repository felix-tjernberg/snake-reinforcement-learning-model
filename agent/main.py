import gym


environment = gym.make("ALE/Pong-v5")
environment.reset()


if __name__ == "__main__":
    print(
        f"""
    sample action: {environment.action_space.sample()}
    observation space: {environment.observation_space.shape}
    sample observation: {environment.observation_space.sample()}
    """
    )
