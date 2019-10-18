import pygame
from tile import *
from enemy import *
from pygame.sprite import Group


class StageManager:
    def __init__(self, screen, stats):
        self.stats = stats
        self.screen = screen
        self.sprites = Group()
        self.enemies = Group()
        self.platforms = Group()

    def update(self, player):
        for e in self.enemies:
            e.update(player, self.platforms)

    def draw(self, camera):
        for p in self.platforms:
            p.draw(camera)
        for e in self.enemies:
            e.draw(camera)

    def load_stage(self, stage):  # character's position in txt file is left bot coordinate
        if stage == 1:
            item_img = pygame.image.load('images/Tile/box.png')
            block_img = pygame.image.load('images/Tile/brick.png')
            flower_img = pygame.image.load('images/Tile/flower.bmp')
            with open('stage/stage1.txt', 'r') as f:
                row = 1
                for l in f:
                    col = 0
                    for c in l:
                        if c == 'b':  # brick
                            self.platforms.add(Tile(self.screen, 'brick', block_img, col*16, row*16))
                        if c == 'i':  # item
                            self.platforms.add(Tile(self.screen, 'item', item_img, col*16, row*16))
                        if c == 'f':  # flower
                            self.platforms.add(Tile(self.screen, 'flower', flower_img, col*16, row*16))
                        if c == 'g':  # goomba
                            self.enemies.add(Goomba(self.screen, col*16, row*16))
                        col += 1
                    row += 1
            f.close()
