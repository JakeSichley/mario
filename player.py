import pygame
from pygame.sprite import Sprite
from pygame.locals import *
from timer import Timer


class Player(Sprite):
    def __init__(self, screen, camera):
        super().__init__()
        self.screen = screen
        self.camera = camera
        idle_image = pygame.image.load('images/player/idle.bmp')
        self.rect = idle_image.get_rect()
        self.y = float(self.rect.y)
        self.x = float(self.rect.x)

        self.vel = pygame.Vector2()
        self.vel.x, self.vel.y = 0, 0
        self.gravity = 0.3
        self.speed = 4
        self.jump_power = 10
        self.is_grounded = False

        # animations
        self.walk_anim = Timer([pygame.image.load('images/player/walk1.bmp'),
                                pygame.image.load('images/player/walk3.bmp')])
        self.idle_anim = Timer([idle_image])
        self.current_anim = self.idle_anim

    def update(self):
        self.move()

    def draw1(self, camera):
        self.screen.blit(self.current_anim.imagerect(), camera.apply(self))

    def draw(self):
        self.screen.blit(self.current_anim.imagerect(), self.rect)

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
            if not self.camera.out_of_camera(self):
                self.vel.x = -self.speed
            else:
                self.vel.x = 0
        if right:  # move right
            self.vel.x = self.speed
        if not (left or right):
            self.vel.x = 0

        if self.vel.x > 0 or self.vel.x < 0:
            self.current_anim = self.walk_anim
        if self.vel.x == 0:
            self.current_anim = self.idle_anim

        self.y += self.vel.y
        self.x += self.vel.x
        self.rect.y = int(self.y)
        self.rect.x = int(self.x)
