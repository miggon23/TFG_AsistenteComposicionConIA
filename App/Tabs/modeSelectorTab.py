from tkinter import ttk
from tkinter import *
from enum import Enum

from PIL import Image, ImageTk


class TematicEnum(Enum):
    PRADERA   =   "Pradera"
    PIANO     =   "Piano"
    DESIERTO  =   "Desierto"
    NIEVE	  =   "Nieve"
    PIRATA    =   "Pirata"
    SELVA     =   "Selva"
    ÉPICO     =   "Épico"
    TENEBROSO =   "Tenebroso"
    AGUA      =   "Agua"
    ASIATICO  =   "Asiático"

class ModeSelectorTab:

    current_tematic = TematicEnum.PRADERA

    def __init__(self, tab):
        self.tab = tab

        self.canvas = Canvas(self.tab, width = 800, height = 600)
        self.canvas.place(x=0, y=0)

    def setUp(self, root):
        self.setBackground(root)
        self.displayEnumSelectors()

    def displayEnumSelectors(self):
        self.current_tematic = StringVar()
        self.combo = ttk.Combobox(self.tab, values=[option.value for option in TematicEnum],
                                  textvariable=self.current_tematic)

        self.combo.bind("<<ComboboxSelected>>", self.selectTematic)
        self.combo.place(x=100, y=100)
        print("combobox packed")

    def selectTematic(self, event):
        # Guardamos la temática seleccionada en el evento
        print("Seleccionado: ",self.current_tematic.get())


    def setBackground(self, root):   

        # Cargar la imagen original
        self.background_image_pil = Image.open("App/Images/DarkRiders.png")
        
        # Crear una instancia de ImageTk para la imagen original
        self.background = ImageTk.PhotoImage(self.background_image_pil)
        
        # Crear la imagen en el canvas
        self.background_id = self.canvas.create_image(0, 0, anchor="nw", image=self.background)

        #self.background_filter_pil = Image.open("App/Images/filterBlue.png")
        #self.background_filter = ImageTk.PhotoImage(self.background_filter_pil)
        #self.background_filter_id = self.canvas.create_image(0, 0, anchor="nw", image=self.background_filter)
        
        # Enlazar la función resize_image al evento de cambio de tamaño de la ventana
        root.bind("<Configure>", self.resize_image)

    def resize_image(self, event):
        # Redimensionar la imagen original cuando cambia el tamaño de la ventana
        new_width = event.width
        new_height = event.height
        resized_image_pil = self.background_image_pil.resize((new_width, new_height), Image.LANCZOS)
        self.background = ImageTk.PhotoImage(resized_image_pil)
        self.canvas.itemconfig(self.background_id, image=self.background)