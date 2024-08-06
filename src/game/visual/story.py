import cv2
import pygame
from game.core.config import VIDEO_PATH

class Video:
    def __init__(self, menu):
        pygame.display.set_caption('DOOM')
        self.menu = menu

    def play_video(self):
        cap = cv2.VideoCapture(VIDEO_PATH)
        if not cap.isOpened():
            print(f"Failed to open video file: {VIDEO_PATH}")
            return
        
        success, img = cap.read()
        if not success:
            print("Failed to read the first frame of the video.")
            return

        shape = img.shape[1::-1]
        wn = pygame.display.set_mode(shape)
        if wn is not None:
            clock = pygame.time.Clock()
            pygame.mixer.init()
            pygame.init()
            sounda = pygame.mixer.Sound("src/content/sound/story.mp3")
            sounda.play()
            while success:
                clock.tick(30)
                success, img = cap.read()
                if not success:
                    break
                for event in pygame.event.get():
                    if event.type == pygame.QUIT:
                        success = False
                if img is not None:
                    wn.blit(pygame.image.frombuffer(img.tobytes(), shape, "BGR"), (0, 0))
                    pygame.display.update()
                else:
                    print("Frame is None, skipping...")
        else:
            print("Failed to create display window.")
    
    def back_to_menu(self):
        self.menu.run()
