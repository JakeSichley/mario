import pygame


class Camera:
    def __init__(self):
        self.rect = pygame.Rect(0, 0, 800, 600)

    def apply(self, target):
        return target.rect.move(self.rect.topleft)

    def update(self, target):
        self.rect.x = -target.rect.x + 400
        # self.rect.y = -target.rect.y + 300