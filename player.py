import pygame
from pygame.sprite import Sprite
from pygame.locals import *
from timer import Timer


class Player(Sprite):
    def __init__(self, screen):
        super().__init__()
        self.screen = screen
        self.rect = pygame.Rect(100, 100, 25, 25)
        self.y = float(self.rect.y)
        self.x = float(self.rect.x)

        self.vel = pygame.Vector2()
        self.vel.x, self.vel.y = 0, 0
        self.gravity = 0.3
        self.speed = 4
        self.jump_power = 10
        self.is_grounded = False

    def update(self):
        self.move()

    def draw(self, camera):
        pygame.draw.rect(self.screen, (250, 250, 250), camera.apply(self))

    def draw(self):
        pygame.draw.rect(self.screen, (250, 250, 250), self.rect)

    def move(self):
        key_pressed = pygame.key.get_pressed()
        left = key_pressed[K_a] or key_pressed[K_LEFT]
        right = key_pressed[K_d] or key_pressed[K_RIGHT]
        jump = key_pressed[K_SPACE]

        if self.y + self.rect.height > 600:
            self.y = 600 - self.rect.height
            self.is_grounded = True
            self.vel.y = 0
        else:
            self.is_grounded = False

        if not self.is_grounded:
            self.vel.y += self.gravity
            if self.vel.y >= 10:
                self.vel.y = 10
        if jump and self.is_grounded:
            self.vel.y = -self.jump_power
        if left:  # move left
            self.vel.x = -self.speed
        if right:  # move right
            self.vel.x = self.speed
        if not (left or right):
            self.vel.x = 0

        self.y += self.vel.y
        self.x += self.vel.x
        self.rect.y = int(self.y)
        self.rect.x = int(self.x)
