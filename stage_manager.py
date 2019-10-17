import pygame
from tile import *
from enemy import *
from pygame.sprite import Group


class StageManager:
    def __init__(self, screen, stats):
        self.stats = stats
        self.screen = screen
        self.sprites = Group()

    def update(self, player):
        for s in self.sprites:
            if s.tag == 'enemy':
                s.update(player, self.sprites)

    def draw(self, camera):
        for s in self.sprites:
            s.draw(camera)

    def load_stage(self, stage):
        item_img = pygame.image.load('images/Tile/box.png')
        block_img = pygame.image.load('images/Tile/brick.png')
        flower_img = pygame.image.load('images/Tile/flower.bmp')
        self.sprites.add(Tile(self.screen, 'item', item_img, 700, 310))
        self.sprites.add(Tile(self.screen, 'item', item_img, 1000, 310))
        for i in range(100):
            self.sprites.add(Tile(self.screen, 'brick', block_img, i * 16, 400))
        self.sprites.add(Tile(self.screen, 'brick', block_img, 800, 310))
        self.sprites.add(Tile(self.screen, 'brick', block_img, 1100, 380))
        self.sprites.add(Tile(self.screen, 'brick', block_img, 900, 380))
        self.sprites.add(Tile(self.screen, 'flower', flower_img, 200, 310))
        self.sprites.add(Goomba(self.screen, 950, 300))
