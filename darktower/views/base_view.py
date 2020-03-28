from abc import ABC

import os

from darktower.dt_game_display import DTGameDisplay

RESOURCES = os.path.join(os.path.dirname(__file__), 'resources')
FONTS = os.path.join(RESOURCES, 'font')
IMAGES = os.path.join(RESOURCES, 'images')


class BaseView(ABC):

    def __init__(self, game_display: DTGameDisplay):
        self.game_display: DTGameDisplay = game_display

    def display(self):
        pass

    def play_audio(self):
        pass
