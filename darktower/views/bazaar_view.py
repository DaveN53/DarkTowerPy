import random
from enum import IntEnum

import pygame

from darktower.constants.defaults import CLOCK_FONT
from darktower.constants.dt_color import DTColor
from darktower.enums import DTEvent, DTUserEvent, AudioFile, INVENTORY_IMAGES, InventoryItems
from darktower.dt_game_display import DTGameDisplay
from darktower.views.base_view import BaseView
from darktower.widgets.dt_button import DTButton


class BazaarView(BaseView):
    def __init__(self, game_display: DTGameDisplay):
        super().__init__(game_display=game_display)
        self.yes_button = DTButton(
            game_display,
            (0, (self.game_display.height/5)*3),
            (self.game_display.width/2, self.game_display.height/5),
            action=self.set_selection,
            action_args=[BazaarSelection.YES],
            color=DTColor.BUTTON_GREEN,
            text='Yes')
        self.no_button = DTButton(
            game_display,
            (self.game_display.width/2, (self.game_display.height/5)*3),
            (self.game_display.width/2, self.game_display.height / 5),
            action=self.set_selection,
            action_args=[BazaarSelection.NO],
            color=DTColor.BUTTON_NO_RED,
            text='No')
        self.haggle_button = DTButton(
            game_display,
            (0, (self.game_display.height/5)*4),
            (self.game_display.width/2, self.game_display.height / 5),
            action=self.set_selection,
            action_args=[BazaarSelection.HAGGLE],
            color=DTColor.BUTTON_ORANGE,
            text='Haggle')
        self.exit_button = DTButton(
            game_display,
            (self.game_display.width/2, (self.game_display.height/5)*4),
            (self.game_display.width/2, self.game_display.height / 5),
            action=self.set_selection,
            action_args=[BazaarSelection.EXIT],
            color=DTColor.BUTTON_BLUE,
            text='Exit')

        self.items = self.get_bazaar_items()
        self.selected_item = InventoryItems.FOOD
        self.purchase = False
        self.purchase_count = 1

    def refresh(self):
        self.items = self.get_bazaar_items()
        self.selected_item = InventoryItems.FOOD
        self.purchase_count = 1
        self.purchase = False

    def set_selection(self, selection: int):
        self.play_beep()
        if selection == BazaarSelection.NO:
            if not self.purchase:
                self.next_item()
            else:
                self.purchase_item()
        elif selection == BazaarSelection.YES:
            if not self.purchase:
                self.purchase = True
            elif not self.selected_item_single():
                self.purchase_count += 1
        elif selection == BazaarSelection.HAGGLE:
            self.haggle()
        elif selection == BazaarSelection.EXIT:
            if self.purchase:
                self.purchase_count = 1
                self.purchase = False
            else:
                self.exit_bazaar(DTEvent.END_TURN)

    @staticmethod
    def exit_bazaar(event):
        exit_event = pygame.event.Event(DTUserEvent.DT_SELECTION, {'dt_event': event})
        pygame.event.post(exit_event)

    def next_item(self):
        item_index = BAZAAR_ITEMS.index(self.selected_item)
        item_index += 1
        if item_index > len(BAZAAR_ITEMS) - 1:
            item_index = 0
        self.selected_item = BAZAAR_ITEMS[item_index]

    def haggle(self):
        result = random.randrange(0, 100)
        if result < 50:
            new_price = self.items[self.selected_item] - 1
            self.items[self.selected_item] = max(new_price, 1)
        else:
            self.exit_bazaar(DTEvent.BAZAAR_CLOSED)

    def purchase_item(self):
        total_price = self.purchase_count * self.items[self.selected_item]

        purchase_event = self.game_display.attempt_purchase(total_price, self.selected_item, self.purchase_count)
        pygame.event.post(purchase_event)

    def selected_item_single(self):
        if self.selected_item in (InventoryItems.HEALER, InventoryItems.SCOUT, InventoryItems.BEAST):
            return True
        return False

    def play_beep(self):
        exit_event = pygame.event.Event(DTUserEvent.PLAY_AUDIO, {'audio': AudioFile.BEEP})
        pygame.event.post(exit_event)

    def display(self):
        self.yes_button.draw()
        self.no_button.draw()
        if not self.purchase:
            self.haggle_button.draw()
        self.exit_button.draw()

        bazaar_price = self.items[self.selected_item]
        bazaar_image = pygame.image.load(INVENTORY_IMAGES[self.selected_item])
        self.game_display.game.blit(bazaar_image, (10, 10))

        if not self.purchase:
            clock_text = bazaar_price
        else:
            clock_text = self.purchase_count

        bazaar_price_text = pygame.font.Font(
            CLOCK_FONT, 45).render(
            f'{clock_text}', True, DTColor.BUTTON_NO_RED)

        text_rect = bazaar_price_text.get_rect()
        text_rect.center = ((self.game_display.width / 4)*3, self.game_display.height / 4)
        self.game_display.game.blit(bazaar_price_text, text_rect)

    @staticmethod
    def get_bazaar_items():
        return {
            InventoryItems.FOOD: 1,
            InventoryItems.WARRIOR: random.randrange(4, 10),
            InventoryItems.BEAST: random.randrange(15, 20),
            InventoryItems.SCOUT: random.randrange(15, 20),
            InventoryItems.HEALER: random.randrange(15, 20)
        }


BAZAAR_ITEMS = [
    InventoryItems.FOOD,
    InventoryItems.WARRIOR,
    InventoryItems.BEAST,
    InventoryItems.SCOUT,
    InventoryItems.HEALER
]


class BazaarSelection(IntEnum):
    NO = 0
    YES = 1
    HAGGLE = 2
    EXIT = 3