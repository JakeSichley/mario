import pygame


class Camera:
    def __init__(self):
        self.rect = pygame.Rect(0, 0, 800, 600)
        self.x = float(self.rect.x)
        self.vel_x = 0

    def apply(self, target):
        return target.rect.move(self.rect.topleft)

    def update(self, target):

        if target.rect.x + self.rect.x >= 300:
            self.x += -4
        #elif self.rect.x + target.rect.x < 100:
        #    self.x += 4


        # self.x += self.vel_x
        self.rect.x = int(self.x)

        #self.rect.x = -target.rect.x + 400
        print('{}_____{}'.format(str(self.rect.x), str(target.rect.x)))
        # self.rect.y = -target.rect.y + 300

    def out_of_camera(self, target):
        return self.rect.x + target.rect.x <= 0
