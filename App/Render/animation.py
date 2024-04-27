import os

from tkinter import ttk
from tkinter import *
from PIL import Image, ImageTk
from App.Config.appInternalConsts import appPaths

class Animation:
    sprites = []
    img_pils = []
    current_id = 0
    binded_img_id = None

    def __init__(self, animationFolderName):
        self.path = appPaths.animationsDirPath + animationFolderName

    def load(self, w, h):

        directory = self.path
        elements = os.listdir(directory)
        files = [element for element in elements if os.path.isfile(os.path.join(directory, element))]

        self.img_pils = [Image.open(directory + "/" + e).resize((w, h), Image.LANCZOS) for e in files if e.endswith(".png")]
        self.sprites = [ImageTk.PhotoImage(img) for img in self.img_pils]

    def bindImage(self, img_id):
        self.binded_img_id = img_id

    def update(self, canvas):
        assert(self.binded_img_id != None)

        canvas.itemconfig(self.binded_img_id, image=self.getCurrentSprite())
        self.current_id = ((self.current_id + 1) % len(self.sprites))

    def getCurrentSprite(self):
        return self.sprites[self.current_id]

        
        
        
        
        