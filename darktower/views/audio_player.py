import os

import pygame
from pygame.event import Event

from darktower.enums import DTEvent
from darktower.views.base_view import RESOURCES

SOUNDS = os.path.join(RESOURCES, 'sounds')


class AudioFile:
    INTRO = os.path.join(SOUNDS, 'intro.wav')
    BAZAAR = os.path.join(SOUNDS, 'bazaar.wav')


class AudioPlayer(object):
    def __init__(self):
        self.chunk = 1024
        pygame.mixer.init()

    def trigger_audio(self, event: Event):
        if event.type == DTEvent.INTRO:
            self.play_wave(AudioFile.INTRO, DTEvent.SELECT_DIFFICULTY)
        elif event.type == DTEvent.SELECT_BAZAAR:
            self.play_wave(AudioFile.BAZAAR, DTEvent.DO_NOTHING)

    @staticmethod
    def play_wave(audio_file: str, end_event):
        pygame.mixer.music.set_endevent(end_event)
        pygame.mixer.music.load(audio_file)
        pygame.mixer.music.play()

    def is_busy(self):
        return pygame.mixer.music.get_busy()



