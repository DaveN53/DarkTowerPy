import random

import pygame

from darktower import utilities
from darktower.dt_game_display import DTGameDisplay
from darktower.enums import AudioFile, DTUserEvent, DTEvent
from darktower.views.base_view import BaseView


class TombRuinView(BaseView):
    def __init__(self, game_display: DTGameDisplay):
        super().__init__(game_display=game_display)
        self.rewards = []
        self.cool_down = 4500
        self.award = False
        self.tomb_time = pygame.time.get_ticks()
        self.get_random_event()

    def refresh(self, **extra_refresh_args):
        self.get_random_event()

    def display(self):
        now = pygame.time.get_ticks()
        if self.award and ((now - self.cool_down) > self.tomb_time):
            if self.rewards:
                tomb_event = pygame.event.Event(DTUserEvent.DT_SELECTION, {'dt_event': DTEvent.SHOW_INVENTORY,
                                                                           'items': self.rewards})
            else:
                tomb_event = pygame.event.Event(DTUserEvent.DT_SELECTION, {'dt_event': DTEvent.END_TURN})
            pygame.event.post(tomb_event)

    def get_random_event(self):
        self.rewards = []
        self.award = False
        self.tomb_time = pygame.time.get_ticks()
        outcome = random.randrange(0, 100)
        if outcome < 55:
            tomb_event = pygame.event.Event(DTUserEvent.DT_SELECTION, {'dt_event': DTEvent.TOMB_BATTLE})
            pygame.event.post(tomb_event)
        elif outcome < 80:
            tomb_event = pygame.event.Event(DTUserEvent.DT_SELECTION, {'dt_event': DTEvent.TOMB_NOTHING})
            pygame.event.post(tomb_event)
        else:
            tomb_event = pygame.event.Event(DTUserEvent.DT_SELECTION, {'dt_event': DTEvent.TOMB})
            pygame.event.post(tomb_event)
            self.rewards = utilities.decide_winnings(self.game_display)
            self.award = True
            print(self.rewards)


