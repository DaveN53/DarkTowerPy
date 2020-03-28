import os
import re
from tkinter import *

from PIL import ImageTk, Image


RESOURCES = os.path.join(os.path.dirname(__file__), 'resources')
FONT = os.path.join(RESOURCES, 'font')
IMAGES = os.path.join(RESOURCES, 'images')
SOUNDS = os.path.join(RESOURCES, 'sounds')


class DTView(Frame):
    def __init__(self, parent):
        Frame.__init__(self, parent)
        self.parent = parent
        self.width = 320
        self.height = 240
        parent.geometry("{}x{}".format(self.width, self.height))
        parent.overrideredirect(1)
        self.images = self.setup_images()
        #self.audio_player = AudioPlayer()
        self.frames = {}
        self.initialize()

    def initialize(self):
        self.frames['main'] = Frame(self)
        self.frames['diff'] = Frame(self)
        self.frames['game'] = Frame(self)
        self.frames['menu'] = Frame(self)

        self.show_main()

        self.setup_main_frame()
        self.setup_diff_frame()
        self.setup_game_frame()

        #self.audio_player.play_wave(os.path.join(SOUNDS, 'darktower.wav'))

        self.after(3500, self.show_diff)

    def setup_main_frame(self):
        main_frame = self.frames['main']
        self.img = ImageTk.PhotoImage(Image.open(os.path.join(IMAGES, 'logo.png')))
        self.label = Label(main_frame, image=self.img, fg="black", bg="black")
        self.label.grid(column=0, row=0)

    def setup_diff_frame(self):
        diff_frame = self.frames['diff']
        diff_frame.grid_columnconfigure(1, weight=1)
        label = Label(diff_frame, text='Select Difficulty')
        easy_button = Button(diff_frame, text=u'Level One')
        med_button = Button(diff_frame, text=u'Level Two')
        hard_button = Button(diff_frame, text=u'Level Three')
        label.grid_columnconfigure(1, weight=1)
        label.grid()

        easy_button.grid(sticky=N+S+E+W)
        med_button.grid(sticky=N+S+E+W)
        hard_button.grid(sticky=N+S+E+W)

        self.hide_frame('diff')

    def setup_game_frame(self):
        game_frame = self.frames['game']

        button = Button(game_frame, text=u"Click Me !", command=lambda: self.show_main())
        button.grid(column=0, row=0)

        self.hide_frame('game')

    def on_button_click(self):
        self.labelVar.set("button clicked")
        self.img = ImageTk.PhotoImage(Image.open(os.path.join(IMAGES, 'bazaar.gif')))
        self.label.configure(image=self.img)
        self.frames['main'].grid_forget()

    def show_main(self):
        self.show_frame('main')
        self.hide_frame('game')
        self.hide_frame('diff')

    def show_diff(self):
        self.show_frame('diff')
        self.hide_frame('main')
        self.hide_frame('game')

    def show_game(self):
        self.show_frame('game')
        self.hide_frame('main')
        self.hide_frame('diff')

    def show_frame(self, frame_name):
        self.frames[frame_name].grid()

    def hide_frame(self, frame_name):
        self.frames[frame_name].grid_forget()

    def setup_images(self):
        image_dict = {}
        for image in os.listdir(IMAGES):
            match = re.search('(.*)\.', image)
            image_dict[match.group(1)] = image
        return image_dict
