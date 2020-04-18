from abc import ABC

from darktower.dt_game_display import DTGameDisplay


class BaseView(ABC):

    def __init__(self, game_display: DTGameDisplay):
        self.game_display = game_display

    def display(self):
        pass

    def play_audio(self):
        pass

    def refresh(self, **extra_refresh_args):
        pass
