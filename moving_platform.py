import pygame
from pygame.sprite import Sprite


class MovingPlatform(Sprite):
    def __init__(self, screen, tag, left, bottom, direction, mode):
        super().__init__()
        self.screen = screen
        self.screen_rect = screen.get_rect()
        self.tag = tag
        self.mode = mode
        self.image = pygame.image.load('images/Tile/moving_platform.png')
        self.rect = self.image.get_rect()
        self.rect.x = left
        self.rect.bottom = bottom
        self.direction = direction

    def update(self, sprites):
        if self.mode == 'vertical':
            if self.rect.centery > self.screen_rect.bottom:
                self.rect.bottom = 10
            if self.rect.centery < 0:
                self.rect.bottom = self.screen_rect.bottom
            self.rect.bottom += self.direction
        if self.mode == 'horizontal':
            self.rect.x += self.direction

    def draw(self, camera):
        self.screen.blit(self.image, camera.apply(self))
