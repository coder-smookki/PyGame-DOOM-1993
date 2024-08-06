import collections
import pygame.time
from game.core.config import *
from game.visual.load_image import load_image
from game.map.point import Point
from game.core.ray import Ray
from game.sound.sound import SpritesSound
from game.utils.utils import get_distance, world_pos2cell, compare_deque, world_pos2tile, angle_between_vectors


"""
Вся роспись спрайтов и так же их назначение по группам 
"""


sprite_textures = {
    '3': {
        'default': collections.deque(
            [load_image(TEXTURES_PATH, f'devil/{i}.png') for i in range(DEVIL_ANIMATION_FRAMES_COUNT)]),
        'dead': collections.deque(
            [load_image(TEXTURES_PATH, f'devil/dead/{i}.png') for i in range(DEVIL_DEATH_ANIMATION_FRAMES_COUNT)])
    },
    '4': {
        'default': collections.deque(
            [load_image(TEXTURES_PATH, f'pin/{i}.png') for i in range(PIN_ANIMATION_FRAMES_COUNT)]),
        'dead': load_image(TEXTURES_PATH, 'pin/dead.png')
    },
    '5': {
        'default': collections.deque(
            [load_image(TEXTURES_PATH, f'flame/{i}.png') for i in range(FLAME_ANIMATION_FRAMES_COUNT)]),
        'dead': load_image(TEXTURES_PATH, 'flame/dead.png')
    },
    '6': {
        'default': collections.deque(
            [load_image(TEXTURES_PATH, f'devil_yellow/{i}.png') for i in range(DEVIL_YELLOW_ANIMATION_FRAMES_COUNT)]),
        'dead': collections.deque(
            [load_image(TEXTURES_PATH, f'devil_yellow/dead/{i}.png') for i in
             range(DEVIL_YELLOW_DEATH_ANIMATION_FRAMES_COUNT)])
    },
    '7': {
        'default': collections.deque(
            [load_image(TEXTURES_PATH, f'aerial/{i}.png') for i in range(AERIAL_ANIMATION_FRAMES_COUNT)]
        ),
        'dead': load_image(TEXTURES_PATH, 'aerial/dead.png')
    },
    '8': {
        'default': collections.deque(
            [load_image(TEXTURES_PATH, f'skull/{i}.png') for i in range(SKULL_ANIMATION_FRAMES_COUNT)]
        ),
        'dead': collections.deque(
            [load_image(TEXTURES_PATH, f'skull/dead/{i}.png') for i in range(SKULL_DEATH_ANIMATION_FRAMES_COUNT)])
    },
    '9': {
        'default': collections.deque(
            [load_image(TEXTURES_PATH, f'imp/{i}.png') for i in range(IMP_ANIMATION_FRAMES_COUNT)]),
        'dead': collections.deque(
            [load_image(TEXTURES_PATH, f'imp/dead/{i}.png') for i in range(IMP_DEATH_ANIMATION_FRAMES_COUNT)]),
        'attack': collections.deque(
            [load_image(TEXTURES_PATH, f'imp/attack/{i}.png') for i in range(IMP_ATTACK_ANIMATION_FRAMES_COUNT)])
    },
    'a': {
        'default': collections.deque(
            [load_image(TEXTURES_PATH, f'soldier/{i}.png') for i in range(SOLDIER_ANIMATION_FRAMES_COUNT)]),
        'dead': collections.deque(
            [load_image(TEXTURES_PATH, f'soldier/dead/{i}.png') for i in range(SOLDIER_DEATH_ANIMATION_FRAMES_COUNT)]),
        'attack': collections.deque(
            [load_image(TEXTURES_PATH, f'soldier/attack/{i}.png') for i in range(SOLDIER_ATTACK_ANIMATION_FRAMES_COUNT)]
        )
    },
    'b': {
        'default': collections.deque(
            [load_image(TEXTURES_PATH, f'death_soldier/{i}.png') for i in range(DEATH_SOLDIER_ANIMATION_FRAMES_COUNT)]
        )
    },
    'd': {
        'default': collections.deque(
            [load_image(TEXTURES_PATH, f'guitar_doom_guy/{i}.png') for i in
             range(GUITAR_DOOM_GUY_ANIMATION_FRAMES_COUNT)]
        )
    },
    'c': {
        'default': collections.deque(
            [load_image(TEXTURES_PATH, f'torch/{i}.png') for i in range(TORCH_ANIMATION_FRAMES_COUNT)])
    },
    'e': {
        'default': collections.deque(
            [load_image(TEXTURES_PATH, f'boss/{i}.png') for i in range(BOSS_ANIMATION_FRAMES_COUNT)]),
        'dead': collections.deque(
            [load_image(TEXTURES_PATH, f'boss/dead/{i}.png') for i in range(BOSS_DEATH_ANIMATION_FRAMES_COUNT)]),
        'attack': collections.deque(
            [load_image(TEXTURES_PATH, f'boss/attack/{i}.png') for i in range(BOSS_ATTACK_ANIMATION_FRAMES_COUNT)])
    },
    '#': {
        'default': collections.deque([load_image(TEXTURES_PATH, 'medkit.png')])
    },
    '$': {
        'default': collections.deque([load_image(TEXTURES_PATH, 'ammo.png')])
    }
}


