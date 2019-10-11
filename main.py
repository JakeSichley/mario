import pygame
import sys
from pygame.locals import *
from settings import Settings
import game_functions as gf
from player import Player
from camera import Camera

FPS = 60


def play():
    pygame.init()
    screen = pygame.display.set_mode((800, 600), 0, 32)
    pygame.display.set_caption("Mario")
    settings = Settings()
    main_clock = pygame.time.Clock()
    camera = Camera()
    pc = Player(screen, camera)

    test_box = pygame.Rect(700, 500, 25, 25)

    # Main loop
    game_over = False
    while not game_over:
        gf.check_inputs(player=pc)

        camera.update(pc)
        pc.update()

        # draw
        gf.update_screen(settings=settings, screen=screen)
        pc.draw1(camera)

        pygame.draw.rect(screen, (200, 0, 0), test_box.move(camera.rect.topleft))
        pygame.display.update()

        main_clock.tick(FPS)


play()
