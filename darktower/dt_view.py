import os
import tkinter
import time
import re
from PIL import ImageTk, Image

RESOURCES = os.path.join(os.path.dirname(__file__), 'resources')
FONT = os.path.join(RESOURCES, 'font')
IMAGES = os.path.join(RESOURCES, 'images')
SOUNDS = os.path.join(RESOURCES, 'sounds')

class DTView(tkinter.Tk):
    def __init__(self, parent):
        tkinter.Tk.__init__(self, parent)
        self.parent = parent
        self.geometry("320x240")
        self.images = self.setup_images()
        self.initialize()

    def initialize(self):
        self.frames = {}
        self.frames['main'] = tkinter.Frame(self)
        self.frames['game'] = tkinter.Frame(self)
        self.frames['menu'] = tkinter.Frame(self)

        self.frames['main'].grid()




        self.setup_main_frame()
        self.setup_game_frame()

        #button = tkinter.Button(self.main_frame, text=u"Click Me !", command=self.on_button_click)
        #button.grid(column=0,row=0)

        #self.img = ImageTk.PhotoImage(Image.open(os.path.join(IMAGES, 'logo.gif')))
        #self.labelVar = tkinter.StringVar()
        #self.label = tkinter.Label(self.game_frame, textvariable=self.labelVar, image=self.img, anchor="w", fg="white", bg="blue")
        #self.label.grid(column=0, row=1, columnspan=2, sticky='Ew')

        #button = tkinter.Button(self.game_frame, text=u"Click Me !", command=self.show_main_frame)
        #button.grid(column=0, row=0)

    def setup_main_frame(self):
        main_frame = self.frames['main']
        button = tkinter.Button(main_frame, text=u"Click Me !", command=lambda: self.show_game())
        button.grid(column=0, row=0)
        self.img = ImageTk.PhotoImage(Image.open(os.path.join(IMAGES, 'logo.gif')))
        self.labelVar = tkinter.StringVar()
        self.label = tkinter.Label(
            main_frame, textvariable=self.labelVar,
            image=self.img, anchor="w", fg="white",
            bg="blue"
        )
        self.label.grid(column=0, row=1, columnspan=2, sticky='Ew')

    def setup_game_frame(self):
        game_frame = self.frames['game']

        button = tkinter.Button(game_frame, text=u"Click Me !", command=lambda: self.show_main())
        button.grid(column=0, row=0)

    def on_button_click(self):
        self.labelVar.set("button clicked")
        self.img = ImageTk.PhotoImage(Image.open(os.path.join(IMAGES, 'bazaar.gif')))
        self.label.configure(image=self.img)
        self.frames['main'].grid_forget()

    def show_game(self):
        self.show_frame('game')
        self.hide_frame('main')

    def show_main(self):
        self.show_frame('main')
        self.hide_frame('game')

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