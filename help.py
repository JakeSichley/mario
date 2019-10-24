from pygame.font import Font


class HelpText:
    def __init__(self, screen, settings):
        self.screen = screen
        self.settings = settings
        self.font = Font(None, 30)
        self.msg = 'A/D: move left/right   W: jump    S: crouch    Space: fire'
        self.text = self.font.render(self.msg, True, (255, 255, 255), self.settings.bg_color)
        self.rect = self.text.get_rect()
        self.rect.x = 17
        self.rect.top = 100

    def draw(self, camera):
        self.screen.blit(self.text, camera.apply(self))
