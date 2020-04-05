import pygame
from pygame.event import Event

from darktower.dt_game_display import DTGameDisplay
from darktower.enums import DTEvent, DTUserEvent, InventoryItems
from darktower.views.audio_player import AudioPlayer
from darktower.views.view_manager import ViewManager


class EventManager:

    def __init__(self, game_display: DTGameDisplay, view_manager: ViewManager, audio_player: AudioPlayer):
        self.game_display = game_display
        self.view_manager = view_manager
        self.audio_player = audio_player
        self.event = DTEvent.INTRO

    def start(self):
        start_event = DTEvent.SELECT_PLAYERS
        self.view_manager.update(start_event)
        self.audio_player.trigger_audio(start_event)

    def consume_event(self, event: Event):
        if event.type == DTUserEvent.DT_SELECTION:
            self.consume_dt_selection_event(event)
            return
        elif event.type == DTUserEvent.MUSIC_END:
            self.consume_dt_audio_end_event(event)
            return
        elif event.type == DTUserEvent.PLAY_AUDIO:
            self.consume_dt_play_audio_event(event)
            return

        if event.type < pygame.USEREVENT or event.type > (pygame.USEREVENT + 9):
            return

        raise EventException('Unknown event: %s', event)

    def consume_dt_selection_event(self, event: Event):
        print('Consuming Event: %s', event)
        dt_event = self.get_dt_event(event)

        if dt_event == DTEvent.BAZAAR_PURCHASE:
            dt_event = self.game_display.attempt_purchase(
                price=event.dict.get('total_price'),
                item=event.dict.get('item'),
                item_count=event.dict.get('item_count')
            )

        if dt_event in (DTEvent.BAZAAR_CLOSED, DTEvent.END_TURN):
            self.game_display.end_turn()

        if dt_event == DTEvent.SHOW_INVENTORY:
            items = event.dict.get('items')
            self.view_manager.update(dt_event, items=items)
        elif dt_event == DTEvent.SELECT_INVENTORY:
            self.view_manager.update(dt_event, items=[
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

        elif dt_event:
            self.view_manager.update(dt_event)
        self.audio_player.trigger_audio(dt_event)

    def consume_dt_audio_end_event(self, event: Event):
        dt_event = self.get_dt_event(event)

        if dt_event:
            self.view_manager.update(dt_event)

        self.post_audio_end_event()

    def consume_dt_play_audio_event(self, event: Event):
        audio = event.dict.get('audio')
        self.audio_player.play_wave(audio)

    @staticmethod
    def get_dt_event(event: Event):
        return event.dict.get('dt_event')

    def post_audio_end_event(self):
        if self.audio_player.end_event_available():
            intro_event = pygame.event.Event(
                DTUserEvent.DT_SELECTION,
                {'dt_event': self.audio_player.consume_audio_end_event()}
            )
            pygame.event.post(intro_event)


class EventException(Exception):
    pass
