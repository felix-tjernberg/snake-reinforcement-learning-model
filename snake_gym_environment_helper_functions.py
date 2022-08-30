from collections import deque
from snake_game.snake_game_agent_version import Coordinate


def manhattan_distance(coordinate_one: Coordinate, coordinate_two: Coordinate):
    """Takes two coordinates and returns the manhattan distance between them"""
    return int(abs(coordinate_one.x - coordinate_two.x) + abs(coordinate_one.y - coordinate_two.y))


def inverse_percentage(value_one: int, value_two: int):
    """Takes two values and returns the inverse percentage between them"""
    return 1 - (value_one / value_two)


def convert_snake_body_coordinates_to_float(snake_body_coordinates: list):
    """Takes a snake body list of coordinates and returns a modified version of that list where each coordinate is now a float in the format x//10.y//10"""
    return [float(f"{coordinate.x//10}.{coordinate.y//10}") for coordinate in snake_body_coordinates]
