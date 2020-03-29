import pygame

from darktower.enums import DTEvent, DTUserEvent, AudioFile


class AudioPlayer(object):
    def __init__(self):
        self.audio_end_event = None
        pygame.mixer.init()

    def trigger_audio(self, event: DTEvent):
        if event == DTEvent.INTRO:
            self.play_wave(AudioFile.INTRO)
            self.audio_end_event = DTEvent.SELECT_DIFFICULTY
        elif event == DTEvent.SELECT_BAZAAR:
            self.play_wave(AudioFile.BAZAAR)
            self.audio_end_event = DTEvent.DO_NOTHING
        elif event == DTEvent.BAZAAR_CLOSED:
            self.play_wave(AudioFile.BAZAAR_CLOSED)
            self.audio_end_event = DTEvent.START_PLAYER_TURN

    @staticmethod
    def play_wave(audio_file: str):
        pygame.mixer.music.set_endevent(DTUserEvent.MUSIC_END)
        pygame.mixer.music.load(audio_file)
        pygame.mixer.music.play()

    def end_event_available(self):
        if type(self.audio_end_event) is DTEvent:
            return True
        return False

    def consume_audio_end_event(self):
        event = self.audio_end_event
        self.audio_end_event = None
        return event

    def is_busy(self):
        return pygame.mixer.music.get_busy()



