import random
from enum import IntEnum

import os
import pygame

from darktower.constants.dt_color import DTColor
from darktower.enums import DTEvent, BazaarItems
from darktower.dt_game_display import DTGameDisplay
from darktower.views.base_view import BaseView, IMAGES
from darktower.widgets.dt_button import DTButton


class BazaarView(BaseView):
    def __init__(self, game_display: DTGameDisplay):
        super().__init__(game_display=game_display)
        self.yes_button = DTButton(
            game_display,
            (0, (self.game_display.height/6)*4),
            (self.game_display.width/2, self.game_display.height/6),
            action=self.set_selection,
            action_args=[BazaarSelection.YES],
            color=DTColor.BUTTON_GREEN,
            text='Yes')
        self.no_button = DTButton(
            game_display,
            (self.game_display.width/2, (self.game_display.height/6)*4),
            (self.game_display.width/2, self.game_display.height / 6),
            action=self.set_selection,
            action_args=[BazaarSelection.NO],
            color=DTColor.BUTTON_NO_RED,
            text='No')
        self.haggle_button = DTButton(
            game_display,
            (0, (self.game_display.height/6)*5),
            (self.game_display.width/2, self.game_display.height / 6),
            action=self.set_selection,
            action_args=[BazaarSelection.HAGGLE],
            color=DTColor.BUTTON_ORANGE,
            text='Haggle')
        self.exit_button = DTButton(
            game_display,
            (self.game_display.width/2, (self.game_display.height/6)*5),
            (self.game_display.width/2, self.game_display.height / 6),
            action=self.exit,
            color=DTColor.BUTTON_BLUE,
            text='Exit')

        self.items = self.get_bazaar_items()
        self.selected_item = BazaarItems.FOOD

    def refresh(self):
        self.items = self.get_bazaar_items()
        self.selected_item = BazaarItems.FOOD

    def set_selection(self, selection: int):
        item_index = BAZAAR_ITEMS.index(self.selected_item)
        if selection == BazaarSelection.NO:
            item_index += 1
            if item_index > len(BAZAAR_ITEMS) - 1:
                item_index = 0
            self.selected_item = BAZAAR_ITEMS[item_index]

    def exit(self):
        intro_event = pygame.event.Event(DTEvent.SHOW_INVENTORY, {'item': self.item})
        pygame.event.post(intro_event)

    def display(self):
        self.yes_button.draw()
        self.no_button.draw()
        self.haggle_button.draw()
        self.exit_button.draw()

        bazaar_price = self.items[self.selected_item]
        bazaar_image = pygame.image.load(BAZAAR_IMAGES[self.selected_item])
        self.game_display.game.blit(bazaar_image, (0, 0))

    @staticmethod
    def get_bazaar_items():
        return {
            BazaarItems.FOOD: 1,
            BazaarItems.WARRIOR: random.randrange(4, 10),
            BazaarItems.BEAST: random.randrange(15, 20),
            BazaarItems.SCOUT: random.randrange(15, 20),
            BazaarItems.HEALER: random.randrange(15, 20)
        }


BAZAAR_IMAGES = {
    BazaarItems.FOOD: os.path.join(IMAGES, 'food.jpg'),
    BazaarItems.WARRIOR: os.path.join(IMAGES, 'warrior.jpg'),
    BazaarItems.BEAST: os.path.join(IMAGES, 'beast.jpg'),
    BazaarItems.SCOUT: os.path.join(IMAGES, 'scout.jpg'),
    BazaarItems.HEALER: os.path.join(IMAGES, 'healer.jpg')
}

BAZAAR_ITEMS = [
    BazaarItems.FOOD,
    BazaarItems.WARRIOR,
    BazaarItems.BEAST,
    BazaarItems.SCOUT,
    BazaarItems.HEALER
]


class BazaarSelection(IntEnum):
    NO = 0
    YES = 1
    HAGGLE = 2