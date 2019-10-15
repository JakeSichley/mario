import pygame
from pygame.font import Font


class HUD:
    def __init__(self, screen, settings, stats):
        self.screen = screen
        self.screen_rect = screen.get_rect()
        self.settings = settings
        self.stats = stats
        self.font = Font(None, 26)
        self.text_color = (255, 255, 255)

        # score
        self.score_text = self.font.render('Score: ' + str(int(self.stats.score)), True, self.text_color,
                                           self.settings.bg_color)
        self.score_rect = self.score_text.get_rect()
        self.score_rect.left = 10
        self.score_rect.bottom = int(self.screen_rect.height / 20)

        # stage
        self.stage_text = self.font.render('Stage: ' + str(self.stats.current_stage), True, self.text_color,
                                           self.settings.bg_color)
        self.stage_rect = self.stage_text.get_rect()
        self.stage_rect.left = int(self.screen_rect.width * 0.88)
        self.stage_rect.bottom = self.score_rect.bottom

        # coins
        self.coins_text = self.font.render('Coin: ' + str(self.stats.coins), True, self.text_color,
                                           self.settings.bg_color)
        self.coins_rect = self.coins_text.get_rect()
        self.coins_rect.left = int(self.screen_rect.width * 0.3)
        self.coins_rect.bottom = self.score_rect.bottom

        # lives
        self.lives_text = self.font.render('Lives: ' + str(self.stats.lives_left), True, self.text_color,
                                           self.settings.bg_color)
        self.lives_rect = self.lives_text.get_rect()
        self.lives_rect.left = self.score_rect.left
        self.lives_rect.top = self.score_rect.bottom + 5

        # time

    def prep_score(self):
        self.score_text = self.font.render('Score:' + str(int(self.stats.score)), True, self.text_color,
                                           self.settings.bg_color)
        self.score_rect = self.score_text.get_rect()
        self.score_rect.left = 10
        self.score_rect.bottom = int(self.screen_rect.height / 20)

    def prep_stage(self):
        self.stage_text = self.font.render('STAGE: ' + str(self.stats.current_stage), True, self.text_color,
                                           self.settings.bg_color)
        self.stage_rect = self.stage_text.get_rect()
        self.stage_rect.left = int(self.screen_rect.width * 0.88)
        self.stage_rect.bottom = self.score_rect.bottom

    def prep_lives(self):
        self.lives_text = self.font.render('Lives: ' + str(self.stats.lives_left), True, self.text_color,
                                           self.settings.bg_color)
        self.lives_rect = self.lives_text.get_rect()
        self.lives_rect.left = self.score_rect.left
        self.lives_rect.top = self.score_rect.bottom + 5

    def draw(self):
        self.screen.blit(self.score_text, self.score_rect)
        self.screen.blit(self.stage_text, self.stage_rect)
        self.screen.blit(self.coins_text, self.coins_rect)
        self.screen.blit(self.lives_text, self.lives_rect)
