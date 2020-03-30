import random

import pygame

from darktower.dt_game_display import DTGameDisplay
from darktower.enums import DTUserEvent, AudioFile, MoveEvent, InventoryItems, EVENT_IMAGES, DTEvent
from darktower.views.base_view import BaseView


class MoveView(BaseView):
    def __init__(self, game_display: DTGameDisplay, **extra_args):
        super().__init__(game_display=game_display)
        self.cool_down = 3000
        self.last_beep = self.last = pygame.time.get_ticks()
        self.event = self.get_move_event()

    def refresh(self, **extra_refresh_args):
        self.last_beep = self.last = pygame.time.get_ticks()
        self.event = self.get_move_event()

    def display(self):
        if self.event in (MoveEvent.DRAGON, MoveEvent.DRAGON_KILL):
            self.display_dragon_event()
        elif self.event in (MoveEvent.LOST, MoveEvent.LOST_SCOUT):
            self.display_lost()

    def display_dragon_event(self):
        now = pygame.time.get_ticks()
        if ((now - self.last) > 1200) and self.event == MoveEvent.DRAGON_KILL:
            # TODO don't load for every frame
            dragon_image = pygame.image.load(EVENT_IMAGES[self.event])
            event_time = 5000
        else:
            dragon_image = pygame.image.load(EVENT_IMAGES[MoveEvent.DRAGON])
            event_time = 3000
        self.display_event(dragon_image)

        if (now - self.last) > event_time:
            selection_event = pygame.event.Event(DTUserEvent.DT_SELECTION, {
                'dt_event': DTEvent.SHOW_INVENTORY,
                'items': [InventoryItems.WARRIOR]})
            pygame.event.post(selection_event)

    def display_lost(self):
        now = pygame.time.get_ticks()
        if ((now - self.last) > 3000) and self.event == MoveEvent.LOST_SCOUT:
            # TODO only create once
            lost_image = pygame.image.load(EVENT_IMAGES[self.event])
            selection_event = pygame.event.Event(DTUserEvent.DT_SELECTION, {'dt_event': DTEvent.START_PLAYER_TURN})
            event_time = 5000
            if (now - self.last_beep) > 3000:
                self.play_beep()
                self.last_beep = pygame.time.get_ticks()

        else:
            lost_image = pygame.image.load(EVENT_IMAGES[MoveEvent.LOST])
            selection_event = pygame.event.Event(DTUserEvent.DT_SELECTION, {'dt_event': DTEvent.END_TURN})
            event_time = 3250
        self.display_event(lost_image)

        if (now - self.last) > event_time:
            pygame.event.post(selection_event)

    def display_event(self, image):
        width, height = image.get_rect().size
        x_pos = (self.game_display.width - width) / 2
        y_pos = (self.game_display.height - height) / 2
        self.game_display.game.blit(image, (x_pos, y_pos))

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


        # TODO REMOVE
        event = MoveEvent.LOST_SCOUT


        self.play_event_audio(event)
        return event

    def play_beep(self):
        exit_event = pygame.event.Event(DTUserEvent.PLAY_AUDIO, {'audio': AudioFile.BEEP})
        pygame.event.post(exit_event)

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
