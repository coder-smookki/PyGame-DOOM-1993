from game.core.config import *

"""Создание карты и мини карты"""


def create_map(map_):
    WORLD_MAP.clear()
    for row_index, row in enumerate(map_):
        for col_index, el in enumerate(row):
            if el in WALL_CHARS:
                x, y = col_index * TILE, row_index * TILE
                WORLD_MAP[(x, y)] = el


def create_minimap(map_):
    MINI_MAP.clear()
    for row_index, row in enumerate(map_):
        for col_index, el in enumerate(row):
            if el in WALL_CHARS:
                x, y = col_index * MAP_TILE, row_index * MAP_TILE
                MINI_MAP.add((x, y))
