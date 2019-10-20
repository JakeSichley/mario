import pygame
from pygame.sprite import Sprite
from pygame.locals import *
from timer import Timer
from bullet import Bullet
from pygame.sprite import Group


class Player(Sprite):
    def __init__(self, screen, settings, stats, stage_manager, camera, hud):
        super().__init__()
        self.screen = screen
        self.screen_rect = screen.get_rect()
        self.settings = settings
        self.stats = stats
        self.sm = stage_manager
        self.camera = camera
        self.hud = hud
        self.bullets = Group()
        self.idle_image = pygame.image.load('images/player/idle.bmp')
        self.big_idle_image = pygame.image.load('images/player/big_idle.bmp')
        self.big_crouch_image = pygame.image.load('images/player/big_crouch.bmp')
        self.rect = self.idle_image.get_rect()
        self.y = float(self.rect.y)
        self.x = float(self.rect.x)

        # movement variables
        self.vel = pygame.Vector2()
        self.vel.x, self.vel.y = 0, 0
        self.gravity = 0.3
        self.max_gravity = 8
        self.max_water_gravity = 5
        self.speed = 4
        self.jump_power = 9
        self.swim_power = 5
        self.is_grounded = False
        self.is_sliding = False
        self.is_crouching = False
        self.is_firing = False

        # player's states variables
        self.level = 1  # 1 = small, 2 = big, 3 = fire
        self.dead = False
        self.invulnerable = False
        self.invuln_time = 1500
        self.invuln_timer = self.invuln_time

        # animations
        self.facing_right = True
        self.die_anim = Timer([pygame.image.load('images/player/die.bmp')])
        # small
        self.walk_anim = Timer([pygame.image.load('images/player/walk1.bmp'),
                                pygame.image.load('images/player/walk2.bmp'),
                                pygame.image.load('images/player/walk3.bmp')])
        self.idle_anim = Timer([self.idle_image])
        self.jump_anim = Timer([pygame.image.load('images/player/jump.bmp')])
        self.slide_anim = Timer([pygame.image.load('images/player/slide.bmp')])
        self.swim_anim = Timer([pygame.image.load('images/player/swim1.bmp'),
                                pygame.image.load('images/player/swim2.bmp'),
                                pygame.image.load('images/player/swim3.bmp'),
                                pygame.image.load('images/player/swim4.bmp')])
        # big
        self.big_idle_anim = Timer([self.big_idle_image])
        self.big_walk_anim = Timer([pygame.image.load('images/player/big_walk1.bmp'),
                                    pygame.image.load('images/player/big_walk2.bmp'),
                                    pygame.image.load('images/player/big_walk3.bmp')])
        self.big_jump_anim = Timer([pygame.image.load('images/player/big_jump.bmp')])
        self.big_slide_anim = Timer([pygame.image.load('images/player/big_slide.bmp')])
        self.big_crouch_anim = Timer([self.big_crouch_image])
        self.big_swim_anim = Timer([pygame.image.load('images/player/big_swim1.bmp'),
                                    pygame.image.load('images/player/big_swim2.bmp'),
                                    pygame.image.load('images/player/big_swim3.bmp'),
                                    pygame.image.load('images/player/big_swim4.bmp'),
                                    pygame.image.load('images/player/big_swim5.bmp'),
                                    pygame.image.load('images/player/big_swim6.bmp')])
        # fire
        self.fire_idle_anim = Timer([pygame.image.load('images/player/fire_idle.bmp')])
        self.fire_walk_anim = Timer([pygame.image.load('images/player/fire_walk1.bmp'),
                                    pygame.image.load('images/player/fire_walk2.bmp'),
                                    pygame.image.load('images/player/fire_walk3.bmp')])
        self.fire_jump_anim = Timer([pygame.image.load('images/player/fire_jump.bmp')])
        self.fire_slide_anim = Timer([pygame.image.load('images/player/fire_slide.bmp')])
        self.fire_crouch_anim = Timer([pygame.image.load('images/player/fire_crouch.bmp')])
        self.fire_throw_anim = Timer([pygame.image.load('images/player/fire_throw.bmp')],
                                     wait=150, step=0, looponce=True)
        self.fire_swim_anim = Timer([pygame.image.load('images/player/fire_swim1.bmp'),
                                     pygame.image.load('images/player/fire_swim2.bmp'),
                                     pygame.image.load('images/player/fire_swim3.bmp'),
                                     pygame.image.load('images/player/fire_swim4.bmp'),
                                     pygame.image.load('images/player/fire_swim5.bmp'),
                                     pygame.image.load('images/player/fire_swim6.bmp')])
        self.current_anim = self.idle_anim

    def update(self, platforms, enemies):
        # check falling off:
        if self.rect.y + self.camera.rect.y > self.screen_rect.height:
            if not self.dead:
                self.die()
            else:
                self.respawn()

        # check invulnerable timer
        if self.invulnerable:
            if pygame.time.get_ticks() - self.invuln_timer > self.invuln_time:
                self.invulnerable = False

        # check collision
        self.is_grounded = False
        if not self.dead:
            sprites_hit = pygame.sprite.spritecollide(self, platforms, False)
            if sprites_hit:
                for s in sprites_hit:
                    if s.tag == 'item':
                        if self.level < 2:
                            self.level_up(2)
                        s.kill()
                    if s.tag == 'flower':
                        self.level_up(3)
                        s.kill()
                    if s.tag == 'brick':
                        self.collide_brick(s)
                    if s.tag == 'win':
                        self.stats.current_stage += 1
                        self.sm.load_stage(self.stats.current_stage)
                        self.reset()
            # check collision with enemies
            enemies_hit = pygame.sprite.spritecollide(self, enemies, False)
            if enemies_hit:
                for e in enemies_hit:
                    self.get_hit()

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

        # update bullets
        for b in self.bullets:
            b.update(platforms, enemies)

    def move(self):
        # key inputs
        key_pressed = pygame.key.get_pressed()
        left = key_pressed[K_a] or key_pressed[K_LEFT]
        right = key_pressed[K_d] or key_pressed[K_RIGHT]
        crouch = key_pressed[K_s] or key_pressed[K_DOWN]

        # gravity
        if not self.is_grounded:
            self.vel.y += self.gravity
            if self.stats.current_stage == 2:
                if self.vel.y >= self.max_water_gravity:
                    self.vel.y = self.max_water_gravity
            else:
                if self.vel.y >= self.max_gravity:
                    self.vel.y = self.max_gravity
        else:
            self.vel.y = 0

        if not self.dead:
            # crouch
            if self.level > 1:
                if self.is_grounded:
                    self.is_crouching = crouch
                else:
                    self.is_crouching = crouch and self.is_crouching

                if self.is_crouching:
                    self.change_rect(self.big_crouch_image.get_rect())
                else:
                    self.change_rect(self.big_idle_image.get_rect())
            # move
            if not self.is_crouching:
                if left:  # move left
                    if self.vel.x > 0:
                        self.is_sliding = True
                    else:
                        self.is_sliding = False

                    if self.facing_right:
                        self.facing_right = not self.facing_right
                    if not self.camera.out_of_camera(self):
                        self.vel.x -= 0.1
                        if self.vel.x <= -self.speed:
                            self.vel.x = -self.speed
                    else:
                        self.vel.x = 0
                if right:  # move right
                    if self.vel.x < 0:
                        self.is_sliding = True
                    else:
                        self.is_sliding = False

                    if not self.facing_right:
                        self.facing_right = not self.facing_right
                    self.vel.x += 0.1
                    if self.vel.x >= self.speed:
                        self.vel.x = self.speed
            if not (left or right) or self.is_crouching:
                self.is_sliding = False
                if self.vel.x > 0:
                    self.vel.x -= 0.1
                    if self.vel.x <= 0:
                        self.vel.x = 0
                elif self.vel.x < 0:
                    self.vel.x += 0.1
                    if self.vel.x >= 0:
                        self.vel.x = 0

    def update_animation(self):
        if self.dead:
            self.current_anim = self.die_anim
            return

        if self.is_firing:
            if self.current_anim.finished:
                self.is_firing = False
            else:
                return

        if self.is_crouching:  # crouch
            if self.level == 2:
                self.current_anim = self.big_crouch_anim
            elif self.level == 3:
                self.current_anim = self.fire_crouch_anim
        else:
            if self.vel.y != 0:  # jump/fall animation
                if self.level == 1:
                    if self.stats.current_stage == 2:
                        self.current_anim = self.swim_anim
                    else:
                        self.current_anim = self.jump_anim
                elif self.level == 2:
                    if self.stats.current_stage == 2:
                        self.current_anim = self.big_swim_anim
                    else:
                        self.current_anim = self.big_jump_anim
                else:
                    if self.stats.current_stage == 2:
                        self.current_anim = self.fire_swim_anim
                    else:
                        self.current_anim = self.fire_jump_anim
            else:
                if self.is_sliding:  # slide animation
                    if self.level == 1:
                        self.current_anim = self.slide_anim
                    elif self.level == 2:
                        self.current_anim = self.big_slide_anim
                    else:
                        self.current_anim = self.fire_slide_anim
                else:
                    if self.vel.x != 0:  # walk animation
                        if self.level == 1:
                            self.current_anim = self.walk_anim
                        elif self.level == 2:
                            self.current_anim = self.big_walk_anim
                        else:
                            self.current_anim = self.fire_walk_anim
                    if self.vel.x == 0:  # idle animation
                        if self.level == 1:
                            self.current_anim = self.idle_anim
                        elif self.level == 2:
                            self.current_anim = self.big_idle_anim
                        else:
                            self.current_anim = self.fire_idle_anim

    def level_up(self, new_level):
        self.level = new_level
        if self.level == 2:
            self.change_rect(self.big_idle_image.get_rect())
        if self.level >= 3:
            self.change_rect(self.big_idle_image.get_rect())

    def change_rect(self, new_rect):
        bot = self.rect.bottom
        self.rect = new_rect
        self.rect.x = int(self.x)
        self.rect.bottom = bot
        self.y = float(self.rect.y)

    def get_hit(self):
        if not self.invulnerable:
            if self.level > 1:
                self.level = 1
                self.change_rect(self.idle_image.get_rect())
                self.invulnerable = True
                self.invuln_timer = pygame.time.get_ticks()
            else:
                self.die()

    def die(self):
        self.dead = True
        self.invulnerable = False
        self.bullets.empty()
        self.vel.x = 0
        self.vel.y = -12
        self.is_grounded = False
        self.y += self.vel.y
        self.rect.y = int(self.y)

    def fire(self):
        if self.level == 3:
            if len(self.bullets) < self.settings.bullet_limit:
                if self.facing_right:
                    d = 1
                    x = self.rect.right
                else:
                    d = -1
                    x = self.rect.left
                y = self.rect.centery
                self.bullets.add(Bullet(screen=self.screen, direction=d, x=x, y=y))
                if not self.is_crouching:
                    self.is_firing = True
                    self.fire_throw_anim.reset()
                    self.current_anim = self.fire_throw_anim

    def jump(self):
        jump_power = self.jump_power
        if self.stats.current_stage == 2:
            jump_power = self.swim_power
        self.vel.y = -jump_power
        self.y += self.vel.y
        self.rect.y = int(self.y)

    def reset(self):
        self.camera.reset()
        self.rect.x = self.rect.y = 0
        self.x = float(self.rect.x)
        self.y = float(self.rect.y)
        self.vel.x = self.vel.y = 0
        self.dead = False

    def respawn(self):
        if self.stats.lives_left > 0:
            self.stats.lives_left -= 1
            self.level = 1
            self.change_rect(self.idle_image.get_rect())
            self.hud.prep_lives()
            self.reset()
            self.sm.reset()
        #else:
            #gameover

    def collide_brick(self, brick):
        c = self.rect.clip(brick.rect)  # collision rect
        if c.width >= c.height:
            if self.vel.y >= 0 and self.rect.top < brick.rect.top:
                self.rect.bottom = brick.rect.top + 1
                self.y = float(self.rect.y)
                self.is_grounded = True
                self.vel.y = 0
            if self.vel.y < 0:
                self.rect.top = brick.rect.bottom
                self.y = float(self.rect.y)
                self.vel.y = 0
                if brick.tag == 'brick' and self.level > 1:
                    brick.kill()
                    print('brick broken')
        if c.width < c.height:
            if self.rect.right > brick.rect.left > self.rect.left:
                self.vel.x = 0
                self.rect.right = brick.rect.left
                self.x = float(self.rect.x)
            elif self.rect.left < brick.rect.right < self.rect.right:
                self.vel.x = 0
                self.rect.left = brick.rect.right
                self.x = float(self.rect.x)

    def collide_enemy(self, enemy):
        self.get_hit()

    def draw1(self):
        if self.facing_right:
            image = self.current_anim.imagerect()
        else:
            image = pygame.transform.flip(self.current_anim.imagerect(), True, False)
        self.screen.blit(image, self.camera.apply(self))

        # draw bullets
        for b in self.bullets:
            b.draw(self.camera)

    def draw(self):
        self.screen.blit(self.current_anim.imagerect(), self.rect)
