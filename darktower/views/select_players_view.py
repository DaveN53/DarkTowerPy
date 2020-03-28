import pygame

from darktower.constants.dt_color import DTColor
from darktower.dt_event import DTEvent
from darktower.dt_game_display import DTGameDisplay
from darktower.views.base_view import BaseView
from darktower.widgets.dt_button import DTButton


class SelectPlayersView(BaseView):
    def __init__(self, game_display: DTGameDisplay):
        super().__init__(game_display=game_display)
        self.one_player_button = DTButton(
            game_display,
            (0, 0),
            (self.game_display.width, self.game_display.height/3),
            action=self.set_players,
            action_args=[1],
            color=DTColor.BUTTON_GRAY,
            text='One player')
        self.two_player_button = DTButton(
            game_display,
            (0, self.game_display.height/4),
            (self.game_display.width, self.game_display.height / 4),
            action=self.set_players,
            action_args=[2],
            color=DTColor.BUTTON_GRAY,
            text='Two players')
        self.three_player_button = DTButton(
            game_display,
            (0, (self.game_display.height/4) * 2),
            (self.game_display.width, self.game_display.height / 4),
            action=self.set_players,
            action_args=[3],
            color=DTColor.BUTTON_GRAY,
            text='Three Players')
        self.four_player_button = DTButton(
            game_display,
            (0, (self.game_display.height/4) * 3),
            (self.game_display.width, self.game_display.height / 4),
            action=self.set_players,
            action_args=[4],
            color=DTColor.BUTTON_GRAY,
            text='Four Players')

    def set_players(self, num_players: int):
        self.game_display.num_players = num_players

        intro_event = pygame.event.Event(DTEvent.START_PLAYER_TURN, {'player': 0})
        pygame.event.post(intro_event)

    def display(self):
        self.one_player_button.draw()
        self.two_player_button.draw()
        self.three_player_button.draw()
        self.four_player_button.draw()
