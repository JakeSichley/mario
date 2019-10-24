from settings import Settings
import game_functions as gf
from player import Player
from camera import Camera
from hud import HUD
from game_stats import GameStats
from enemy import *
from stage_manager import StageManager
from credits import CreditsScreen
from gameover import GameoverScreen
from help import HelpText

FPS = 60


def play():
    pygame.init()
    settings = Settings()
    screen = pygame.display.set_mode((settings.scr_width, settings.scr_height), 0, 32)
    pygame.display.set_caption("Mario")
    stats = GameStats()
    main_clock = pygame.time.Clock()
    cs = CreditsScreen(screen=screen)
    go = GameoverScreen(screen=screen)
    camera = Camera(settings=settings)
    sm = StageManager(screen=screen, settings=settings, stats=stats)
    hud = HUD(screen=screen, settings=settings, stats=stats, stage_manager=sm)
    pc = Player(screen=screen, settings=settings, stats=stats, stage_manager=sm, camera=camera, hud=hud)
    sm.load_stage(stage=stats.current_stage, hud=hud)
    help_text = HelpText(screen=screen, settings=settings)
    pygame.mouse.set_visible(False)

    # Main loop
    while True:
        gf.check_inputs(player=pc)

        if stats.current_stage < 4 and stats.current_stage != -1:
            camera.update(pc)
        if stats.current_stage != -1:
            gf.update_player(player=pc, platforms=sm.platforms, enemies=sm.enemies)
            sm.update(player=pc)

        # draw
        if stats.current_stage != -1:
            screen.fill(settings.bg_color)
            sm.draw(camera)
            pc.draw1()

        if stats.current_stage < 4 and stats.current_stage != -1:
            hud.draw()
            if stats.current_stage == 1:
                help_text.draw(camera)
        elif stats.current_stage == 4:
            cs.draw()
        elif stats.current_stage == -1:
            go.draw()
        pygame.display.update()
        main_clock.tick(60)


play()
