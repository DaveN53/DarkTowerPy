from darktower.dt_view import DTView


class DTCore(object):
    def __init__(self):
        self.main_view = DTView(None)
        self.main_view.title('Dark Tower')

    def start_game(self):
        self.main_view.mainloop()


if __name__ == "__main__":
    app = DTCore()
    app.start_game()