from copy import deepcopy
import pygame
from game.core.config import *
from game.visual.hit import RayCastHit, SpriteHit
from game.visual.load_image import load_image
from game.core.ray_casting import ray_casting, sprites_ray_casting
from game.core.sprite import InteractiveSprite
from game.utils.utils import world_pos2cell


"""
Рендер хода игры
"""


sky_texture = load_image(TEXTURES_PATH, SKY_TEXTURE)
wall_textures = {
    '.': load_image(TEXTURES_PATH, RANGE_TEXTURE, color_key=None),
    'A': load_image(TEXTURES_PATH, STONE2, color_key=None),
    'B': load_image(TEXTURES_PATH, COMPUTER_1, color_key=None),
    'C': load_image(TEXTURES_PATH, COMPUTER_2, color_key=None),
    'D': load_image(TEXTURES_PATH, FACE_WALL_1, color_key=None),
    'E': load_image(TEXTURES_PATH, FACE_WALL_2, color_key=None),
    'F': load_image(TEXTURES_PATH, FACE_WALL_3, color_key=None),
    'G': load_image(TEXTURES_PATH, MARBLE_WALL_1, color_key=None),
    'H': load_image(TEXTURES_PATH, MARBLE_WALL_2, color_key=None),
    'J': load_image(TEXTURES_PATH, MARBLE_WALL_BLOOD, color_key=None),
    'K': load_image(TEXTURES_PATH, METAL_WALL, color_key=None),
    'L': load_image(TEXTURES_PATH, DUDE_WALL_1, color_key=None),
    'M': load_image(TEXTURES_PATH, DUDE_WALL_2, color_key=None),
    'N': load_image(TEXTURES_PATH, BASIC_WALL_2, color_key=None),
    'O': load_image(TEXTURES_PATH, BASIC_WALL_3, color_key=None),
    'P': load_image(TEXTURES_PATH, BASIC_WALL_4, color_key=None),
    'Q': load_image(TEXTURES_PATH, BASIC_WALL_5, color_key=None),
    'R': load_image(TEXTURES_PATH, NEW_WALL_1, color_key=None),
    'S': load_image(TEXTURES_PATH, NEW_WALL_2, color_key=None),
    'T': load_image(TEXTURES_PATH, NEW_WALL_3, color_key=None),
    'U': load_image(TEXTURES_PATH, NEW_WALL_4, color_key=None),
    'V': load_image(TEXTURES_PATH, NEW_WALL_5, color_key=None),
    'W': load_image(TEXTURES_PATH, NEW_WALL_6, color_key=None),
    'X': load_image(TEXTURES_PATH, NEW_WALL_7, color_key=None),
    'Y': load_image(TEXTURES_PATH, NEW_WALL_8, color_key=None),
    'Z': load_image(TEXTURES_PATH, NEW_WALL_9, color_key=None),
}


class Render:
    def __init__(self, screen, player, screen_map, sprites, level):
        self.screen = screen
        self._player = player
        self.screen_map = screen_map
        self.sprites = sprites
        self._level = level

    def render(self):
        self._draw_sky()
        self._draw_floor()
        self._draw_world()
        self._draw_minimap()
        self._player.draw()

    def _draw_floor(self):
        pygame.draw.rect(self.screen, ANTHRACITE, (0, HALF_SCREEN_HEIGHT, SCREEN_WIDTH, HALF_SCREEN_HEIGHT))

    def _draw_sky(self):
        sky_image = pygame.transform.scale(sky_texture, (SCREEN_WIDTH, SCREEN_HEIGHT))
        sky_offset = -10 * math.degrees(self._player.direction) % SCREEN_WIDTH
        self.screen.blit(sky_image, (sky_offset, 0))
        self.screen.blit(sky_image, (sky_offset + SCREEN_WIDTH, 0))
        self.screen.blit(sky_image, (sky_offset - SCREEN_WIDTH, 0))

    # Отрисовка 2.5D
    def _draw_world(self):
        sprite_hits = sprites_ray_casting(self.sprites, self._player.pos, self._player.direction)
        wall_hits = ray_casting(self._player.pos, self._player.direction)
        hits = list(sorted([*enumerate(sprite_hits), *enumerate(wall_hits)], key=lambda i: i[1].distance, reverse=True))
        self.draw_hit(hits)

    def draw_hit(self, hits):
        for hit_index, hit in hits:
            if isinstance(hit, RayCastHit):
                offset = int(hit.offset) % TILE
                distance = hit.distance * math.cos(self._player.direction - hit.angel)
                self._draw_wall(distance, offset, hit_index, hit.point)
            elif isinstance(hit, SpriteHit):
                sprite = self.sprites[hit.sprite_index]
                if isinstance(sprite, InteractiveSprite):
                    self.sprites[hit.sprite_index].full_update(self._player)
                self.draw_sprite(sprite.get_texture(), hit.distance, hit.casted_ray_index, sprite.vertical_scale,
                                 sprite.vertical_shift)

    def draw_sprite(self, texture, distance, current_ray, vertical_scale, vertical_shift):
        distance = max(distance, MIN_DISTANCE) * math.cos(HALF_FOV - current_ray * DELTA_ANGLE)
        projection_height = min(PROJECTION_COEFFICIENT / distance, SCREEN_HEIGHT * 2)
        projection_width = deepcopy(projection_height)
        sprite_x = current_ray * SCALE - projection_width // 2
        sprite_y = HALF_SCREEN_HEIGHT - (projection_height * vertical_scale) // 2

        if texture:
            texture = pygame.transform.scale(texture, (projection_width, projection_height))
            self.screen.blit(texture, (sprite_x, sprite_y + vertical_shift))

    def _draw_wall(self, distance, offset, hit_index, point):
        cell = world_pos2cell(*point)
        texture_char = self._level[cell[1]][cell[0]]
        texture_char = texture_char if texture_char in WALL_CHARS else '.'
        texture = wall_textures[texture_char]
        distance = max(distance, MIN_DISTANCE)
        projection_height = min(PROJECTION_COEFFICIENT / distance, SCREEN_HEIGHT * 2)
        wall = texture.subsurface(offset * TEXTURE_SCALE, 0, TEXTURE_SCALE,
                                  TEXTURE_HEIGHT)
        wall = pygame.transform.scale(wall, (SCALE, projection_height))
        self.screen.blit(wall, (hit_index * SCALE, HALF_SCREEN_HEIGHT - projection_height // 2))

    def _draw_minimap(self):
        self.screen_map.fill(BLACK)
        x, y = self._player.x / MAP_TILE, self._player.y / MAP_TILE
        cos_a, sin_a = math.cos(self._player.direction), math.sin(self._player.direction)
        pygame.draw.line(self.screen_map, YELLOW, (int(x) // MAP_TILE, int(y) // MAP_TILE),
                         (int(x) // MAP_TILE + MIINIMAP_OFFSET * cos_a, int(y) // MAP_TILE + MIINIMAP_OFFSET * sin_a),
                         2)
        pygame.draw.circle(self.screen_map, GREEN, (int(x) // MAP_TILE, int(y) // MAP_TILE), 3)
        for x, y in MINI_MAP:
            pygame.draw.rect(self.screen_map, RED, (x, y, MAP_TILE, MAP_TILE))
        self.screen.blit(self.screen_map,
                         (SCREEN_WIDTH - SCREEN_WIDTH // MAP_TILE + 80, SCREEN_HEIGHT - SCREEN_HEIGHT // MAP_TILE))
