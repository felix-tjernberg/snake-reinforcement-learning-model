from enum import Enum
from collections import namedtuple

Coordinate = namedtuple("Coordinate", "x, y")


class Direction(Enum):
    RIGHT = 0
    LEFT = 1
    UP = 2
    DOWN = 3