def sprites_update(sprites, player):
    for sprite in sprites:
        sprite.update()
        if isinstance(sprite, InteractiveSprite):
            sprite.full_update(player)

            if sprite.can_attack(player):
                SpritesSound.damage()
                SpritesSound.get_damage(3)

                if not sprite.is_dead:
                    sprite.attack()
                    player.damage(sprite.damage)
            else:
                sprite.stop_attack()
        elif isinstance(sprite, PickableSprite):
            if sprite.can_pick(player.pos):
                sprite.pick()
                player.pick(sprite.type)

    return sprites


class StaticSprite:
    def __init__(self, animation_list, dead_texture, pos, vertical_scale=1.0, vertical_shift=0.0, destroyed=False,
                 animation_speed=SPRITE_ANIMATION_SPEED):
        self.dead_texture = dead_texture
        self.pos = pos
        self.is_dead = False
        self.vertical_scale = vertical_scale
        self.vertical_shift = vertical_shift
        self.destroyed = destroyed

        self.default_animation_list = animation_list.copy()
        self.animation_list = animation_list
        self.animation_count = 0
        self.animation_speed = animation_speed

        self.texture = self.animation_list[0].copy()
        self.default_texture = self.texture.copy()

    def death(self):
        self.is_dead = True

    def reset(self):
        self.is_dead = False

    def get_texture(self):
        if not self.destroyed:
            return self.animation_list[0]
        else:
            if self.is_dead:
                return self.dead_texture
            else:
                return self.animation_list[0]

    def update(self):
        self.animation_count += 1
        if self.animation_count == self.animation_speed:
            self.animation_list.rotate(-1)
            self.animation_count = 0

    def copy(self):
        return StaticSprite(self.animation_list, self.dead_texture, self.pos, self.vertical_scale, self.vertical_shift,
                            self.destroyed, animation_speed=self.animation_speed)


