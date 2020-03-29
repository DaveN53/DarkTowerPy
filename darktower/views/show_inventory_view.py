import os
import pygame

from darktower.constants.defaults import CLOCK_FONT
from darktower.constants.dt_color import DTColor
from darktower.dt_game_display import DTGameDisplay
from darktower.enums import IMAGES, INVENTORY_IMAGES, DTUserEvent, AudioFile, DTEvent
from darktower.views.base_view import BaseView


class ShowInventoryView(BaseView):
    def __init__(self, game_display: DTGameDisplay, **extra_args):
        super().__init__(game_display=game_display)
        self.last = pygame.time.get_ticks()
        self.cool_down = 3000
        self.gold_image = pygame.image.load(os.path.join(IMAGES, 'gold.jpg'))
        item = extra_args.get('item')
        self.item_image = pygame.image.load(INVENTORY_IMAGES[item])
        self.item_count = self.game_display.current_items[item]
        self.beeped = False

    def refresh(self, **extra_refresh_args):
        self.last = pygame.time.get_ticks()
        self.beeped = False

        item = extra_refresh_args.get('item')
        self.item_image = pygame.image.load(INVENTORY_IMAGES[item])
        self.item_count = self.game_display.current_items[item]

    def display(self):
        now = pygame.time.get_ticks()
        if now - self.last <= self.cool_down:
            image = self.item_image
            text = int(self.item_count)
            self.display_item(image, text)
        elif now - self.last <= (self.cool_down * 2):
            image = self.gold_image
            text = self.game_display.current_gold
            self.display_item(image, text)
            if not self.beeped:
                self.play_beep()
                self.beeped = True
        else:
            exit_event = pygame.event.Event(DTUserEvent.DT_SELECTION, {'dt_event': DTEvent.END_TURN})
            pygame.event.post(exit_event)

    def display_item(self, image, text):
        self.game_display.game.blit(image, (0, 0))

        bazaar_price_text = pygame.font.Font(
            CLOCK_FONT, 45).render(
            f'{text}', True, DTColor.BUTTON_NO_RED)

        text_rect = bazaar_price_text.get_rect()
        text_rect.center = ((self.game_display.width / 4) * 3, self.game_display.height / 4)
        self.game_display.game.blit(bazaar_price_text, text_rect)

    def play_beep(self):
        exit_event = pygame.event.Event(DTUserEvent.PLAY_AUDIO, {'audio': AudioFile.BEEP})
        pygame.event.post(exit_event)