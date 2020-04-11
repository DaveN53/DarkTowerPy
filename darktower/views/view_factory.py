from darktower.enums import DTEvent, InventoryItems
from darktower.dt_game_display import DTGameDisplay
from darktower.views.EmptyView import EmptyView
from darktower.views.battle_view import BattleView
from darktower.views.bazaar_closed_view import BazaarClosedView
from darktower.views.bazaar_view import BazaarView
from darktower.views.intro_view import IntroView
from darktower.views.move_view import MoveView
from darktower.views.player_turn_select_view import PlayerTurnSelectView
from darktower.views.sanctuary_citadel_view import SanctuaryCitadelView
from darktower.views.select_difficulty_view import SelectDifficultyView
from darktower.views.select_players_view import SelectPlayersView
from darktower.views.show_inventory_view import ShowInventoryView
from darktower.views.tomb_ruin_view import TombRuinView


class ViewFactory:

    def __init__(self, game_display: DTGameDisplay):
        self.game_display = game_display

    def build_view(self, dt_event: DTEvent, **extra_args):
        if dt_event == DTEvent.INTRO:
            return IntroView(self.game_display)
        elif dt_event == DTEvent.SELECT_DIFFICULTY:
            return SelectDifficultyView(self.game_display)
        elif dt_event == DTEvent.SELECT_PLAYERS:
            return SelectPlayersView(self.game_display)
        elif dt_event == DTEvent.START_PLAYER_TURN:
            return PlayerTurnSelectView(self.game_display)
        elif dt_event == DTEvent.SELECT_BAZAAR:
            return BazaarView(self.game_display)
        elif dt_event == DTEvent.BAZAAR_CLOSED:
            return BazaarClosedView(self.game_display)
        elif dt_event == DTEvent.SHOW_INVENTORY:
            return ShowInventoryView(self.game_display, **extra_args)
        elif dt_event == DTEvent.SELECT_INVENTORY:
            return ShowInventoryView(self.game_display, items=[
                InventoryItems.GOLD,
                InventoryItems.FOOD,
                InventoryItems.WARRIOR,
                InventoryItems.BEAST,
                InventoryItems.HEALER,
                InventoryItems.SCOUT,
                InventoryItems.SWORD,
                InventoryItems.BRASS_KEY,
                InventoryItems.SILVER_KEY,
                InventoryItems.GOLD_KEY
            ])
        elif dt_event == DTEvent.SELECT_SANCTUARY_CITADEL:
            return SanctuaryCitadelView(self.game_display)
        elif dt_event == DTEvent.SELECT_MOVE:
            return MoveView(self.game_display)
        elif dt_event == DTEvent.BATTLE:
            return BattleView(self.game_display)
        elif dt_event == DTEvent.SELECT_TOMB_RUIN:
            return TombRuinView(self.game_display)

        raise ViewException('Cannot build view for event: %s', dt_event)


class ViewException(Exception):
    pass
