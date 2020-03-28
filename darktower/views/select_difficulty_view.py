import pygame

from darktower.constants.dt_color import DTColor
from darktower.dt_event import DTEvent
from darktower.dt_game_display import DTGameDisplay
from darktower.views.base_view import BaseView
from darktower.widgets.dt_button import DTButton


class SelectDifficultyView(BaseView):
    def __init__(self, game_display: DTGameDisplay):
        super().__init__(game_display=game_display)
        self.level_one_button = DTButton(
            game_display,
            (0, 0),
            (self.game_display.width, self.game_display.height/3),
            action=self.set_diff,
            action_args=[1],
            color=DTColor.BUTTON_GRAY,
            text='level one')
        self.level_two_button = DTButton(
            game_display,
            (0, self.game_display.height/3),
            (self.game_display.width, self.game_display.height / 3),
            action=self.set_diff,
            action_args=[2],
            color=DTColor.BUTTON_GRAY,
            text='level two')
        self.level_three_button = DTButton(
            game_display,
            (0, (self.game_display.height/3) * 2),
            (self.game_display.width, self.game_display.height / 3),
            action=self.set_diff,
            action_args=[3],
            color=DTColor.BUTTON_GRAY,
            text='level three')

    def set_diff(self, diff: int):
        self.game_display.difficulty = diff

        intro_event = pygame.event.Event(DTEvent.SELECT_PLAYERS, {})
        pygame.event.post(intro_event)

    def display(self):
        self.level_one_button.draw()
        self.level_two_button.draw()
        self.level_three_button.draw()
