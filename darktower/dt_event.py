from enum import IntEnum

import pygame


def dt_event_num(num: int):
    return pygame.USEREVENT + 1 + num


class DTEvent(IntEnum):
    INTRO = dt_event_num(0)
    SELECT_DIFFICULTY = dt_event_num(1)
    SELECT_PLAYERS = dt_event_num(2)
    START_PLAYER_TURN = dt_event_num(3)
