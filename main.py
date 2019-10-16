import pygame
from settings import Settings
import game_functions as gf
from player import Player
from camera import Camera
from hud import HUD
from game_stats import GameStats
from pygame.sprite import Sprite
from pygame.sprite import Group
from timer import Timer

FPS = 60


class Tile(Sprite):
    def __init__(self, screen, tag, image, x, y):
        super().__init__()
        self.screen = screen
        self.image = image
        self.rect = self.image.get_rect()
        self.tag = tag
        self.rect.x = x
        self.rect.y = y

    def draw(self, camera):
        self.screen.blit(self.image, camera.apply(self))


class Enemy(Sprite):
    def __init__(self, screen, frames, point, x, y):
        super().__init__()
        self.tag = 'enemy'
        self.screen = screen
        self.anim = Timer(frames)
        self.rect = frames[0].get_rect()
        self.rect.x = x
        self.rect.y = y
        self.x = float(self.rect.x)
        self.y = float(self.rect.y)
        self.point = point

    def update(self, player, sprites):
        pass

    def draw(self, camera):
        self.screen.blit(self.anim.imagerect(), camera.apply(self))


class Goomba(Enemy):
    def __init__(self, screen, x, y):
        self.screen = screen
        self.screen_rect = screen.get_rect()
        self.frames = [pygame.image.load('images/enemy/goomba1.bmp'),
                       pygame.image.load('images/enemy/goomba2.bmp')]
        super().__init__(screen=screen, frames=self.frames, point=100, x=x, y=y)

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


def play():
    pygame.init()
    settings = Settings()
    screen = pygame.display.set_mode((settings.scr_width, settings.scr_height), 0, 32)
    pygame.display.set_caption("Mario")
    stats = GameStats()
    main_clock = pygame.time.Clock()
    camera = Camera(settings=settings)
    hud = HUD(screen=screen, settings=settings, stats=stats)
    pc = Player(screen=screen, settings=settings, stats=stats, camera=camera, hud=hud)

    #enemies = Group()
    sprites = Group()
    item_img = pygame.image.load('images/Tile/box.png')
    block_img = pygame.image.load('images/Tile/brick.png')
    flower_img = pygame.image.load('images/Tile/flower.bmp')
    sprites.add(Tile(screen, 'item', item_img, 700, 310))
    sprites.add(Tile(screen, 'item', item_img, 1000, 310))
    for i in range(100):
        sprites.add(Tile(screen, 'brick', block_img, i*16, 400))
    sprites.add(Tile(screen, 'brick', block_img, 800, 310))
    sprites.add(Tile(screen, 'brick', block_img, 1100, 380))
    sprites.add(Tile(screen, 'brick', block_img, 900, 380))
    sprites.add(Tile(screen, 'flower', flower_img, 200, 310))
    sprites.add(Goomba(screen, 950, 300))

    # Main loop
    game_over = False
    while not game_over:
        gf.check_inputs(player=pc)

        camera.update(pc)
        gf.update_player(player=pc, sprites=sprites)
        for e in sprites:
            if e.tag == 'enemy':
                e.update(player=pc, sprites=sprites)

        # draw
        gf.update_screen(settings=settings, screen=screen)
        pc.draw1()
        for s in sprites:
            s.draw(camera)

        hud.draw()
        pygame.display.update()

        main_clock.tick(60)


play()
