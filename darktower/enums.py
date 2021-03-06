from enum import IntEnum

import os
import pygame

RESOURCES = os.path.join(os.path.dirname(__file__), 'views', 'resources')
FONTS = os.path.join(RESOURCES, 'font')
IMAGES = os.path.join(RESOURCES, 'images')
SOUNDS = os.path.join(RESOURCES, 'sounds')


def dt_event_num(num: int):
    return pygame.USEREVENT + 1 + num


class DTUserEvent(IntEnum):
    DT_SELECTION = dt_event_num(0)
    MUSIC_END = dt_event_num(1)
    PLAY_AUDIO = dt_event_num(2)


class DTEvent(IntEnum):
    INTRO = 0
    SELECT_DIFFICULTY = 1
    SELECT_PLAYERS = 2
    START_PLAYER_TURN = 3
    SELECT_BAZAAR = 4
    SELECT_TOMB_RUIN = 5
    SELECT_MOVE = 6
    SELECT_SANCTUARY_CITADEL = 7
    SELECT_DARK_TOWER = 8
    SELECT_FRONTIER = 9
    SELECT_INVENTORY = 10
    SHOW_INVENTORY = 11
    BAZAAR_CLOSED = 12
    END_TURN = 13
    BAZAAR_PURCHASE = 14
    BATTLE = 15
    TOMB_NOTHING = 16
    TOMB_BATTLE = 17
    TOMB = 18
    DO_NOTHING = 99


class InventoryItems(IntEnum):
    FOOD = 0
    WARRIOR = 1
    BEAST = 2
    SCOUT = 3
    HEALER = 4
    SWORD = 5
    BRASS_KEY = 6
    SILVER_KEY = 7
    GOLD_KEY = 8
    GOLD = 9
    PEGASUS = 10
    WIZARD = 11


class AudioFile:
    INTRO = os.path.join(SOUNDS, 'intro.wav')
    BAZAAR = os.path.join(SOUNDS, 'bazaar.wav')
    BAZAAR_CLOSED = os.path.join(SOUNDS, 'bazaar-closed.wav')
    BEEP = os.path.join(SOUNDS, 'beep.wav')
    SANCTUARY_CITADEL = os.path.join(SOUNDS, 'sanctuary.wav')
    DRAGON = os.path.join(SOUNDS, 'dragon.wav')
    DRAGON_KILL = os.path.join(SOUNDS, 'dragon-kill.wav')
    LOST = os.path.join(SOUNDS, 'lost.wav')
    PLAGUE = os.path.join(SOUNDS, 'plague.wav')
    BATTLE = os.path.join(SOUNDS, 'battle.wav')
    BATTLE_ROUND_WON = os.path.join(SOUNDS, 'enemy-hit.wav')
    BATTLE_ROUND_LOST = os.path.join(SOUNDS, 'player-hit.wav')
    TOMB = os.path.join(SOUNDS, 'tomb.wav')
    TOMB_BATTLE = os.path.join(SOUNDS, 'tomb-battle.wav')
    TOMB_NOTHING = os.path.join(SOUNDS, 'tomb-nothing.wav')


class MoveEvent:
    SAFE = 0
    LOST = 1
    PLAGUE = 2
    DRAGON = 3
    BATTLE = 4
    DRAGON_KILL = 5
    LOST_SCOUT = 6
    PLAGUE_HEALER = 7


INVENTORY_IMAGES = {
    InventoryItems.FOOD: os.path.join(IMAGES, 'food.jpg'),
    InventoryItems.WARRIOR: os.path.join(IMAGES, 'warrior.jpg'),
    InventoryItems.BEAST: os.path.join(IMAGES, 'beast.jpg'),
    InventoryItems.SCOUT: os.path.join(IMAGES, 'scout.jpg'),
    InventoryItems.HEALER: os.path.join(IMAGES, 'healer.jpg'),
    InventoryItems.SWORD: os.path.join(IMAGES, 'sword.jpg'),
    InventoryItems.BRASS_KEY: os.path.join(IMAGES, 'brasskey.jpg'),
    InventoryItems.SILVER_KEY: os.path.join(IMAGES, 'silverkey.jpg'),
    InventoryItems.GOLD_KEY: os.path.join(IMAGES, 'goldkey.jpg'),
    InventoryItems.GOLD: os.path.join(IMAGES, 'gold.jpg'),
    InventoryItems.PEGASUS: os.path.join(IMAGES, 'pegasus.jpg'),
    InventoryItems.WIZARD: os.path.join(IMAGES, 'wizard.jpg')
}

EVENT_IMAGES = {
    MoveEvent.DRAGON: os.path.join(IMAGES, 'dragon.jpg'),
    MoveEvent.DRAGON_KILL: os.path.join(IMAGES, 'sword.jpg'),
    MoveEvent.LOST: os.path.join(IMAGES, 'lost.jpg'),
    MoveEvent.LOST_SCOUT: os.path.join(IMAGES, 'scout.jpg'),
    MoveEvent.PLAGUE: os.path.join(IMAGES, 'plague.jpg'),
    MoveEvent.PLAGUE_HEALER: os.path.join(IMAGES, 'healer.jpg')
}