import sys
sys.path.append('././Reaper_Scripts/')

from tkinter import ttk
from tkinter import *
from enum import Enum

from PIL import Image, ImageTk
from Reaper_Scripts import llamamosReaper

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
    ROCK      =   "Rock"
    POP       =   "Pop"
    TECNO     =   "Tecno"

class ModeSelectorTab:

    current_tematic = TematicEnum.PRADERA

    background_filter_id = None

    def __init__(self, tab):
        self.tab = tab

        self.canvas = Canvas(self.tab, width = 800, height = 600)
        self.canvas.pack(fill="both", expand=True)

    def setUp(self, root):
        self.root = root
        self.setBackground("0_0")
        self.setCheckboxes()
        self.displayEnumSelectors()
        self.setButtons()

    def onEntryTab(self):
        self.resize_image()

    def setCheckboxes(self):
        self.retro = BooleanVar()
        Checkbutton(self.canvas, text="Retro", variable=self.retro, justify=LEFT, command=self.onSelectCheckbox).place(x=30, y=280)

        self.underWater = BooleanVar()
        Checkbutton(self.canvas, text="Bajo el agua", variable=self.underWater, justify=LEFT, command=self.onSelectCheckbox).place(x=30, y=320)

        self.lofi = BooleanVar()
        Checkbutton(self.canvas, text="Lofi", variable=self.lofi, justify=LEFT, command=self.onSelectCheckbox).place(x=30, y=360)

        self.vintage = BooleanVar()
        Checkbutton(self.canvas, text="Vintage", variable=self.vintage, justify=LEFT, command=self.onSelectCheckbox).place(x=30, y=440)
 
        self.dream = BooleanVar()
        Checkbutton(self.canvas, text="Dream", variable=self.dream, justify=LEFT, command=self.onSelectCheckbox).place(x=30, y=480)
    
        self.spatial = BooleanVar()
        Checkbutton(self.canvas, text="Espacial", variable=self.spatial, justify=LEFT, command=self.onSelectCheckbox).place(x=30, y=400)
   
    def setButtons(self):
      
        original_image = Image.open("App/Images/playButton.png")

        # Reduce el tamaño de la imagen
        resized_image = original_image.resize((100, 100), Image.LANCZOS) 
        self.playButtonImage = ImageTk.PhotoImage(resized_image)

        # Calcula las coordenadas para centrar el botón
        x = (800 - 100) / 2
        y = (600 - 100) / 2

        # Crea y coloca el botón en las coordenadas calculadas
        Button(self.canvas, image=self.playButtonImage, command=self.playReaper).place(x=x, y=y)

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

        if(self.spatial.get()):
            self.setBackground("espacial")
        else:
            if(self.retro.get()):
                if(self.underWater.get()):    
                    self.setBackground("0_3")
                else:
                    self.setBackground("0_1")
            elif(self.underWater.get()):    
                self.setBackground("0_2")

            if(self.lofi.get()):
                self.background_lofi_pil = Image.open("App/Images/Backgrounds/lofi.png")
                self.background_lofi = ImageTk.PhotoImage(self.background_lofi_pil)
                self.background_lofi_id = self.canvas.create_image(0, 0, anchor="nw", image=self.background_lofi)
            else:
                self.canvas.delete(self.background_lofi_id)
            
            if(self.vintage.get()):
                self.background_vintage_pil = Image.open("App/Images/Backgrounds/vintage.png")
                self.background_vintage = ImageTk.PhotoImage(self.background_vintage_pil)
                self.background_vintage_id = self.canvas.create_image(0, 0, anchor="nw", image=self.background_vintage)
            else:
                self.canvas.delete(self.background_vintage_id)

            if(self.dream.get()):
                self.background_dream_pil = Image.open("App/Images/Backgrounds/dream.png")
                self.background_dream = ImageTk.PhotoImage(self.background_dream_pil)
                self.background_dream_id = self.canvas.create_image(0, 0, anchor="nw", image=self.background_dream)
            else:
                self.canvas.delete(self.background_dream_id)

    def setBackground(self, image):   

        # Cargar la imagen original
        self.background_image_pil = Image.open("App/Images/Backgrounds/"+ image +".png")
        
        # Crear una instancia de ImageTk para la imagen original
        self.background = ImageTk.PhotoImage(self.background_image_pil)
        
        # Crear la imagen en el canvas
        self.background_id = self.canvas.create_image(0, 0, anchor="nw", image=self.background)
        
        # Enlazar la función resize_image al evento de cambio de tamaño de la ventana
        self.root.bind("<Configure>", self.resize_image)

    def resize_image(self, event = None):
        # Redimensionar la imagen original cuando cambia el tamaño de la ventana
        new_width = self.tab.winfo_width()
        new_height = self.tab.winfo_height()
        resized_image_pil = self.background_image_pil.resize((new_width, new_height), Image.LANCZOS)
        self.background = ImageTk.PhotoImage(resized_image_pil)
        self.canvas.itemconfig(self.background_id, image=self.background)

    def playReaper(self):
        reaperStream = llamamosReaper.ReaperStream()
        reaperStream.SetUp()

        
