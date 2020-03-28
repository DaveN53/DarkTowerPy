import pygame


class DTGameDisplay:
    def __init__(self):
        self.width = 320
        self.height = 240
        self.current_event = None
        pygame.init()
        self.game = pygame.display.set_mode((self.width, self.height))
        pygame.display.set_caption('Dark Tower')
        self.difficulty = None
        self.num_players = None
        self.current_player = 0



