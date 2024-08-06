from game.core.config import *
from game.visual.hit import SpriteHit
from game.map.point import Point
from game.core.ray import Ray, RayCastHit
from game.core.sprite import StaticSprite
from game.utils.utils import get_distance

"""
Коллизия и видимость текстур
"""


def ray_casting(player_pos: Point, player_angle: float) -> list[RayCastHit]:
    current_angle: float = player_angle - HALF_FOV
    ray_cast_hits: list[RayCastHit] = []
    for _ in range(RAYS_AMOUNT):
        ray = Ray(player_pos, current_angle, MAX_VIEW_DISTANCE)
        ray_cast_hit = ray.ray_cast()
        ray_cast_hits.append(ray_cast_hit)
        current_angle += DELTA_ANGLE
    return ray_cast_hits


def sprites_ray_casting(sprites: list[StaticSprite], player_pos: Point, player_angel: float) -> list[SpriteHit]:
    sprites_hits = []
    for sprite_index, sprite in enumerate(sprites):
        x, y = sprite.pos
        dx, dy = x - player_pos.x, y - player_pos.y
        distance = get_distance(x, y, player_pos.x, player_pos.y)
        point_angel = math.atan2(dy, dx)
        delta_angel = point_angel - player_angel
        if dx > 0 and math.pi <= player_angel <= math.pi * 2 or dx < 0 and dy < 0:
            delta_angel += math.pi * 2
        delta_ray_index = int(delta_angel / DELTA_ANGLE)
        current_ray_index = CENTER_RAY_INDEX + delta_ray_index
        if 0 <= current_ray_index <= RAYS_AMOUNT - 1:
            sprites_hits.append(
                SpriteHit(sprite_index, distance, delta_angel, current_ray_index, sprite.animation_list))
    return sprites_hits
