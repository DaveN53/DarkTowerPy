from darktower.dt_event import DTEvent
from darktower.dt_game_display import DTGameDisplay
from darktower.views.intro_view import IntroView
from darktower.views.player_turn_select_view import PlayerTurnSelectView
from darktower.views.select_difficulty_view import SelectDifficultyView
from darktower.views.select_players_view import SelectPlayersView


class ViewFactory:

    def __init__(self, game_display: DTGameDisplay):
        self.game_display = game_display

    def build_view(self, dt_event: DTEvent):
        if dt_event == DTEvent.INTRO:
            return IntroView(self.game_display)
        elif dt_event == DTEvent.SELECT_DIFFICULTY:
            return SelectDifficultyView(self.game_display)
        elif dt_event == DTEvent.SELECT_PLAYERS:
            return SelectPlayersView(self.game_display)
        elif dt_event == DTEvent.START_PLAYER_TURN:
            return PlayerTurnSelectView(self.game_display)

        raise ViewException('Cannot build view for event: %s', dt_event)


class ViewException(Exception):
    pass
