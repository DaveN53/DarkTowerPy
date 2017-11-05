import pygame


class AudioPlayer(object):
    def __init__(self):
        self.chunk = 1024
        pygame.mixer.init()

    def play_wave(self, filename):
        pygame.mixer.music.load(filename)
        pygame.mixer.music.play()

    def is_busy(self):
        return pygame.mixer.music.get_busy()
