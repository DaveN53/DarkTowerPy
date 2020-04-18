import os

import pygame

from darktower.dt_game_display import DTGameDisplay
from darktower.enums import IMAGES
from darktower.utilities import load_image
from darktower.views.base_view import BaseView


class BazaarClosedView(BaseView):
    def __init__(self, game_display: DTGameDisplay):
        super().__init__(game_display=game_display)

    def display(self):
        bazaar_image = load_image('bazaar.jpg')
        width, height = bazaar_image.get_rect().size
        x_pos = (self.game_display.width - width) / 2
        y_pos = (self.game_display.height - height) / 2
        self.game_display.game.blit(bazaar_image, (x_pos, y_pos))


