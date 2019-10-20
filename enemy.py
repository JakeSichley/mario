import pygame
from pygame.sprite import Sprite
from timer import Timer


class Enemy(Sprite):
    def __init__(self, screen, frames, point, left, bot):
        super().__init__()
        self.tag = 'enemy'
        self.screen = screen
        self.anim = Timer(frames)
        self.rect = frames[0].get_rect()
        self.rect.x = left
        self.rect.bottom = bot
        self.x = float(self.rect.x)
        self.y = float(self.rect.y)
        self.point = point

    def set_pos(self, left, bot):
        self.rect.x = left
        self.rect.y = bot
        self.x = float(self.rect.x)
        self.y = float(self.rect.y)

    def die(self):
        self.kill()

    def update(self, player, sprites):
        pass

    def draw(self, camera):
        self.screen.blit(self.anim.imagerect(), camera.apply(self))


class Goomba(Enemy):
    def __init__(self, screen, left, bot):
        self.screen = screen
        self.screen_rect = screen.get_rect()
        self.frames = [pygame.image.load('images/enemy/goomba1.bmp'),
                       pygame.image.load('images/enemy/goomba2.bmp')]
        super().__init__(screen=screen, frames=self.frames, point=100, left=left, bot=bot)

        self.is_grounded = False
        self.chasing_player = False
        self.speed = 1
        self.gravity = 0.3
        self.vely = 0

    def update(self, player, sprites):
        # check falling off
        if self.rect.y > self.screen_rect.height:
            self.kill()

        # gravity
        if not self.is_grounded:
            self.vely += self.gravity
            if self.vely >= 6:
                self.vely = 6
        else:
            if self.rect.x - player.rect.x < 350:
                self.chasing_player = True
            if self.chasing_player:
                self.x -= self.speed

        self.y += self.vely
        self.rect.x = int(self.x)
        self.rect.y = int(self.y)

        # collision
        self.is_grounded = False
        sprites_hit = pygame.sprite.spritecollide(self, sprites, False)
        if sprites_hit:
            for s in sprites_hit:
                if s.tag == 'brick':
                    c = self.rect.clip(s.rect)  # collision rect
                    if c.width >= c.height:
                        if self.vely >= 0:
                            self.rect.bottom = s.rect.top + 1
                            self.y = float(self.rect.y)
                            self.is_grounded = True
                            self.vely = 0
                    if c.width < c.height:
                        self.speed *= -1
