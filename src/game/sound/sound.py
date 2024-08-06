import random
import pygame
from game.core.config import *


"""
Принцип работы музыки в игре
"""


class Music:
    def __init__(self, path=MUSIC_FILES):
        pygame.mixer.pre_init(44100, -16, 1, 512)
        pygame.mixer.init()
        self.path = path
        self.theme = pygame.mixer.music
        self.init_track()

    def init_track(self):
        self.theme.load(random.choice(self.path))
        for file in self.path:
            self.theme.queue(file)

    def play_music(self):
        if self.theme.get_volume() != 0:
            self.theme.set_volume(0.1)
            self.theme.play()

    def change_music_volume(self, volume):
        self.theme.set_volume(volume)

    def return_volume(self):
        return self.theme.get_volume()


class MenuMusic(Music):
    def __init__(self, path):
        super().__init__(path)
        self.path = path

    def init_track(self):
        self.theme.load(self.path)


class SoundEffect:
    def __init__(self, path):
        pygame.mixer.pre_init(44100, -16, 1, 512)
        pygame.mixer.init()
        self.init_track(path)

    def init_track(self, path):
        self.effect = pygame.mixer.Sound(path)

    def play_sound(self, channel=2):
        if not pygame.mixer.Channel(channel).get_busy():
            pygame.mixer.Channel(channel).play(self.effect)

    @staticmethod
    def change_effects_volume(volume):
        for channel in range(1, 5):
            pygame.mixer.Channel(channel).set_volume(volume)

    @staticmethod
    def return_volume():
        return pygame.mixer.Channel(1).get_volume(), pygame.mixer.Channel(2).get_volume()


class GunSound(SoundEffect):
    def play_sound(self, channel=2):
        pygame.mixer.Channel(1).play(self.effect)

    @staticmethod
    def stop_sound():
        pygame.mixer.Channel(1).stop()


class SpritesSound:
    @staticmethod
    def wall_hit(channel=2):
        SoundEffect(WALL_HIT_SOUND).play_sound(channel)

    @staticmethod
    def sprite_hit(channel=2):
        SoundEffect(SPRITE_HIT_SOUND).play_sound(channel)

    @staticmethod
    def no_ammo(channel=2):
        SoundEffect(NO_AMMO_SOUND).play_sound(channel)

    @staticmethod
    def damage(channel=2):
        SoundEffect(DAMAGE_SOUND).play_sound(channel)

    @staticmethod
    def dead(channel=2):
        SoundEffect(DEAD_SOUND).play_sound(channel)

    @staticmethod
    def get_damage(channel=2):
        SoundEffect(DO_DAMAGE_SOUND).play_sound(channel)

    @staticmethod
    def footstep(channel=2):
        SoundEffect(FOOTSTEP_SOUND).play_sound(channel)
