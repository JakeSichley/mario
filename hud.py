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
        self.score_text = self.font.render('0', True, self.text_color, self.settings.bg_color)
        self.score_rect = self.score_text.get_rect()
        self.score_rect.right = int(self.screen_rect.width / 9)
        self.score_rect.bottom = int(self.screen_rect.height / 20)

        # stage
        self.stage_text = self.font.render('STAGE: ' + str(self.stats.current_stage), True, self.text_color,
                                           self.settings.bg_color)
        self.stage_rect = self.stage_text.get_rect()
        self.stage_rect.left = int(self.screen_rect.width * 0.85)
        self.stage_rect.bottom = self.score_rect.bottom

    def prep_score(self):
        self.score_text = self.font.render(str(int(self.stats.score)), True, self.text_color, self.settings.bg_color)
        self.score_rect = self.score_text.get_rect()
        self.score_rect.right = int(self.screen_rect.width / 9)
        self.score_rect.bottom = int(self.screen_rect.height / 20)

    def prep_stage(self):
        self.stage_text = self.font.render('STAGE: ' + str(self.stats.current_stage), True, self.text_color,
                                           self.settings.bg_color)
        self.stage_rect = self.stage_text.get_rect()
        self.stage_rect.left = int(self.screen_rect.width * 0.85)
        self.stage_rect.bottom = self.score_rect.bottom

    def draw(self):
        self.screen.blit(self.score_text, self.score_rect)
        self.screen.blit(self.stage_text, self.stage_rect)
