import cv2
import pygame
from config import VIDEO_PATH

"""
Принцип работы кнопки story, где идёт кастцена
"""

class Video:
    def __init__(self, menu):
        pygame.display.set_caption('DOOM')
        self.menu = menu


    def play_video(self):
        cap = cv2.VideoCapture(VIDEO_PATH)
        success, img = cap.read()
        shape = img.shape[1::-1]
        wn = pygame.display.set_mode(shape)
        clock = pygame.time.Clock()
        pygame.mixer.init()
        pygame.init()
        sounda = pygame.mixer.Sound("sound/story.mp3")
        sounda.play()
        while success:
            clock.tick(120)
            success, img = cap.read()
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    success = False
            wn.blit(pygame.image.frombuffer(img.tobytes(), shape, "BGR"), (0, 0))
            pygame.display.update()

    def back_to_menu(self):
        self.menu.run()
