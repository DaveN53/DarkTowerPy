import os
import pygame

from darktower.constants.defaults import CLOCK_FONT
from darktower.constants.dt_color import DTColor
from darktower.dt_game_display import DTGameDisplay
from darktower.enums import IMAGES, INVENTORY_IMAGES, DTUserEvent, AudioFile, DTEvent
from darktower.utilities import load_image
from darktower.views.base_view import BaseView


class ShowInventoryView(BaseView):
    def __init__(self, game_display: DTGameDisplay, **extra_args):
        super().__init__(game_display=game_display)
        self.cool_down = 3000

        print('Init Extra Args: {}'.format(extra_args))
        self.items = extra_args.get('items', [])
        self.setup_display()

    def refresh(self, **extra_refresh_args):
        print('Refresh Extra Args: {}'.format(extra_refresh_args))
        self.items = extra_refresh_args.get('items', [])
        self.setup_display()

    def display(self):
        now = pygame.time.get_ticks()

        i = int((now - self.last) / self.cool_down)
        if i < len(self.items):
            item = self.item_info[self.items[i]]
            image_path = item['image_path']
            text = int(item['count'])
            image = load_image(image_path)
            self.display_item(image, text)
            self.play_beep(now)
        else:
            exit_event = pygame.event.Event(DTUserEvent.DT_SELECTION, {'dt_event': DTEvent.END_TURN})
            pygame.event.post(exit_event)

    def display_item(self, image, text):
        self.game_display.game.blit(image, (20, 20))

        bazaar_price_text = pygame.font.Font(
            CLOCK_FONT, 90).render(
            str(text), True, DTColor.BUTTON_NO_RED)

        text_rect = bazaar_price_text.get_rect()
        text_rect.center = ((self.game_display.width / 4) * 3, self.game_display.height / 4)
        self.game_display.game.blit(bazaar_price_text, text_rect)

    def setup_display(self):
        self.last = pygame.time.get_ticks()
        self.last_beep = pygame.time.get_ticks() - self.cool_down

        self.item_info = {}
        final_items = []
        print('Items: {}'.format(self.items))
        for item in self.items:
            value = self.game_display.current_items[item]
            if type(value) == bool and not value:
                continue

            final_items.append(item)
            self.item_info[item] = {
                'count': self.game_display.current_items[item],
                'image_path': INVENTORY_IMAGES[item]
            }
        self.items = final_items
        print('Final Items: {}'.format(self.items))

    def play_beep(self, now):
        if now - self.last_beep > self.cool_down:
            exit_event = pygame.event.Event(DTUserEvent.PLAY_AUDIO, {'audio': AudioFile.BEEP})
            pygame.event.post(exit_event)
            self.last_beep = pygame.time.get_ticks()
