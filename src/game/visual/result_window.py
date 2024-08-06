import collections
import random
import sys
import pygame
from game.core.config import *
from game.visual.load_image import load_image
from game.visual.menu import button

"""
Окно с результатом и концовка
"""

font = pygame.font.Font(FONT, 200)
font_res = pygame.font.Font(FONT, 75)
font_back = pygame.font.Font(FONT, 30)


def show_res(screen, time, kills):
    button(screen, TIME_NAME + str(int(time)) + '  ' + SEC, RED, TIME_POS, TIME_SIZE[0], TIME_SIZE[1], font_res)
    button(screen, KILLS_NAME + str(kills), BLUE, KILLS_POS, TIME_SIZE[0], TIME_SIZE[1], font_res)


class EndMenu:
    def __init__(self, screen, clock):
        self.screen = screen
        self.clock = clock
        self.animation_count = 0
        self.lost_frames_count = 0
        self.running = True
        self.animation_list = collections.deque()
        self.end_message = str()

    def run(self, total_time, kills):
        pygame.mouse.set_visible(True)
        while self.running:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.display.quit()
                    sys.exit()
                if event.type == pygame.MOUSEBUTTONDOWN:
                    pass
            self.screen.fill(BLACK)
            self._draw(total_time, kills)
            self.back_to_menu()

            pygame.display.flip()
            self.clock.tick(20)

    def _draw(self, total_time, kills_count):
        shot_sprite = self.animation_list[0]
        self.screen.blit(shot_sprite, PICTURE_POS)
        self.animation_count += 1
        if self.animation_count == WEAPON_ANIMATION_SPEED:
            self.animation_list.rotate(-1)
            self.animation_count = 0
            self.lost_frames_count += 1
        color = random.randrange(0, 255)
        button(self.screen, self.end_message, (color, color, color), SENT_POS, SENT_SIZE[0], SENT_SIZE[1], font)
        show_res(self.screen, total_time, kills_count)

    def back_to_menu(self):
        self.btn_back, self.back = button(self.screen, BACK_TO_MENU, WHITE, BACK_TO_MENU_POS, BACK_TO_MENU_SIZE[0],
                                          BACK_TO_MENU_SIZE[1],
                                          font_back)
        mouse_pos = pygame.mouse.get_pos()
        mouse_click = pygame.mouse.get_pressed()
        if self.btn_back.collidepoint(mouse_pos):
            button(self.screen, BACK_TO_MENU, RED, BACK_TO_MENU_POS, BACK_TO_MENU_SIZE[0], BACK_TO_MENU_SIZE[1],
                   font_back)
            if mouse_click[0]:
                self.running = False


class Win(EndMenu):
    def __init__(self, screen, clock):
        super().__init__(screen, clock)
        self.animation_list = self._load_picture(SKELETON_AMOUNT)
        self.end_message = WON

    @staticmethod
    def _load_picture(pictures_amount):
        animation_list = [pygame.transform.scale(load_image(TEXTURES_PATH, f'win/{i}.gif'), PICTURE_SIZE) for i in
                          range(pictures_amount)]
        return collections.deque(animation_list)


class Losing(EndMenu):
    def __init__(self, screen, clock):
        super().__init__(screen, clock)
        self.animation_list = self._load_picture(SKULL_AMOUNT)
        self.end_message = LOSE

    @staticmethod
    def _load_picture(pictures_amount):
        animation_list = [pygame.transform.scale(load_image(TEXTURES_PATH, f'losing/{i}.gif'), PICTURE_SIZE) for i in
                          range(pictures_amount)]
        return collections.deque(animation_list)
