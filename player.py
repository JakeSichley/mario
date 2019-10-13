import pygame
from pygame.sprite import Sprite
from pygame.locals import *
from timer import Timer


class Player(Sprite):
    def __init__(self, screen, settings, stats, camera):
        super().__init__()
        self.screen = screen
        self.screen_rect = screen.get_rect()
        self.settings = settings
        self.stats = stats
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

        self.level = 1
        self.dead = False
        self.invulnerable = False
        self.invuln_time = 2000
        self.invuln_timer = self.invuln_time

        # animations
        self.facing_right = True
        self.walk_anim = Timer([pygame.image.load('images/player/walk1.bmp'),
                                pygame.image.load('images/player/walk2.bmp'),
                                pygame.image.load('images/player/walk3.bmp')])
        self.idle_anim = Timer([idle_image])
        self.jump_anim = Timer([pygame.image.load('images/player/jump.bmp')])
        self.current_anim = self.idle_anim

    def update(self):
        # check invulnerable timer
        if self.invulnerable:
            if self.invuln_timer > 0:
                self.invuln_timer -= pygame.time.Clock().tick()
            else:
                self.invulnerable = False

        # check if is grounded
        if self.y + self.rect.height >= self.screen_rect.height:
            self.y = self.screen_rect.height - self.rect.height
            self.is_grounded = True
            self.vel.y = 0
        else:
            self.is_grounded = False

        self.move()

        # update coordinate
        self.y += self.vel.y
        self.x += self.vel.x
        self.rect.y = int(self.y)
        self.rect.x = int(self.x)

    def draw1(self, camera):
        if self.facing_right:
            image = self.current_anim.imagerect()
        else:
            image = pygame.transform.flip(self.current_anim.imagerect(), True, False)
        self.screen.blit(image, camera.apply(self))

    def draw(self):
        self.screen.blit(self.current_anim.imagerect(), self.rect)

    def move(self):
        # key inputs
        key_pressed = pygame.key.get_pressed()
        left = key_pressed[K_a] or key_pressed[K_LEFT]
        right = key_pressed[K_d] or key_pressed[K_RIGHT]
        jump = key_pressed[K_w]

        # gravity
        if not self.is_grounded:
            self.vel.y += self.gravity
            if self.vel.y >= 9:
                self.vel.y = 9

        # move
        if left:  # move left
            if self.facing_right:
                self.facing_right = False
            if not self.camera.out_of_camera(self):
                self.vel.x = -self.speed
            else:
                self.vel.x = 0
        if right:  # move right
            if not self.facing_right:
                self.facing_right = True
            self.vel.x = self.speed
        if not (left or right):
            self.vel.x = 0

        # set animation
        if not self.is_grounded:  # jump/fall animation
            self.current_anim = self.jump_anim
        else:
            if self.vel.x != 0:  # walk animation
                self.current_anim = self.walk_anim
            if self.vel.x == 0:
                self.current_anim = self.idle_anim

    def level_up(self):
        if self.level == 1:
            self.level += 1

    def get_hit(self):
        if not self.invulnerable:
            if self.level >= 1:
                self.level = 1
                self.invulnerable = True
                self.invuln_timer = self.invuln_time
            else:
                self.die()

    def die(self):
        self.stats.lives_left -= 1

    def jump(self):
        if self.is_grounded:
            self.vel.y = -self.jump_power
            self.y += self.vel.y
            self.rect.y = int(self.y)

    def respawn(self):
        self.rect.x = 0
        self.rect.y = 0
        self.dead = False