from typing import Tuple, List

import pygame

from darktower.constants.defaults import DEFAULT_FONT, DEFAULT_FONT_SIZE, DEFAULT_FONT_COLOR
from darktower.dt_game_display import DTGameDisplay


class DTButton:
    def __init__(self,
                 game_display: DTGameDisplay,
                 pos: Tuple,
                 dimensions: Tuple,
                 action=None,
                 action_args: List=[],
                 **kwargs):
        self.game_display = game_display
        self.x_pos = pos[0]
        self.y_pos = pos[1]
        self.width = dimensions[0] - 1
        self.height = dimensions[1] - 1
        self.button = (self.x_pos, self.y_pos, self.width, self.height)
        self.action = action
        self.action_args = action_args
        self.color = kwargs.get('color')
        self.text = kwargs.get('text')
        self.font = kwargs.get('font', DEFAULT_FONT)
        self.font_size = kwargs.get('font_size', DEFAULT_FONT_SIZE)
        self.text_color = kwargs.get('text_color', DEFAULT_FONT_COLOR)

    def draw(self, color=None, enabled: bool = True):
        button_color = color or self.color
        if self.is_mouse_hovering():
            pygame.draw.rect(self.game_display.game, tuple(min(c + 20, 255) for c in button_color), self.button)
            if self.game_display.current_event.type == pygame.MOUSEBUTTONUP and self.action:
                print('Pressed: {}\nEnabled: {}'.format(self.text, enabled))
                if enabled:
                    self.action(*self.action_args)

        else:
            pygame.draw.rect(self.game_display.game, button_color, self.button)

        if self.text:
            self.draw_text()

    def draw_text(self):
        text_surface = pygame.font.Font(self.font, self.font_size).render(self.text, True, self.text_color)
        button_x_center = self.x_pos + (self.width / 2)
        button_y_center = self.y_pos + (self.height / 2)
        text_rect = text_surface.get_rect()
        text_rect.center = (button_x_center, button_y_center)
        self.game_display.game.blit(text_surface, text_rect)

    def is_mouse_hovering(self):
        mouse_pos = pygame.mouse.get_pos()
        if self.y_pos < mouse_pos[1] < (self.y_pos + self.height):
            if self.x_pos < mouse_pos[0] < (self.x_pos + self.width):
                return True

        return False

    @staticmethod
    def is_mouse_click():
        if pygame.mouse.get_pressed()[0] == 1:
            return True
        return False
