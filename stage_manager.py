import pygame
from tile import *
from enemy import *
from pygame.sprite import Group


class StageManager:
    def __init__(self, screen, stats):
        self.stats = stats
        self.screen = screen
        self.enemies = Group()
        self.platforms = Group()
        self.time_limit = 401000  # 400s
        self.time_start = 0
        self.time_elapsed = 0

    def update(self, player):
        # time over
        self.time_elapsed = pygame.time.get_ticks() - self.time_start
        if self.time_elapsed >= self.time_limit:
            if not player.dead:
                player.die()

        for e in self.enemies:
            e.update(player, self.platforms)

    def draw(self, camera):
        for p in self.platforms:
            p.draw(camera)
        for e in self.enemies:
            e.draw(camera)

    def load_stage(self, stage):  # character's position in txt file is left bot coordinate
        self.enemies.empty()
        self.platforms.empty()
        self.time_start = pygame.time.get_ticks()
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
            self.load('stage/stage2.txt', tile_dict)  # build map form txt file

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

    def reset(self):
        self.load_stage(self.stats.current_stage)
