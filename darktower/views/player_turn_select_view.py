import pygame

from darktower.constants.defaults import DEFAULT_FONT_SIZE, DEFAULT_FONT_COLOR, CLOCK_FONT
from darktower.constants.dt_color import DTColor
from darktower.enums import DTEvent, DTUserEvent
from darktower.dt_game_display import DTGameDisplay
from darktower.views.base_view import BaseView
from darktower.widgets.dt_button import DTButton


class PlayerTurnSelectView(BaseView):
    def __init__(self, game_display: DTGameDisplay):
        super().__init__(game_display=game_display)

        self.game_display = game_display

        self.bazaar_button = DTButton(
            game_display,
            (self.game_display.width/3, self.game_display.height/4),
            (self.game_display.width/3, self.game_display.height/4),
            action=self.make_selection,
            action_args=[DTEvent.SELECT_BAZAAR],
            color=DTColor.BUTTON_BLUE,
            text='Bazaar',
            font_size=20)
        self.tomb_ruin_button = DTButton(
            game_display,
            (0, (self.game_display.height/4) * 2),
            (self.game_display.width/3, self.game_display.height / 4),
            action=self.make_selection,
            action_args=[DTEvent.SELECT_TOMB_RUIN],
            color=DTColor.BUTTON_BLUE,
            text='Tomb|Ruin',
            font_size=20)
        self.move_button = DTButton(
            game_display,
            (self.game_display.width/3, (self.game_display.height/4) * 2),
            (self.game_display.width/3, self.game_display.height / 4),
            action=self.make_selection,
            action_args=[DTEvent.SELECT_MOVE],
            color=DTColor.BUTTON_BLUE,
            text='Move',
            font_size=20)
        self.sanctuary_citadel_button = DTButton(
            game_display,
            ((self.game_display.width/3)*2, (self.game_display.height/4) * 2),
            (self.game_display.width/3, self.game_display.height / 4),
            action=self.make_selection,
            action_args=[DTEvent.SELECT_SANCTUARY_CITADEL],
            color=DTColor.BUTTON_BLUE,
            text='Sanctuary',
            font_size=20)
        self.dark_tower_button = DTButton(
            game_display,
            (0, (self.game_display.height / 4) * 3),
            (self.game_display.width/3, self.game_display.height / 4),
            action=self.make_selection,
            action_args=[DTEvent.SELECT_DARK_TOWER],
            color=DTColor.BUTTON_RED,
            text='DarkTower',
            font_size=20)
        self.frontier_button = DTButton(
            game_display,
            (self.game_display.width/3, (self.game_display.height / 4) * 3),
            (self.game_display.width/3, self.game_display.height / 4),
            action=self.make_selection,
            action_args=[DTEvent.SELECT_FRONTIER],
            color=DTColor.BUTTON_BLUE,
            text='Frontier',
            font_size=20)
        self.inventory_button = DTButton(
            game_display,
            ((self.game_display.width/3)*2, (self.game_display.height / 4) * 3),
            (self.game_display.width/3, self.game_display.height / 4),
            action=self.make_selection,
            action_args=[DTEvent.SELECT_INVENTORY],
            color=DTColor.BUTTON_DARK_TAN,
            text='Inventory',
            font_size=20)

        self.player_text = pygame.font.Font(
            CLOCK_FONT, DEFAULT_FONT_SIZE).render(
            f'P{self.game_display.current_player + 1}', True, DTColor.BUTTON_NO_RED)

    @staticmethod
    def make_selection(event: DTEvent):
        selection_event = pygame.event.Event(DTUserEvent.DT_SELECTION, {'dt_event': event})
        pygame.event.post(selection_event)

    def refresh(self):
        self.player_text = pygame.font.Font(
            CLOCK_FONT, DEFAULT_FONT_SIZE).render(
            f'P{self.game_display.current_player + 1}', True, DTColor.BUTTON_NO_RED)

    def display(self):
        self.bazaar_button.draw()
        self.tomb_ruin_button.draw()
        self.move_button.draw()
        self.sanctuary_citadel_button.draw()
        self.dark_tower_button.draw()
        self.frontier_button.draw()
        self.inventory_button.draw()

        text_rect = self.player_text.get_rect()
        text_rect.center = (self.game_display.width/2, self.game_display.height/8)
        self.game_display.game.blit(self.player_text, text_rect)
