from darktower.dt_view import DTView
import tkinter


class DTMain(object):
    def __init__(self):
        self.root = tkinter.Tk()
        self.root.title('Dark Tower')
        self.main_frame = DTView(self.root)
        self.main_frame.grid()


    def start_game(self):
        self.root.mainloop()


if __name__ == "__main__":
    app = DTMain()
    app.start_game()