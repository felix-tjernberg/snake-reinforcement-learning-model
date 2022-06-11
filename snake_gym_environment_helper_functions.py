from collections import deque
from snake_game.snake_game_agent_version import Coordinate


def manhattan_distance(coordinate_one: Coordinate, coordinate_two: Coordinate):
    """Takes two coordinates and returns the manhattan distance between them"""
    return int(abs(coordinate_one.x - coordinate_two.x) + abs(coordinate_one.y - coordinate_two.y))


def inverse_percentage(value_one: int, value_two: int):
    """Takes two values and returns the inverse percentage between them"""
    return 1 - (value_one / value_two)


def append_coordinates_to_deque_in_float_form(coordinate: Coordinate, deque_of_coordinates: deque):
    """Appends coordinate x and y to a deque in a form of a float where integers are x and decimals are y"""
    coordinate = f"{coordinate.x//10}.{coordinate.y//10}"
    deque_of_coordinates.append(float(coordinate))
