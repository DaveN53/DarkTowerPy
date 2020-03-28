from darktower.dt_game_display import DTGameDisplay
from darktower.views.view_factory import ViewFactory


class ViewManager:
    def __init__(self, game_display: DTGameDisplay):
        self.game_display = game_display
        self.view_factory = ViewFactory(self.game_display)
        self.views = {}
        self.event = None

    def update(self, event):
        self.event = event

    def display(self):
        if not self.event:
            return

        event_value = self.event.type

        view = self.views.get(event_value)
        if not view:
            view = self.view_factory.build_view(event_value)
            self.views[event_value] = view

        view.display()
