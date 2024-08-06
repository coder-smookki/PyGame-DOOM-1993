from typing import Any
from game.core.config import *
from game.visual.hit import RayCastHit
from game.map.point import Point
from game.utils.utils import world_pos2tile

"""
Реализация 2.5D эффекта
"""


class Ray:
    def __init__(self, origin: Point, direction: float, length: float = None, end: Point = None):
        """
        Ray class used for convenient use
        :param origin: start point of ray
        :param direction: direction of ray
        :param length: a parameter that determines the length of the beam
        :param end: end point of ray
        """
        self.origin = origin
        self.direction = direction

        if length is None and end is None:
            raise TypeError('Ray.__init__ method has only 3 required arguments '
                            'start: Point, angel: float and (length: float or end: Point)')
        elif length is not None and end is not None:
            raise TypeError(
                'Ray.__init__ method has only 3 required arguments, '
                'you can`t use length and end parameters at the same time')

    def ray_cast(self):
        player_x, player_y = self.origin
        cos_a, sin_a = math.cos(self.direction), math.sin(self.direction)
        square_x, square_y = world_pos2tile(self.origin.x, self.origin.y)

        cos_a = 10 ** -10 if cos_a == 0 else cos_a
        sin_a = 10 ** -10 if sin_a == 0 else sin_a

        x_ver, y_ver, vert_dist, ver_offset = self.vertical_collision(square_x, player_x, player_y, sin_a, cos_a)
        x_hor, y_hor, hor_dist, hor_offset = self.horizontal_collision(square_y, player_x, player_y, sin_a, cos_a)

        if hor_dist > vert_dist:
            return RayCastHit(vert_dist, (x_ver, y_ver), self.direction, ver_offset)
        return RayCastHit(hor_dist, (x_hor, y_hor), self.direction, hor_offset)

    @staticmethod
    def vertical_collision(square_x, player_x, player_y, sin_a, cos_a) -> tuple[Any, Any, Any, Any]:
        y_ver, vert_dist = 0, 0
        x_ver, sign_x = (square_x + TILE, 1) if cos_a >= 0 else (square_x, -1)
        point, distance = None, None
        for i in range(0, min(MAX_VERTICAL_RAY_DISTANCE, MAX_RENDER_DISTANCE), TILE):
            vert_dist = (x_ver - player_x) / cos_a
            y_ver = player_y + vert_dist * sin_a
            tile_pos = world_pos2tile(x_ver + sign_x, y_ver)
            if tile_pos in WORLD_MAP.keys():
                point, distance = tile_pos, vert_dist
                break
            x_ver += sign_x * TILE

        offset = y_ver
        distance = vert_dist if distance is None else distance
        point = (x_ver, y_ver) if point is None else point
        return *point, distance, offset

    @staticmethod
    def horizontal_collision(square_y, player_x, player_y, sin_a, cos_a) -> tuple[Any, Any, Any, Any]:
        x_hor, hor_dist = 0, 0
        y_hor, sign_y = (square_y + TILE, 1) if sin_a >= 0 else (square_y, -1)
        point, distance = None, None
        for i in range(0, min(MAX_HORIZONTAL_RAY_DISTANCE, MAX_RENDER_DISTANCE), TILE):
            hor_dist = (y_hor - player_y) / sin_a
            x_hor = player_x + hor_dist * cos_a
            tile_pos = world_pos2tile(x_hor, y_hor + sign_y)
            if tile_pos in WORLD_MAP.keys():
                point, distance = tile_pos, hor_dist
                break
            y_hor += sign_y * TILE
        offset = x_hor
        distance = hor_dist if distance is None else distance
        point = (x_hor, y_hor) if point is None else point
        return *point, distance, offset
