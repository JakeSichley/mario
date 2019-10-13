import pygame
import sys
from pygame.locals import *


RIGHT_KEYS = [K_d, K_RIGHT]
LEFT_KEYS = [K_a, K_LEFT]


def terminate():
    pygame.quit()
    sys.exit()


def check_inputs(player):
    for e in pygame.event.get():
        if e.type == QUIT:
            terminate()
        elif e.type == KEYDOWN:
            check_keydown(e, player)
        elif e.type == KEYUP:
            check_keyup(e, player)


def check_keydown(event, player):
    if event.key == K_w:
        player.jump()


def check_keyup(event, player):
    if event.key == K_ESCAPE:
        terminate()


def update_screen(settings, screen):
    screen.fill(settings.bg_color)


def update_player(player, sprites):
    player.update()

    sprite = pygame.sprite.spritecollideany(player, sprites)
    if sprite is not None:
        if sprite.tag == 'item':
            player.level_up()
            sprite.kill()
