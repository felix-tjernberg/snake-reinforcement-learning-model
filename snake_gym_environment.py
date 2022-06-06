from gym import spaces, Env
from numpy import array, float32, inf
from snake_game.snake_game_agent_version import SnekGame
from stable_baselines3.common.callbacks import BaseCallback


class SnakeGymEnvironment(Env):
    def __init__(self):
        super(SnakeGymEnvironment, self).__init__()
        self.action_space = spaces.Discrete(4)
        self.observation_space = spaces.Box(
            low=-inf,
            high=inf,
            # The observation shape is a one dimensional vector with 6 observations
            shape=(6,),
            dtype=float32,
        )
        self.snake_game = SnekGame()

    def step(self, action):
        self.snake_game.agent_action = action
        self.snake_game.game_tick()

        # Reward the agent for eating food and punish for game over
        if self.snake_game.game_over:
            self.reward = self.snake_game.score - 10
        else:
            self.reward = self.snake_game.score

        return (
            self.observe_game_state(),  # Observation array
            self.reward,
            self.snake_game.game_over,  # If the episode is done
            {"game_score": self.snake_game.score},  # Infos object
        )

    def reset(self):
        self.reward = 0
        self.snake_game.reset_game()
        return self.observe_game_state()  # In reset we only return the observation

    def observe_game_state(self):
        snake_head = self.snake_game.head
        food = self.snake_game.food
        food_delta_x = snake_head.x - food.x
        food_delta_y = snake_head.y - food.y

        all_body_x = [coordinate.x for coordinate in self.snake_game.body]
        all_body_y = [coordinate.y for coordinate in self.snake_game.body]

        return array(
            [
                snake_head.x,
                snake_head.y,
                food_delta_x,
                food_delta_y,
                sum(all_body_x),
                sum(all_body_y),
            ],
            dtype=float32,
        )

    def render(self, mode="real_time"):
        if mode == "real_time":
            self.snake_game.display_update = True

    def close(self):
        self.snake_game.quit_game()


class SnakeGymEnvironmentCallback(BaseCallback):
    """
    Callback for recording game score in logger object
    """

    def __init__(self, verbose=0):
        super(SnakeGymEnvironmentCallback, self).__init__(verbose)

    def _on_step(self) -> bool:
        self.logger.record("game_score", self.locals["infos"][0]["game_score"])
        return True
