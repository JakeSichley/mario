import pygame
from settings import Settings
import game_functions as gf
from player import Player
from camera import Camera
from hud import HUD
from game_stats import GameStats

FPS = 60


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

    test_box = pygame.Rect(700, 380, 25, 25)

    # Main loop
    game_over = False
    while not game_over:
        gf.check_inputs(player=pc)

        camera.update(pc)
        pc.update()

        # draw
        gf.update_screen(settings=settings, screen=screen)
        pc.draw1(camera)
        pygame.draw.rect(screen, (200, 0, 0), test_box.move(camera.rect.left, camera.rect.top))

        hud.draw()
        pygame.display.update()

        main_clock.tick(FPS)


play()
