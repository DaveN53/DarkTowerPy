import random
from math import floor

import pygame

from darktower import utilities
from darktower.constants.defaults import CLOCK_FONT
from darktower.constants.dt_color import DTColor
from darktower.dt_game_display import DTGameDisplay
from darktower.enums import IMAGES, DTUserEvent, AudioFile, DTEvent, InventoryItems
from darktower.utilities import load_image
from darktower.views.base_view import BaseView
from darktower.widgets.dt_button import DTButton


class BattleView(BaseView):

    def __init__(self, game_display: DTGameDisplay):
        super().__init__(game_display=game_display)
        self.brigand_image = load_image('brigands.jpg')
        self.warrior_image = load_image('warriors.jpg')
        self.brigands = 0
        self.rewards = []
        self.round_time = 0
        self.last_sound = 0
        self.cool_down = 3000
        self.new_round = True
        self.round_outcome = None
        self.cancel = False
        self.battle_start = True
        self.battle_end = False
        self.config_battle()

        self.cancel_button = DTButton(
            game_display,
            (self.game_display.width / 4, (self.game_display.height / 4) * 2.8),
            (self.game_display.width / 2, self.game_display.height / 4),
            action=self.cancel_battle,
            color=DTColor.BUTTON_BLUE,
            text='Cancel',
            font_size=40)

    def refresh(self, **extra_refresh_args):
        self.config_battle()

    def display(self):
        if self.battle_end:
            return

        now = pygame.time.get_ticks()
        if self.new_round and self.cancel:
            self.finish_battle()
            return

        if self.battle_start:
            #if now > (self.round_time + 1500):
            self.show_brigands()
            self.play_beep(now)
            if now > (self.round_time + self.cool_down):
                self.battle_start = False
                self.next_round()
            else:
                return

        self.decide_round()

        if now < (self.round_time + self.cool_down):
            self.play_beep(now)
            self.show_warriors()
            self.cancel_button.draw(DTColor.BUTTON_BLUE_DIM if self.cancel else None)
        elif now < (self.round_time + (self.cool_down * 2)):
            self.show_brigands()
            self.cancel_button.draw(DTColor.BUTTON_BLUE_DIM if self.cancel else None)
            self.play_beep(now)
        elif now < (self.round_time + (self.cool_down * 3)):
            if self.battle_start:
                self.battle_start = False
                self.next_round()

            self.play_outcome_audio(now)
        elif now < (self.round_time + (self.cool_down * 3.25)):
            self.next_round()

    def show_brigands(self):
        self.game_display.game.blit(self.brigand_image, (20, 20))
        self.show_text(self.brigands)

    def show_warriors(self):
        self.game_display.game.blit(self.warrior_image, (20, 20))
        self.show_text(self.game_display.current_warriors)

    def show_text(self, text):
        bazaar_price_text = pygame.font.Font(
            CLOCK_FONT, 90).render(
            str(text), True, DTColor.BUTTON_NO_RED)

        text_rect = bazaar_price_text.get_rect()
        text_rect.center = ((self.game_display.width / 4) * 3, self.game_display.height / 4)
        self.game_display.game.blit(bazaar_price_text, text_rect)

    def decide_round(self):
        if self.battle_start:
            return

        if not self.new_round:
            return

        outcome = random.randrange(0, 100)
        # Give player advantage when their numbers are greater
        diff = min(1, self.game_display.current_warriors - self.brigands)
        outcome -= min(35, int(pow(diff, (diff/5)).real))
        if outcome <= 55:
            self.brigands = floor(self.brigands / 2)
            if self.brigands <= 0:
                self.round_outcome = BattleEvent.PLAYER_WON_BATTLE
                self.decide_winnings()
            else:
                self.round_outcome = BattleEvent.PLAYER_WON_ROUND
        else:
            self.game_display.current_warriors -= 1
            if self.game_display.current_warriors <= 1:
                self.round_outcome = BattleEvent.BRIGAND_WON_BATTLE
            else:
                self.round_outcome = BattleEvent.BRIGAND_WON_ROUND

        self.new_round = False

    def next_round(self):
        if self.round_outcome in (BattleEvent.BRIGAND_WON_BATTLE, BattleEvent.PLAYER_WON_BATTLE):
            self.cancel = True
            self.finish_battle()
            self.battle_end = True
            return

        self.new_round = True
        self.round_time = pygame.time.get_ticks()

    def play_outcome_audio(self, now):
        if now < (self.last_sound + self.cool_down):
            return

        if self.round_outcome in (BattleEvent.PLAYER_WON_ROUND, BattleEvent.PLAYER_WON_BATTLE):
            audio_event = pygame.event.Event(DTUserEvent.PLAY_AUDIO, {'audio': AudioFile.BATTLE_ROUND_WON})
            pygame.event.post(audio_event)
        elif self.round_outcome in (BattleEvent.BRIGAND_WON_ROUND, BattleEvent.BRIGAND_WON_BATTLE):
            audio_event = pygame.event.Event(DTUserEvent.PLAY_AUDIO, {'audio': AudioFile.BATTLE_ROUND_LOST})
            pygame.event.post(audio_event)

        self.last_sound = pygame.time.get_ticks()

    def play_beep(self, now):
        if now < (self.last_sound + self.cool_down):
            return

        exit_event = pygame.event.Event(DTUserEvent.PLAY_AUDIO, {'audio': AudioFile.BEEP})
        pygame.event.post(exit_event)
        self.last_sound = pygame.time.get_ticks()

    def config_battle(self):
        self.round_time = 0
        self.last_sound = 0
        self.new_round = True
        self.round_outcome = None
        self.cancel = False
        self.battle_start = True
        self.battle_end = False
        self.rewards = []
        self.round_time = pygame.time.get_ticks()
        self.brigands = random.randrange(
            self.game_display.current_warriors - 3,
            self.game_display.current_warriors + 3
        )

    def decide_winnings(self):
        self.rewards = utilities.decide_winnings(self.game_display, odds=1.5)

    def cancel_battle(self):
        self.cancel = True

    def finish_battle(self):
        if self.rewards:
            print('Rewards:\n{}'.format(self.rewards))
            self.rewards.append(InventoryItems.WARRIOR)
            end_event = pygame.event.Event(DTUserEvent.DT_SELECTION, {'dt_event': DTEvent.SHOW_INVENTORY,
                                                                      'items': self.rewards})
        else:
            end_event = pygame.event.Event(DTUserEvent.DT_SELECTION, {'dt_event': DTEvent.SHOW_INVENTORY,
                                                                      'items': [InventoryItems.WARRIOR]})
        pygame.event.post(end_event)


class BattleEvent:
    PLAYER_WON_ROUND = 0
    BRIGAND_WON_ROUND = 1
    BATTLE_CANCEL = 2
    PLAYER_WON_BATTLE = 3
    BRIGAND_WON_BATTLE = 4
