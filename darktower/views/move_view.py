import random

import pygame

from darktower.dt_game_display import DTGameDisplay
from darktower.enums import DTUserEvent, AudioFile, MoveEvent, InventoryItems
from darktower.views.base_view import BaseView


class MoveView(BaseView):
    def __init__(self, game_display: DTGameDisplay, **extra_args):
        super().__init__(game_display=game_display)
        self.cool_down = 3000
        self.last = pygame.time.get_ticks()
        self.event = self.get_move_event()

    def refresh(self, **extra_refresh_args):
        self.last = pygame.time.get_ticks()
        self.event = self.get_move_event()

    def display(self):
        now = pygame.time.get_ticks()

    def get_move_event(self):
        rand = random.randrange(0, 100)
        event = MoveEvent.SAFE
        if rand < 5:
            if self.game_display.current_items[InventoryItems.SWORD]:
                event = MoveEvent.DRAGON_KILL
                self.game_display.current_items[InventoryItems.SWORD] = False
            else:
                event = MoveEvent.DRAGON
        elif rand < 20:
            if self.game_display.current_items[InventoryItems.SCOUT]:
                event = MoveEvent.LOST_SCOUT
            else:
                event = MoveEvent.LOST
        elif rand < 35:
            if self.game_display.current_items[InventoryItems.HEALER]:
                event = MoveEvent.PLAGUE_HEALER
            else:
                event = MoveEvent.PLAGUE
        elif rand < 60:
            event = MoveEvent.BATTLE

        self.play_event_audio(event)
        return event

    @staticmethod
    def play_event_audio(event: MoveEvent):
        if event == MoveEvent.DRAGON:
            audio = AudioFile.DRAGON
        elif event == MoveEvent.DRAGON_KILL:
            audio = AudioFile.DRAGON_KILL
        elif event in (MoveEvent.LOST, MoveEvent.LOST_SCOUT):
            audio = AudioFile.LOST
        elif event in (MoveEvent.PLAGUE, MoveEvent.PLAGUE_HEALER):
            audio = AudioFile.PLAGUE
        elif event == MoveEvent.BATTLE:
            audio = AudioFile.BATTLE
        elif event == MoveEvent.SAFE:
            audio = AudioFile.BEEP

        audio_event = pygame.event.Event(DTUserEvent.PLAY_AUDIO, {'audio': audio})
        pygame.event.post(audio_event)
