import pygame
from pygame.sprite import Sprite


class Tile(Sprite):
    def __init__(self, screen, tag, image, x, y):
        super().__init__()
        self.screen = screen
        self.image = image
        self.rect = self.image.get_rect()
        self.tag = tag
        self.rect.x = x
        self.rect.y = y

    def draw(self, camera):
        self.screen.blit(self.image, camera.apply(self))