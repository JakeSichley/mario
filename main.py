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


class Mushroom(Sprite):
    def __init__(self, screen, x, y):
        super().__init__()
        self.screen = screen
        self.image = pygame.image.load('images/Tile/box.png')
        self.rect = self.image.get_rect()
        self.tag = 'item'
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

    test_box = Mushroom(screen, 700, 350)
    sprites = Group()
    sprites.add(test_box)

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
