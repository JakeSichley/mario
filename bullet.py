import pygame
from pygame.sprite import Sprite
from timer import Timer


class Bullet(Sprite):
    def __init__(self, screen, direction):
        super().__init__()
        self.screen = screen
        self.speed = 6
        self.direction = direction
        self.anim = Timer([pygame.image.load('images/player/fire1.bmp'),
                           pygame.image.load('images/player/fire2.bmp'),
                           pygame.image.load('images/player/fire3.bmp'),
                           pygame.image.load('images/player/fire4.bmp')])
        self.rect = self.anim.frames[0].get_rect()

    def draw(self, camera):
        self.screen.blit(self.anim.imagerect(), camera.apply(self))
