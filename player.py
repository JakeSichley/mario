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
        self.idle_image = pygame.image.load('images/player/idle.bmp')
        self.big_idle_image = pygame.image.load('images/player/big_idle.bmp')
        self.rect = self.idle_image.get_rect()
        self.y = float(self.rect.y)
        self.x = float(self.rect.x)

        self.vel = pygame.Vector2()
        self.vel.x, self.vel.y = 0, 0
        self.gravity = 0.3
        self.speed = 4
        self.jump_power = 9
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
        self.idle_anim = Timer([self.idle_image])
        self.jump_anim = Timer([pygame.image.load('images/player/jump.bmp')])
        self.slide_anim = Timer([pygame.image.load('images/player/slide.bmp')])
        self.big_idle_anim = Timer([self.big_idle_image])
        self.big_walk_anim = Timer([pygame.image.load('images/player/big_walk1.bmp'),
                                    pygame.image.load('images/player/big_walk2.bmp'),
                                    pygame.image.load('images/player/big_walk3.bmp')])
        self.big_jump_anim = Timer([pygame.image.load('images/player/big_jump.bmp')])
        self.big_slide_anim = Timer([pygame.image.load('images/player/big_slide.bmp')])
        self.current_anim = self.idle_anim

    def update(self, sprites):
        # check invulnerable timer
        if self.invulnerable:
            if self.invuln_timer > 0:
                self.invuln_timer -= pygame.time.Clock().tick()
            else:
                self.invulnerable = False

        # check collision
        self.is_grounded = False
        sprites_hit = pygame.sprite.spritecollide(self, sprites, False)
        if sprites_hit:
            for s in sprites_hit:
                if s.tag == 'item':
                    self.level_up()
                    s.kill()
                if s.tag == 'brick':
                    self.collide_brick(s)
                    # if self.vel.x > 0:
                    #    self.x = sprite.rect.left - self.rect.width
                    #   self.rect.x = int(self.x)
                    # elif self.vel.x < 0:
                    #   self.x = sprite.rect.right
                    #  self.rect.x = int(self.x)
                if s.tag == 'enemy':
                    self.collide_enemy(s)

        self.move()
        self.y += self.vel.y
        if self.camera.out_of_camera(self):
            self.x = -self.camera.rect.x
            self.vel.x = 0
        else:
            self.x += self.vel.x
        self.rect.y = int(self.y)
        self.rect.x = int(self.x)

        self.update_animation()

    def move(self):
        # key inputs
        key_pressed = pygame.key.get_pressed()
        left = key_pressed[K_a] or key_pressed[K_LEFT]
        right = key_pressed[K_d] or key_pressed[K_RIGHT]

        # gravity
        if not self.is_grounded:
            self.vel.y += self.gravity
            if self.vel.y >= 8:
                self.vel.y = 8
        else:
            self.vel.y = 0

        # move
        if left:  # move left
            if self.facing_right:
                self.facing_right = False
            if not self.camera.out_of_camera(self):
                self.vel.x -= 0.1
                if self.vel.x <= -self.speed:
                    self.vel.x = -self.speed
            else:
                self.vel.x = 0
        if right:  # move right
            if not self.facing_right:
                self.facing_right = True
            self.vel.x += 0.1
            if self.vel.x >= self.speed:
                self.vel.x = self.speed
        if not (left or right):
            self.vel.x = 0

    def update_animation(self):
        # set animation
        if self.vel.y != 0:  # jump/fall animation
            self.current_anim = self.jump_anim if self.level == 1 else self.big_jump_anim
        else:
            if self.vel.x != 0:  # walk animation
                self.current_anim = self.walk_anim if self.level == 1 else self.big_walk_anim
            if self.vel.x == 0:
                self.current_anim = self.idle_anim if self.level == 1 else self.big_idle_anim

    def level_up(self):
        if self.level == 1:
            self.level += 1
            bot = self.rect.bottom
            self.current_anim = self.big_idle_anim
            self.rect = self.big_idle_image.get_rect()
            self.rect.x = int(self.x)
            self.rect.bottom = bot
            self.y = float(self.rect.y)

    def get_hit(self):
        if not self.invulnerable:
            if self.level >= 1:
                self.level = 1
                self.current_anim = self.idle_anim
                self.rect = self.idle_image.get_rect()
                self.rect.x = int(self.x)
                self.rect.y = int(self.y)
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

    def collide_brick(self, brick):
        if brick.rect.top <= self.rect.bottom < brick.rect.bottom:
            self.rect.bottom = brick.rect.top + 1
            self.is_grounded = True
            self.vel.y = 0
        if self.vel.y < 0:
            self.rect.top = brick.rect.bottom
            self.vel.y = 0

        self.y = float(self.rect.y)

    def collide_enemy(self, enemy):
        pass

    def draw1(self):
        if self.facing_right:
            image = self.current_anim.imagerect()
        else:
            image = pygame.transform.flip(self.current_anim.imagerect(), True, False)
        self.screen.blit(image, self.camera.apply(self))

    def draw(self):
        self.screen.blit(self.current_anim.imagerect(), self.rect)
