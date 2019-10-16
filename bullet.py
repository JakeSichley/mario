import pygame
from pygame.sprite import Sprite
from timer import Timer


class Bullet(Sprite):
    def __init__(self, screen, direction, x, y):
        super().__init__()
        self.screen = screen
        self.speed = 6
        self.max_distace = 500
        self.traveled_distance = 0
        self.direction = direction
        self.anim = Timer([pygame.image.load('images/player/fire1.bmp'),
                           pygame.image.load('images/player/fire2.bmp'),
                           pygame.image.load('images/player/fire3.bmp'),
                           pygame.image.load('images/player/fire4.bmp')])
        self.rect = self.anim.frames[0].get_rect()
        self.rect.x = x
        self.rect.y = y
        self.x = float(self.rect.x)

    def update(self, sprites):
        if self.traveled_distance >= self.max_distace:
            self.kill()
        else:
            self.x += (self.direction * self.speed)
            self.traveled_distance += self.speed
            self.rect.x = int(self.x)

            # check collision
            hit = pygame.sprite.spritecollideany(self, sprites)
            if hit:
                if hit.tag == 'brick':
                    self.kill()
                if hit.tag == 'enemy':
                    self.kill()
                    hit.kill()

    def draw(self, camera):
        self.screen.blit(self.anim.imagerect(), camera.apply(self))
