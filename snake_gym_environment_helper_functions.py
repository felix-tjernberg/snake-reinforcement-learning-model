from snake_game.snake_game_agent_version import Coordinate


def manhattan_distance(coordinate_one: Coordinate, coordinate_two: Coordinate):
    """Takes two coordinates and returns the manhattan distance between them"""
    return int(abs(coordinate_one.x - coordinate_two.x) + abs(coordinate_one.y - coordinate_two.y))
