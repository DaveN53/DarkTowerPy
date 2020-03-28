from enum import IntEnum

import pygame


def dt_event_num(num: int):
    return pygame.USEREVENT + 1 + num


class DTEvent(IntEnum):
    INTRO = dt_event_num(0)
    SELECT_DIFFICULTY = dt_event_num(1)
    SELECT_PLAYERS = dt_event_num(2)
    START_PLAYER_TURN = dt_event_num(3)
    SELECT_BAZAAR = dt_event_num(4)
    SELECT_TOMB_RUIN = dt_event_num(5)
    SELECT_MOVE = dt_event_num(6)
    SELECT_SANCTUARY_CITADEL = dt_event_num(7)
    SELECT_DARK_TOWER = dt_event_num(8)
    SELECT_FRONTIER = dt_event_num(9)
    SELECT_INVENTORY = dt_event_num(10)
    SHOW_INVENTORY = dt_event_num(11)


class BazaarItems(IntEnum):
    FOOD = 0
    WARRIOR = 1
    BEAST = 2
    SCOUT = 3
    HEALER = 4