class InteractiveSprite(StaticSprite):
    def __init__(self, animation_list, dead_texture, pos, speed, damage, hit_distance, vertical_scale=1.0,
                 vertical_shift=0.0, attack_animation_list=None, death_animation_list=None,
                 animation_speed=SPRITE_ANIMATION_SPEED, health=1):
        super(InteractiveSprite, self).__init__(animation_list, dead_texture, pos, vertical_scale, vertical_shift,
                                                animation_speed)
        self.damage = damage

        self._speed = speed
        self._hit_distance = hit_distance
        self._attack_delay = 0
        self._attack = False
        self._attack_animation_list = None if attack_animation_list is None else attack_animation_list.copy()
        self._death_animation_list = None if death_animation_list is None else death_animation_list.copy()
        self._is_death_animation_playing = False
        self._health = health
        self._moving = False

    def full_update(self, player):
        self._move_to(player.x, player.y)
        self._attack_delay += pygame.time.get_ticks() / 1000
        if self._health <= 0:
            self.death()
        super(InteractiveSprite, self).update()

    def copy(self):
        return InteractiveSprite(self.animation_list, self.dead_texture, self.pos, self._speed, self.damage,
                                 self._hit_distance, self.vertical_scale, self.vertical_shift,
                                 self._attack_animation_list,
                                 self._death_animation_list, self.animation_speed, self._health)

    def get_damage(self, val):
        self._health -= val

    def death(self):
        super(InteractiveSprite, self).death()
        self._start_death_animation()

    def attack(self):
        self._start_attack_animation()
        self._attack = True

    def stop_attack(self):
        if self._attack_animation_list is not None and self._attack:
            self._stop_attack_animation()
        else:
            self._attack = False

    def get_texture(self):
        if self._is_death_animation_playing and self._death_animation_list is not None:
            if self._is_death_animation_finished():
                self.animation_list = collections.deque([self.dead_texture.copy()])

        # Return default dead texture if death animation not passed else return current animation frame
        if self.is_dead and self._death_animation_list is None:
            return self.dead_texture.copy()
        elif not self._moving and not self.is_dead:
            return self.default_animation_list[0].copy()
        else:
            return self.animation_list[0].copy()

    def can_attack(self, target):
        if self._can_attack(target):
            self._attack_delay = 0
            return True

        return False

    def _move_to(self, to_x, to_y):
        distance_to_target = get_distance(*self.pos, to_x, to_y)

        if distance_to_target >= SPRITE_VISIBILITY_AREA:
            self._moving = False
            return

        tile_x, tile_y = world_pos2tile(*self.pos)
        to_tile_x, to_tile_y = world_pos2tile(to_x, to_y)
        # If not is dead and next pos if not a finish point
        if not self.is_dead and (tile_x, tile_y) != (to_tile_x, to_tile_y):
            dx, dy = self.pos[0] - to_x, self.pos[1] - to_y
            move_coefficient_x, move_coefficient_y = 1 if dx < 0 else -1, 1 if dy < 0 else -1
            next_x = self.pos[0] + move_coefficient_x * self._speed
            next_y = self.pos[1] + move_coefficient_y * self._speed
            cell_x, cell_y = world_pos2cell(next_x, next_y)
            """If next pos is not a wall, else move forward (backward) if wall not forward (backward), 
             else move right (left) if wall not right (left)"""
            if (cell_x * TILE, cell_y * TILE) not in WORLD_MAP:
                self.pos = [next_x, next_y]
                self._moving = True
            elif (cell_x * TILE, tile_y) not in WORLD_MAP:
                self.pos = [next_x, tile_y]
                self._moving = True
            elif (tile_x, cell_y * TILE) not in WORLD_MAP:
                self.pos = [tile_x, next_y]
                self._moving = True
            else:
                self._moving = False
        else:
            self._moving = False

    def _start_death_animation(self):
        if self._death_animation_list is not None:
            if not self._is_death_animation_playing:
                self.animation_list = self._death_animation_list.copy()
                self.animation_list.rotate(-1)
                self._is_death_animation_playing = True
        else:
            self._is_death_animation_playing = False
            self.animation_list = collections.deque([self.dead_texture.copy()])

    def _start_attack_animation(self):
        if self._attack_animation_list and not self._attack:
            self.animation_list = self._attack_animation_list.copy()
            self.animation_list.rotate(-1)

    def _stop_attack_animation(self):
        if self._attack and compare_deque(self.animation_list, self._attack_animation_list):
            self._attack = False
            self.animation_list = self.default_animation_list.copy()

    def _is_death_animation_finished(self):
        return compare_deque(self.animation_list, self._death_animation_list)

    def _can_attack(self, target):
        distance_to_target = get_distance(*self.pos, target.x, target.y)
        return not self.is_dead and self._attack_delay >= SPRITE_ATTACK_DELAY and \
               self._can_hit(distance_to_target) and self._is_target_behind_the_wall(target.pos, distance_to_target)

    def _can_hit(self, distance_to_target):
        return distance_to_target <= self._hit_distance

    def _is_target_behind_the_wall(self, target_pos, distance_to_target):
        dx, dy = target_pos[0] - self.pos[0], target_pos[1] - self.pos[1]
        ray_cast_distance = Ray(Point(*self.pos), angle_between_vectors(RIGHT_VECTOR, (dx, dy, 0)),
                                MAX_VIEW_DISTANCE).ray_cast().distance
        return distance_to_target < ray_cast_distance


class PickableSpriteTypes:
    MED_KIT = 'MED_KIT'
    AMMO = 'AMMO'


class PickableSprite(StaticSprite):
    def __init__(self, sprite_type, animation_list, dead_texture, pos, pickled=False):
        super(PickableSprite, self).__init__(animation_list, dead_texture, pos)
        self.pickled = pickled
        self.type = sprite_type

    def can_pick(self, pos):
        if self.pickled:
            return False

        from_x, from_y = world_pos2tile(*pos)
        x, y = world_pos2tile(*self.pos)

        return (from_x == x and from_y == y) or (from_x + TILE == x and from_y + TILE == y) or (
                from_x - TILE == x and from_y - TILE == y)

    def pick(self):
        self.pickled = True

    def get_texture(self):
        if not self.pickled:
            return self.animation_list[0]
        else:
            return

    def copy(self):
        return PickableSprite(self.type, self.animation_list, self.dead_texture, self.pos, self.pickled)


