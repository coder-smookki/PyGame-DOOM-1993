import pygame
from game.core.config import *
from game.map.map import create_map, create_minimap
from game.visual.menu import MainMenu, show_info
from game.map.mode import Modes
from game.core.player import Player
from game.core.render import Render, wall_textures
from game.visual.result_window import Win, Losing
from game.sound.sound import Music
from game.core.sprite import create_sprites, sprites_update, is_win
from game.visual.stats import Stats
from game.utils.utils import is_game_over
from game.core.weapon import Weapon


"""
Самая главная часть со связками всех файлов и их применение и от цифрация в окно
"""


class Game:
    def __init__(self):
        self._screen = pygame.display.set_mode(SCREEN_SIZE, pygame.DOUBLEBUF)
        self._minimap_screen = pygame.Surface((MAP_SIZE[0] * MAP_TILE, MAP_SIZE[1] * MAP_TILE))
        self._clock = pygame.time.Clock()
        self._caption = WINDOW_NAME
        self._sprites = list()

    def _pre_init(self):
        pygame.display.set_caption('DOOM')
        self._menu = MainMenu(self._screen, self._clock)
        self._losing = Losing(self._screen, self._clock)
        self._win = Win(self._screen, self._clock)

    def run(self):
        self._pre_init()
        self._menu.run()
        self._init()
        self._play_theme()
        self._config()
        self._update()
        self._finish()

    def _init(self):
        self._weapons = [
            Weapon(self._screen, 'Gun1', (500, 450), SHOTGUN_ANIMATION_FRAME_COUNTS, SHOTGUN, SHOTGUN_AMMO,
                   SHOTGUN_DAMAGE, SHOTGUN_MAX_DISTANCE),
            Weapon(self._screen, 'Gun2', (400, 400), PISTOL_ANIMATION_FRAME_COUNTS, PISTOL, PISTOL_AMMO, PISTOL_DAMAGE,
                   PISTOL_MAX_DISTANCE),
            Weapon(self._screen, 'Gun3', (350, 300), RIFLE_ANIMATION_FRAME_COUNTS, RIFLE, RIFLE_AMMO, RIFLE_DAMAGE,
                   RIFLE_MAX_DISTANCE)]

        self._sprites = create_sprites(self._menu.chosen_level)
        self._stats = Stats()
        self._player = Player(TILE * 2 - TILE // 2, TILE * 2 - TILE // 2, self._weapons, self._sprites, self._stats)
        self._render = Render(self._screen, self._player, self._minimap_screen, self._sprites, self._menu.chosen_level)
        self._running = True
        self._is_game_end = False

        create_map(self._menu.chosen_level)
        create_minimap(self._menu.chosen_level)
        pygame.init()

    def _config(self):
        pygame.display.set_caption(self._caption)
        pygame.mouse.set_visible(False)

    def _respawn_arcade_sprites(self):
        self._menu.arcade_class.spawn(SPRITES_COUNT_TO_SPAWN_IN_ARCADE)
        sprites = create_sprites(self._menu.arcade_class.get_map())

        self._render.sprites = sprites
        self._player.sprites = sprites
        self._sprites = sprites

    def _update(self):
        while self._running:
            self._screen.fill(SKYBLUE)
            self._clock.tick(FPS)

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    self._running = False
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_ESCAPE:
                        self.run()
                if self._is_game_end:
                    if event.type in [pygame.MOUSEBUTTONDOWN, pygame.KEYDOWN]:
                        self._running = False
                if event.type == pygame.MOUSEBUTTONDOWN and not self._is_game_end:
                    self._player.on_mouse_down(event)

            if self._is_all_arcade_sprites_killed():
                self._respawn_arcade_sprites()

            self._is_game_end = self.is_game_end()
            if self._is_game_end:
                total_time = self._stats.total_time()
                kills_count = self._stats.get_kills()
                if is_game_over(self._player):
                    self._player.dead()
                    self._losing.run(total_time, kills_count)
                    self.run()
                elif is_win(self._sprites):
                    self._win.run(total_time, kills_count)
                    self.run()
            else:
                self._player.update()
                self._render.render()
                sprites_update(self._sprites, self._player)
                show_info(self._screen, self._player)

            pygame.display.set_caption('FPS: ' + str(int(self._clock.get_fps())))
            pygame.display.flip()

    def _is_all_arcade_sprites_killed(self):
        return self._menu.mode == Modes.ARCADE and is_win(self._sprites)

    def is_game_end(self):
        return is_game_over(self._player) or is_win(self._sprites)

    @staticmethod
    def _finish():
        pygame.quit()

    @staticmethod
    def _play_theme():
        theme = Music()
        theme.play_music()


if __name__ == '__main__':
    game = Game()
    game.run()
