import pygame

from darktower.dt_game_display import DTGameDisplay
from darktower.views.audio_player import AudioPlayer
from darktower.views.event_manager import EventManager
from darktower.views.view_manager import ViewManager


class DTMain(object):
    def __init__(self):
        self.dt_game_display = DTGameDisplay()
        self.view_manager = ViewManager(self.dt_game_display)
        self.audio_player = AudioPlayer()
        self.event_manager = EventManager(self.dt_game_display, self.view_manager, self.audio_player)
        self.clock = pygame.time.Clock()

    def run_game(self):
        pygame.init()

        self.event_manager.start()

        run_game = True
        while run_game:
            event = pygame.event.poll()
            if event.type == pygame.QUIT:
                break

            if event.type == pygame.MOUSEBUTTONUP:
                print(event)

            self.dt_game_display.current_event = event
            self.event_manager.consume_event(event)
            self.view_manager.display()

            self.clock.tick()

    def exit_game(self):
        pygame.quit()


if __name__ == "__main__":
    print('initializing')
    app = DTMain()
    print('running')
    app.run_game()
    print('exiting')
    app.exit_game()
