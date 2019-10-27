import pygame
from pygame.sprite import Sprite


class Tile(Sprite):
    def __init__(self, screen, tag, image, left, bot):
        super().__init__()
        self.screen = screen
        self.image = image
        self.rect = self.image.get_rect()
        self.tag = tag
        self.rect.x = left
        self.rect.bottom = bot

    def update(self):
        pass

    def draw(self, camera):
        self.screen.blit(self.image, camera.apply(self))


class PopupCoin(Tile):
    def __init__(self, screen, tag, image, left, bot):
        super().__init__(screen, tag, image, left, bot)
        self.max_distance = 16
        self.travel_distance = 0
        self.y = float(self.rect.y)

    def update(self):
        self.y -= 1
        self.travel_distance += 1
        self.rect.y = int(self.y)
        if self.travel_distance >= self.max_distance:
            self.kill()