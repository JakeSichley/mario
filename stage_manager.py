import pygame
from tile import *
from enemy import *
from pygame.sprite import Group


class StageManager:
    def __init__(self, screen, settings, stats):
        self.stats = stats
        self.settings = settings
        self.screen = screen
        self.enemies = Group()
        self.platforms = Group()
        self.time_limit = 401000  # 401s
        self.time_start = 0
        self.time_elapsed = 0
        self.bgm = pygame.mixer.Sound('audio/overworld.ogg')

    def update(self, player):
        # time over
        if self.stats.current_stage != 4:
            self.time_elapsed = pygame.time.get_ticks() - self.time_start
            if self.time_elapsed >= self.time_limit:
                if not player.dead and not player.stage_clear:
                    player.die()

        for e in self.enemies:
            e.update(player, self.platforms)

    def draw(self, camera):
        for p in self.platforms:
            p.draw(camera)
        for e in self.enemies:
            e.draw(camera)

    def load_stage(self, stage, hud):  # character's position in txt file is left bot coordinate
        self.enemies.empty()
        self.platforms.empty()
        self.time_start = pygame.time.get_ticks()
        self.time_elapsed = 0
        # set up bg_color
        if stage in [1, 3]:
            self.settings.bg_color = (150, 150, 250)
        if stage in [2]:
            self.settings.bg_color = (100, 100, 255)
        if stage in [-1, 4]:
            self.settings.bg_color = (0, 0, 0)

        if stage == 1:
            # set up tile set
            tile_dict = {'b': ['brick', pygame.image.load('images/Tile/brick.png')],
                         'i': ['item', pygame.image.load('images/Tile/box.png')],
                         'f': ['flower', pygame.image.load('images/Tile/flower.bmp')],
                         'w': ['win', pygame.image.load('images/Tile/flag.png')]}
            self.load('stage/stage1.txt', tile_dict)  # build map form txt file
        if stage == 2:
            tile_dict = {'b': ['brick', pygame.image.load('images/Tile/brick.png')],
                         'i': ['item', pygame.image.load('images/Tile/box.png')],
                         'f': ['flower', pygame.image.load('images/Tile/flower.bmp')],
                         'w': ['win', pygame.image.load('images/Tile/flag.png')]}
            self.load('stage/stage2.txt', tile_dict)
        if stage == 3:
            tile_dict = {'b': ['brick', pygame.image.load('images/Tile/brick.png')],
                         'i': ['item', pygame.image.load('images/Tile/box.png')],
                         'f': ['flower', pygame.image.load('images/Tile/flower.bmp')],
                         'w': ['win', pygame.image.load('images/Tile/flag.png')]}
            self.load('stage/stage3.txt', tile_dict)
        if stage == 4:  # credits screen
            tile_dict = {'b': ['brick', pygame.image.load('images/Tile/brick.png')]}
            self.load('stage/credits.txt', tile_dict)

        # load music
        pygame.mixer.stop()
        if stage in [1, 3]:
            self.bgm = pygame.mixer.Sound('audio/overworld.ogg')
        elif stage in [2]:
            self.bgm = pygame.mixer.Sound('audio/underwater.ogg')
        elif stage == 4:
            self.bgm = pygame.mixer.Sound('audio/ending.ogg')
        self.bgm.play(-1)

        # refresh hud
        hud.refresh()

    def load(self, fname, tile_dict):
        with open(fname, 'r') as f:
            row = 1
            for l in f:
                col = 0
                for c in l:
                    if c in tile_dict:
                        self.platforms.add(Tile(self.screen, tile_dict[c][0], tile_dict[c][1], col * 16, row * 16))
                    if c == 'g':  # goomba
                        self.enemies.add(Goomba(self.screen, col * 16, row * 16))
                    col += 1
                row += 1
        f.close()

    def reset(self, hud):
        self.load_stage(self.stats.current_stage, hud)
