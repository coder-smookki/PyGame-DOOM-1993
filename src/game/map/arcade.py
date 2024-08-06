import os
import random
from copy import deepcopy
from game.core.config import *
from game.utils.utils import world_pos2cell

"""
Прописан класс Arcade, который отвечает за мод в игре.
В этом моде появляются рандомные противники и можно бесконечно выживать
"""


class Arcade:
    def __init__(self, arcade_map_file_name):
        self.level_path = os.path.join(LEVELS_PATH, arcade_map_file_name)
        self.clean_map = self.load_map()
        self.map = deepcopy(self.clean_map)
        self.spawns = self.get_spawns()

    def load_map(self):
        with open(self.level_path, 'r') as file:
            lines = list(map(str.strip, file.readlines()))
            lines = list(map(list, lines))
            file.close()

        return lines

    def get_spawns(self):
        spawns = list()

        for row_index, row in enumerate(self.map):
            for el_index, el in enumerate(row):
                if el == ARCADE_SPAWN_CHAR:
                    x, y = el_index * TILE, row_index * TILE
                    spawns.append((x, y))

        return spawns

    @staticmethod
    def get_random_sprite():
        return random.choice(MOVABLE_SPRITES)

    def spawn(self, count):
        self.map = deepcopy(self.clean_map)

        spawns = [random.choice(self.spawns) for _ in range(count)]
        for spawn in spawns:
            cell_x, cell_y = world_pos2cell(*spawn)
            self.map[cell_y][cell_x] = self.get_random_sprite()

    def formated_map(self):
        new_map = []
        for row in self.map:
            new_map.append(''.join(row))

        return new_map

    def get_map(self):
        return self.formated_map()
