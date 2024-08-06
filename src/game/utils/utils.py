import math
import numba
import numpy
from game.core.config import TILE

"""
Утилиты в ходе игры по типу (Если у игрока, здоровье меньше или равно 0, то возвращать True при котором
открывается окно Lose
"""

@numba.njit(fastmath=True, cache=True)
def get_distance(x0, y0, x1, y1):
    return math.sqrt((x0 - x1) ** 2 + (y0 - y1) ** 2)


@numba.njit(fastmath=True, cache=True)
def world_pos2cell(x, y):
    return int(x // TILE), int(y // TILE)


@numba.njit(fastmath=True, cache=True)
def world_pos2tile(x, y):
    cx, cy = world_pos2cell(x, y)
    return cx * TILE, cy * TILE


def compare_deque(d1, d2):
    if len(d1) != len(d2):
        return False

    for i, j in zip(d1, d2):
        if i != j:
            return False

    return True


def is_game_over(player):
    if player.health <= 0:
        return True


def unit_vector(vector):
    return vector / numpy.linalg.norm(vector)


def angle_between_vectors(v1, v2):
    v1_u = unit_vector(v1)
    v2_u = unit_vector(v2)
    return numpy.arccos(numpy.clip(numpy.dot(v1_u, v2_u), -1.0, 1.0))
