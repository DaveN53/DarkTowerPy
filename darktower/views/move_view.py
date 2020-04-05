import random

import pygame
from math import ceil

from darktower.dt_game_display import DTGameDisplay
from darktower.enums import DTUserEvent, AudioFile, MoveEvent, InventoryItems, EVENT_IMAGES, DTEvent
from darktower.views.base_view import BaseView


class MoveView(BaseView):
    def __init__(self, game_display: DTGameDisplay, **extra_args):
        super().__init__(game_display=game_display)
        self.cool_down = 3000
        self.images = {}
        self.event_time = 0
        self.initial_event_time = 0
        self.selection_event = None

        self.last_beep = self.last = pygame.time.get_ticks()
        self.event = self.get_move_event()
        self.configure_event()

    def get_event_images(self, event):
        image = self.images.get(event)
        if not image:
            image = pygame.image.load(EVENT_IMAGES[event])
            self.images[event] = image

        return image

    def refresh(self, **extra_refresh_args):
        self.last_beep = self.last = pygame.time.get_ticks()
        self.event = self.get_move_event()
        self.configure_event()

    def display(self):
        now = pygame.time.get_ticks()
        if self.event == MoveEvent.SAFE:
            if (now - self.last) > self.event_time:
                pygame.event.post(self.selection_event)
        elif self.event in (MoveEvent.DRAGON, MoveEvent.DRAGON_KILL):
            self.display_dragon_event()
        elif self.event in (MoveEvent.LOST, MoveEvent.LOST_SCOUT):
            self.display_lost()
        elif self.event in (MoveEvent.PLAGUE, MoveEvent.PLAGUE_HEALER):
            self.display_plague()
        elif self.event == MoveEvent.BATTLE:
            if (now - self.last) > self.event_time:
                pygame.event.post(self.selection_event)

    def display_dragon_event(self):
        now = pygame.time.get_ticks()
        if ((now - self.last) > 1200) and self.event == MoveEvent.DRAGON_KILL:
            # TODO don't load for every frame
            dragon_image = pygame.image.load(EVENT_IMAGES[MoveEvent.DRAGON_KILL])
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
        self.display_lost_plague(MoveEvent.LOST, MoveEvent.LOST_SCOUT)

    def display_plague(self):
        self.display_lost_plague(MoveEvent.PLAGUE, MoveEvent.PLAGUE_HEALER)

    def display_lost_plague(self, initial_event: MoveEvent, resolution_event: MoveEvent):
        now = pygame.time.get_ticks()
        if ((now - self.last) > self.initial_event_time) and self.event == resolution_event:
            lost_image = self.get_event_images(resolution_event)
            if (now - self.last_beep) > self.initial_event_time:
                self.play_beep()
                self.last_beep = pygame.time.get_ticks()
        else:
            lost_image = self.get_event_images(initial_event)
        self.display_event(lost_image)

        if (now - self.last) > self.event_time:
            pygame.event.post(self.selection_event)

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
        elif rand < 15:
            if self.game_display.current_items[InventoryItems.SCOUT]:
                event = MoveEvent.LOST_SCOUT
            else:
                event = MoveEvent.LOST
        elif rand < 30:
            if self.game_display.current_items[InventoryItems.HEALER]:
                event = MoveEvent.PLAGUE_HEALER
            else:
                event = MoveEvent.PLAGUE
        elif rand < 50:
            event = MoveEvent.BATTLE

        print(f'rand: {rand}, event: {event}')


        # TODO REMOVE
        event = MoveEvent.BATTLE

        self.play_event_audio(event)
        return event

    def configure_event(self):
        if self.event == MoveEvent.SAFE:
            self.event_time = 2000
            self.selection_event = pygame.event.Event(DTUserEvent.DT_SELECTION, {'dt_event': DTEvent.END_TURN})
        elif self.event == MoveEvent.DRAGON:
            stolen_warriors = ceil(self.game_display.current_warriors / 4)
            stolen_gold = ceil(self.game_display.current_gold / 4)

            self.game_display.dragon[InventoryItems.WARRIOR] += stolen_warriors
            self.game_display.dragon[InventoryItems.GOLD] += stolen_gold

            self.game_display.current_warriors -= stolen_warriors
            self.game_display.current_gold -= stolen_gold

            self.selection_event = pygame.event.Event(DTUserEvent.DT_SELECTION, {'dt_event': DTEvent.SHOW_INVENTORY,
                                                                                 'items': [InventoryItems.WARRIOR]})
        elif self.event == MoveEvent.DRAGON_KILL:
            self.game_display.current_warriors += self.game_display.dragon[InventoryItems.WARRIOR]
            self.game_display.current_gold += self.game_display.dragon[InventoryItems.GOLD]

            self.game_display.dragon[InventoryItems.WARRIOR] = 0
            self.game_display.dragon[InventoryItems.GOLD] = 0

            self.selection_event = pygame.event.Event(DTUserEvent.DT_SELECTION, {'dt_event': DTEvent.SHOW_INVENTORY,
                                                                                 'items': [InventoryItems.WARRIOR]})
        elif self.event == MoveEvent.LOST:
            self.selection_event = pygame.event.Event(DTUserEvent.DT_SELECTION, {'dt_event': DTEvent.END_TURN})
            self.event_time = 3250
        elif self.event == MoveEvent.LOST_SCOUT:
            self.selection_event = pygame.event.Event(DTUserEvent.DT_SELECTION, {'dt_event': DTEvent.START_PLAYER_TURN})
            self.event_time = 5000
            self.initial_event_time = 3000
        elif self.event == MoveEvent.PLAGUE:
            self.game_display.current_warriors -= 2
            self.selection_event = pygame.event.Event(DTUserEvent.DT_SELECTION, {'dt_event': DTEvent.SHOW_INVENTORY,
                                                                                 'items': [InventoryItems.WARRIOR]})
            self.event_time = 3250
        elif self.event == MoveEvent.PLAGUE_HEALER:
            self.game_display.current_warriors += 2
            self.selection_event = pygame.event.Event(DTUserEvent.DT_SELECTION, {'dt_event': DTEvent.SHOW_INVENTORY,
                                                                                 'items': [InventoryItems.WARRIOR]})
            self.event_time = 5500
            self.initial_event_time = 3500
        elif self.event == MoveEvent.BATTLE:
            self.event_time = 2000
            self.selection_event = pygame.event.Event(DTUserEvent.DT_SELECTION, {'dt_event': DTEvent.BATTLE})

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
