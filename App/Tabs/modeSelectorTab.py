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

    background_filter_id = None

    def __init__(self, tab):
        self.tab = tab

        self.canvas = Canvas(self.tab, width = 800, height = 600)
        self.canvas.pack(fill="both", expand=True)

    def setUp(self, root):
        self.setBackground(root)
        self.setCheckboxes()
        self.displayEnumSelectors()
        self.setButtons()

    def setCheckboxes(self):
        self.lofi = BooleanVar()
        Checkbutton(self.canvas, text="Lofi", variable=self.lofi, justify=LEFT, command=self.onSelectCheckbox).place(x=30, y=360)
        #Checkbutton(self.canvas, text="Lofi", variable=self.lofi, justify=LEFT).grid(column=0, row=1)

        self.retro = BooleanVar()
        Checkbutton(self.canvas, text="Retro", variable=self.retro, justify=LEFT, command=self.onSelectCheckbox).place(x=30, y=400)
        #Checkbutton(self.canvas, text="Retro", variable=self.retro, justify=LEFT).grid(column=0, row=2)

        self.underWater = BooleanVar()
        Checkbutton(self.canvas, text="Bajo el agua", variable=self.underWater, justify=LEFT, command=self.onSelectCheckbox).place(x=30, y=440)
        #Checkbutton(self.canvas, text="Bajo el agua", variable=self.underWater, justify=LEFT).grid(column=0, row=3)

        self.spatial = BooleanVar()
        Checkbutton(self.canvas, text="Espacial", variable=self.spatial, justify=LEFT, command=self.onSelectCheckbox).place(x=30, y=480)
        #Checkbutton(self.canvas, text="Espacial", variable=self.spatial, justify=LEFT).grid(column=0, row=4)

    def setButtons(self):
      
        original_image = Image.open("App/Images/playButton.png")

        # Reduce el tamaño de la imagen
        resized_image = original_image.resize((100, 100), Image.LANCZOS) 
        self.playButtonImage = ImageTk.PhotoImage(resized_image)

        # Calcula las coordenadas para centrar el botón
        x = (800 - 100) / 2
        y = (600 - 100) / 2

        # Crea y coloca el botón en las coordenadas calculadas
        Button(self.canvas, image=self.playButtonImage).place(x=x, y=y)

        # Botón de todo aleatorio
        original_image = Image.open("App/Images/dado6.png")

        # Reduce el tamaño de la imagen
        resized_image = original_image.resize((80, 80), Image.LANCZOS) 
        self.generateAllRandom_buttonImage = ImageTk.PhotoImage(resized_image)

        # Calcula las coordenadas para centrar el botón
        x = 800 * 0.8
        y = 600 * 0.7

        # Crea y coloca el botón en las coordenadas calculadas
        Button(self.canvas, image=self.generateAllRandom_buttonImage).place(x=x, y=y)

    def displayEnumSelectors(self):
        self.current_tematic = StringVar()
        self.combo = ttk.Combobox(self.canvas, values=[option.value for option in TematicEnum],
                                  textvariable=self.current_tematic)

        self.combo.bind("<<ComboboxSelected>>", self.selectTematic)
        #self.combo.grid(column=3, row=0, padx=10, pady= 40)
        self.combo.place(x=500, y= 80)

        print("combobox packed")

    def selectTematic(self, event):
        # Guardamos la temática seleccionada en el evento
        print("Seleccionado: ",self.current_tematic.get())

    def onSelectCheckbox(self):
        if(self.underWater.get()):
            self.background_filter_pil = Image.open("App/Images/filterBlue.png")
            self.background_filter = ImageTk.PhotoImage(self.background_filter_pil)
            self.background_filter_id = self.canvas.create_image(0, 0, anchor="nw", image=self.background_filter)
        else:
            self.canvas.delete(self.background_filter_id)

    def setBackground(self, root):   

        # Cargar la imagen original
        self.background_image_pil = Image.open("App/Images/DarkRiders.png")
        
        # Crear una instancia de ImageTk para la imagen original
        self.background = ImageTk.PhotoImage(self.background_image_pil)
        
        # Crear la imagen en el canvas
        self.background_id = self.canvas.create_image(0, 0, anchor="nw", image=self.background)
        
        # Enlazar la función resize_image al evento de cambio de tamaño de la ventana
        root.bind("<Configure>", self.resize_image)

    def resize_image(self, event):
        # Redimensionar la imagen original cuando cambia el tamaño de la ventana
        new_width = event.width
        new_height = event.height
        resized_image_pil = self.background_image_pil.resize((new_width, new_height), Image.LANCZOS)
        self.background = ImageTk.PhotoImage(resized_image_pil)
        self.canvas.itemconfig(self.background_id, image=self.background)