movable_sprites_dict = {
    '3': InteractiveSprite(sprite_textures['3']['default'], sprite_textures['3']['dead'][-1], None, speed=2, damage=5,
                           hit_distance=SPRITE_HIT_DISTANCE * 2, death_animation_list=sprite_textures['3']['dead'],
                           health=3),
    '4': InteractiveSprite(sprite_textures['4']['default'], sprite_textures['4']['dead'], None, speed=1, damage=3,
                           hit_distance=SPRITE_HIT_DISTANCE * 4, health=3),
    '6': InteractiveSprite(sprite_textures['6']['default'], sprite_textures['6']['dead'][-1], None, speed=1, damage=5,
                           hit_distance=SPRITE_HIT_DISTANCE * 4, death_animation_list=sprite_textures['6']['dead'],
                           health=4),
    '7': InteractiveSprite(sprite_textures['7']['default'], sprite_textures['7']['dead'], None, speed=1, damage=0.5,
                           hit_distance=SPRITE_HIT_DISTANCE * 6, health=1),
    '8': InteractiveSprite(sprite_textures['8']['default'], sprite_textures['8']['dead'][-1], None, speed=2, damage=3,
                           hit_distance=SPRITE_HIT_DISTANCE * 1.5, health=3,
                           death_animation_list=sprite_textures['8']['dead']),
    '9': InteractiveSprite(sprite_textures['9']['default'], sprite_textures['9']['dead'][-1], None, speed=2, damage=5,
                           hit_distance=SPRITE_HIT_DISTANCE * 1.5, attack_animation_list=sprite_textures['9']['attack'],
                           death_animation_list=sprite_textures['9']['dead'], health=5),
    'a': InteractiveSprite(sprite_textures['a']['default'], sprite_textures['a']['dead'][-1], None, speed=1, damage=3,
                           hit_distance=SPRITE_HIT_DISTANCE * 5, attack_animation_list=sprite_textures['a']['attack'],
                           death_animation_list=sprite_textures['a']['dead'], health=5),
    'e': InteractiveSprite(sprite_textures['e']['default'], sprite_textures['e']['dead'][-1], None, speed=3, damage=10,
                           death_animation_list=sprite_textures['e']['dead'],
                           attack_animation_list=sprite_textures['e']['attack'], health=30,
                           hit_distance=SPRITE_HIT_DISTANCE * 2)
}

static_sprites_dict = {
    '5': StaticSprite(sprite_textures['5']['default'], sprite_textures['5']['dead'], None, 0.7),
    'b': StaticSprite(sprite_textures['b']['default'], None, None),
    'd': StaticSprite(sprite_textures['d']['default'], None, None, animation_speed=SPRITE_ANIMATION_SPEED / 2),
    'c': StaticSprite(sprite_textures['c']['default'], None, None, animation_speed=SPRITE_ANIMATION_SPEED / 2)
}

pickable_sprites_dict = {
    '#': PickableSprite(PickableSpriteTypes.MED_KIT, sprite_textures['#']['default'], None, None),
    '$': PickableSprite(PickableSpriteTypes.AMMO, sprite_textures['$']['default'], None, None)
}


def create_sprites(world_map) -> list[StaticSprite]:
    sprites = []
    for row_index, row in enumerate(world_map):
        for col_index, el in enumerate(row):
            if el in SPRITE_CHARS:
                sprite_pos = col_index * TILE + TILE // 2, row_index * TILE + TILE // 2
                sprite = None
                if el in STATIC_SPRITES:
                    sprite = static_sprites_dict[el].copy()
                elif el in MOVABLE_SPRITES:
                    sprite = movable_sprites_dict[el].copy()
                elif el in PICKABLE_SPRITES:
                    sprite = pickable_sprites_dict[el].copy()

                if el in SPRITE_CHARS and sprite is not None:
                    sprite.pos = sprite_pos
                    sprite.reset()
                    sprites.append(sprite)

    return sprites


def is_win(sprites):
    sprites = list(filter(lambda i: isinstance(i, InteractiveSprite), sprites))
    for sprite in sprites:
        if not sprite.is_dead:
            return False

    return True
