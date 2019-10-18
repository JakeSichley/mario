import pygame
from settings import Settings
import game_functions as gf
from player import Player
from camera import Camera
from hud import HUD
from game_stats import GameStats
from pygame.sprite import Group
from tile import *
from enemy import *
from stage_manager import StageManager

FPS = 60


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
    sm = StageManager(screen=screen, stats=stats)
    sm.load_stage(stage=stats.current_stage)

    # Main loop
    game_over = False
    while not game_over:
        gf.check_inputs(player=pc)

        camera.update(pc)
        gf.update_player(player=pc, platforms=sm.platforms, enemies=sm.enemies)
        sm.update(player=pc)

        # draw
        gf.update_screen(settings=settings, screen=screen)
        pc.draw1()
        sm.draw(camera)

        hud.draw()
        pygame.display.update()

        main_clock.tick(60)


play()
