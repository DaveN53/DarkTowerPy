import random

import pygame

from darktower.dt_game_display import DTGameDisplay
from darktower.enums import AudioFile, DTUserEvent, InventoryItems, DTEvent
from darktower.views.base_view import BaseView


class SanctuaryCitadelView(BaseView):
    def __init__(self, game_display: DTGameDisplay, **extra_args):
        super().__init__(game_display=game_display)
        self.cool_down = 3000
        self.last = pygame.time.get_ticks()
        self.show_rewards = True

        self.awarded_items = self.calculate_need()
        exit_event = pygame.event.Event(DTUserEvent.PLAY_AUDIO, {'audio': AudioFile.SANCTUART_CITADEL})
        pygame.event.post(exit_event)

    def refresh(self, **extra_refresh_args):
        self.last = pygame.time.get_ticks()
        self.show_rewards = True

        self.awarded_items = self.calculate_need()
        exit_event = pygame.event.Event(DTUserEvent.PLAY_AUDIO, {'audio': AudioFile.SANCTUART_CITADEL})
        pygame.event.post(exit_event)

    def display(self):
        now = pygame.time.get_ticks()
        if (now - self.last) > self.cool_down:
            if self.show_rewards:
                show_event = pygame.event.Event(DTUserEvent.DT_SELECTION,
                                                {'dt_event': DTEvent.SHOW_INVENTORY,
                                                 'items': self.awarded_items})
                pygame.event.post(show_event)

    def calculate_need(self):
        awarded_items = []
        if self.game_display.current_gold <= 7:
            gold_min = 7 - self.game_display.current_gold
            self.game_display.current_gold += random.randrange(gold_min, 10)
        if self.game_display.current_items[InventoryItems.FOOD] <= 5:
            food_min = 5 - self.game_display.current_items[InventoryItems.FOOD]
            self.game_display.current_items[InventoryItems.FOOD] += random.randrange(food_min, 6)
            awarded_items.append(InventoryItems.FOOD)
        if self.game_display.current_items[InventoryItems.WARRIOR] <= 4:
            warrior_min = 4 - self.game_display.current_items[InventoryItems.WARRIOR]
            self.game_display.current_items[InventoryItems.WARRIOR] += random.randrange(warrior_min, 4)
            awarded_items.append(InventoryItems.WARRIOR)
        return awarded_items
