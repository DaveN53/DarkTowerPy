from darktower.dt_game_display import DTGameDisplay
from darktower.enums import DTEvent
from darktower.views.view_factory import ViewFactory


class ViewManager:
    def __init__(self, game_display: DTGameDisplay):
        self.game_display = game_display
        self.view_factory = ViewFactory(self.game_display)
        self.views = {}
        self.dt_event = None
        self.current_view = None
        self.extra_args = None

    def update(self, dt_event: DTEvent, **extra_args):
        if dt_event == DTEvent.DO_NOTHING:
            return

        self.dt_event = dt_event
        self.extra_args = extra_args

        if dt_event == DTEvent.END_TURN:
            self.dt_event = DTEvent.START_PLAYER_TURN

        self.current_view = self.views.get(self.dt_event)

        if self.current_view:
            self.current_view.refresh(**extra_args)

    def display(self):
        if type(self.dt_event) is not DTEvent:
            return

        if not self.current_view:
            self.current_view = self.view_factory.build_view(self.dt_event, **self.extra_args)
            self.views[self.dt_event] = self.current_view

        self.current_view.display()
