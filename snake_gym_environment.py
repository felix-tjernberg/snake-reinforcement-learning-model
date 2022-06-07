from gym import spaces, Env
from numpy import array, float32, inf
from snake_game.snake_game_agent_version import SnekGame
from stable_baselines3.common.callbacks import BaseCallback
from snake_gym_environment_helper_functions import manhattan_distance


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
        self.amount_of_steps_taken_between_foods += 1
        self.total_steps_taken += 1

        # Reward agent for getting closer to the food
        current_manhattan_distance_to_food = manhattan_distance(self.snake_game.food, self.snake_game.head)
        if current_manhattan_distance_to_food < self.first_manhattan_distance_to_food:
            if current_manhattan_distance_to_food not in self.manhattan_distance_reward_list:
                self.reward += 1
                self.manhattan_distance_reward_list.append(current_manhattan_distance_to_food)

        # Reward agent for eating food and reset amount of steps taken
        if self.snake_game.score > self.previous_score:
            self.reward += 100
            self.reward += self.max_amount_of_steps_allowed_between_foods - self.amount_of_steps_taken_between_foods
            self.amount_of_steps_taken_between_foods = 0
        self.previous_score = self.snake_game.score

        # Punish agent for eating itself
        if self.snake_game.game_over:
            if self.snake_game.head in self.snake_game.body[1:]:
                self.reward -= 100

        # Punish agent for not moving fast enough between foods
        if self.amount_of_steps_taken_between_foods == self.max_amount_of_steps_allowed_between_foods:
            self.reward -= 1000
            self.snake_game.game_over = True

        return (
            self.observe_game_state(),  # Observation array
            self.reward,
            self.snake_game.game_over,  # If the episode is done
            {"game_score": self.snake_game.score},  # Infos object
        )

    def reset(self):
        self.reward = 0
        self.snake_game.reset_game()

        self.manhattan_distance_reward_list = []
        self.first_manhattan_distance_to_food = manhattan_distance(self.snake_game.food, self.snake_game.head)

        self.amount_of_steps_taken_between_foods = 0
        self.max_amount_of_steps_allowed_between_foods = self.snake_game.max_score
        self.previous_score = self.snake_game.score
        self.total_steps_taken = 0

        return self.observe_game_state()  # In reset we only return the observation

    def observe_game_state(self):
        snake_head = self.snake_game.head
        food = self.snake_game.food
        food_delta_x = snake_head.x - food.x
        food_delta_y = snake_head.y - food.y
        return array(
            [
                snake_head.x,
                snake_head.y,
                food_delta_x,
                food_delta_y,
                len(self.snake_game.body),
                self.amount_of_steps_taken_between_foods,
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
