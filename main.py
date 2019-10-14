import pygame
from settings import Settings
import game_functions as gf
from player import Player
from camera import Camera
from hud import HUD
from game_stats import GameStats
from pygame.sprite import Sprite
from pygame.sprite import Group

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


def play():
    pygame.init()
    settings = Settings()
    screen = pygame.display.set_mode((settings.scr_width, settings.scr_height), 0, 32)
    pygame.display.set_caption("Mario")
    stats = GameStats()
    main_clock = pygame.time.Clock()
    camera = Camera(settings=settings)
    pc = Player(screen=screen, settings=settings, stats=stats, camera=camera)
    hud = HUD(screen=screen, settings=settings, stats=stats)

    sprites = Group()
    item_img = pygame.image.load('images/Tile/box.png')
    block_img = pygame.image.load('images/Tile/brick.png')
    sprites.add(Tile(screen, 'item', item_img, 700, 310))
    sprites.add(Tile(screen, 'item', item_img, 1000, 310))
    for i in range(100):
        sprites.add(Tile(screen, 'brick', block_img, i*16, 400))
    sprites.add(Tile(screen, 'brick', block_img, 800, 310))


    # Main loop
    game_over = False
    while not game_over:
        gf.check_inputs(player=pc)

        camera.update(pc)
        gf.update_player(player=pc, sprites=sprites)

        # draw
        gf.update_screen(settings=settings, screen=screen)
        pc.draw1()
        for s in sprites:
            s.draw(camera)

        hud.draw()
        pygame.display.update()

        main_clock.tick(FPS)


play()
