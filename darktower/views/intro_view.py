import os

import pygame

from darktower.dt_game_display import DTGameDisplay
from darktower.enums import IMAGES
from darktower.views.base_view import BaseView


class IntroView(BaseView):

    def __init__(self, game_display: DTGameDisplay):
        super().__init__(game_display=game_display)
        self.introImage = pygame.image.load(os.path.join(IMAGES, 'logo.png'))

    def display(self):
        self.game_display.game.blit(self.introImage, (0, 0))
