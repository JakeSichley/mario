class GameStats:
    def __init__(self):
        self.game_status = 0  # 0: menu, 1: game active
        self.current_stage = 1
        self.score = 0

        self.lives_left = 3

    def reset(self):
        self.game_status = 0
        self.current_stage = 1
        self.score = 0
        self.lives_left = 3
