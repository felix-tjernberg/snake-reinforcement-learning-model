from snake_game.snake_game_agent_version import Coordinate


def manhattan_distance(coordinate_one: Coordinate, coordinate_two: Coordinate):
    """Takes two coordinates and returns the manhattan distance between them"""
    return int(abs(coordinate_one.x - coordinate_two.x) + abs(coordinate_one.y - coordinate_two.y))


def inverse_percentage(value_one: int, value_two: int):
    """Takes two values and returns the inverse percentage between them"""
    return 1 - (value_one / value_two)
