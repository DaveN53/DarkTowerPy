import pygame
from pygame.event import Event

from darktower.enums import DTEvent


class EventManager:

    def __init__(self):
        self.event = DTEvent.INTRO

    @staticmethod
    def start():
        start_event = DTEvent.SELECT_BAZAAR
        intro_event = pygame.event.Event(start_event, {})
        pygame.event.post(intro_event)

    @staticmethod
    def is_view_event(event: Event):
        return event.type in list(map(int, DTEvent))
