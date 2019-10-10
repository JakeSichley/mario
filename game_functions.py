import pygame
import sys
from pygame.locals import *


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
    pass


def check_keyup(event, player):
    if event.key == K_ESCAPE:
        terminate()


def update_screen(settings, screen):
    screen.fill(settings.bg_color)
