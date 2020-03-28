import os

import pygame
from pygame.event import Event

from darktower.dt_event import DTEvent
from darktower.views.base_view import RESOURCES

SOUNDS = os.path.join(RESOURCES, 'sounds')


class AudioFile:
    INTRO = os.path.join(SOUNDS, 'intro.wav')


class AudioPlayer(object):
    def __init__(self):
        self.chunk = 1024
        pygame.mixer.init()

    def trigger_audio(self, event: Event):
        if event.type == DTEvent.INTRO:
            self.play_wave(AudioFile.INTRO, DTEvent.SELECT_DIFFICULTY)

    @staticmethod
    def play_wave(audio_file: str, end_event: DTEvent =None):
        if end_event:
            pygame.mixer.music.set_endevent(end_event)

        pygame.mixer.music.load(audio_file)
        pygame.mixer.music.play()

    def is_busy(self):
        return pygame.mixer.music.get_busy()



