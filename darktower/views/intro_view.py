import os

import pygame

from darktower.dt_game_display import DTGameDisplay
from darktower.enums import IMAGES
from darktower.utilities import load_image
from darktower.views.base_view import BaseView


class IntroView(BaseView):

    def __init__(self, game_display: DTGameDisplay):
        super().__init__(game_display=game_display)
        self.introImage = load_image('logo.png')

    def display(self):
        self.game_display.game.blit(self.introImage, (0, 0))
