import json
import os

from tkinter import ttk
from tkinter import *
from enum import Enum

from PIL import Image, ImageTk
from Reaper_Scripts import llamamosReaper
from App.AppState.modeState import ModeState
from App.AppState.tooltip import Tooltip
from App.AppState.presetsManager import PresetManager
from Utils import globalConsts

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
        self.displayPresetSelector()
        self.setButtons()

        self.recoverStateFromFile()

        # Enlazar la función resize_image al evento de cambio de tamaño de la ventana
        self.root.bind("<Configure>", self.resize_image)

        self.reaperStream = llamamosReaper.ReaperStream()
        self.presetManager = PresetManager()


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
        Checkbutton(self.canvas, text="Vintage", variable=self.vintage, justify=LEFT, command=self.onSelectCheckbox).place(x=30, y=400)
 
        self.dream = BooleanVar()
        Checkbutton(self.canvas, text="Dream", variable=self.dream, justify=LEFT, command=self.onSelectCheckbox).place(x=30, y=440)
    
        self.spatial = BooleanVar()
        Checkbutton(self.canvas, text="Espacial", variable=self.spatial, justify=LEFT, command=self.onSelectCheckbox).place(x=30, y=480)
   
    def setButtons(self):
      
        original_image = Image.open("App/Images/playButton.png")

        # Reduce el tamaño de la imagen
        resized_image = original_image.resize((100, 100), Image.LANCZOS) 
        self.playButtonImage = ImageTk.PhotoImage(resized_image)

        # Calcula las coordenadas para centrar el botón
        x = (800 - 100) / 2
        y = (600 - 100) / 2

        # Crea y coloca el botón en las coordenadas calculadas
        self.playButton = ttk.Button(self.canvas, image=self.playButtonImage, command=self.playReaper)
        self.playButton.place(x=x, y=y)

        playTooltip = Tooltip(self.playButton, "Apply changes and play")

        self.playButton.bind("<Enter>", playTooltip.show_tooltip)
        self.playButton.bind("<Leave>", playTooltip.hide_tooltip)

        #  -----------  Botón de todo aleatorio ---------------
        original_image = Image.open("App/Images/dado6.png")

        # Reduce el tamaño de la imagen
        resized_image = original_image.resize((80, 80), Image.LANCZOS) 
        self.generateAllRandom_buttonImage = ImageTk.PhotoImage(resized_image)

        # Calcula las coordenadas para centrar el botón
        x = 800 * 0.8
        y = 600 * 0.7

        # Crea y coloca el botón en las coordenadas calculadas
        Button(self.canvas, image=self.generateAllRandom_buttonImage).place(x=x, y=y)

        #  -----------  Botón de guardar presets ---------------
        original_image = Image.open("App/Images/saveIcon.png")
        resized_image = original_image.resize((30, 30), Image.LANCZOS) 
        self.savePreset_image = ImageTk.PhotoImage(resized_image)

        x = 800 * 0.85
        y = 600 * 0.04

        self.savePreset_button = Button(self.canvas, image=self.savePreset_image, command=self.savePresetAction)
        self.savePreset_button.place(x=x, y=y)

        savePreset_tooltip = Tooltip(self.savePreset_button, "Save preset")
        self.savePreset_button.bind("<Enter>", savePreset_tooltip.show_tooltip)
        self.savePreset_button.bind("<Leave>", savePreset_tooltip.hide_tooltip)


    def displayEnumSelectors(self):
        self.current_tematic = StringVar()
        self.combo = ttk.Combobox(self.canvas, values=[option.value for option in TematicEnum],
                                  textvariable=self.current_tematic, state="readonly")

        self.combo.bind("<<ComboboxSelected>>", self.selectTematic)
        #self.combo.grid(column=3, row=0, padx=10, pady= 40)
        self.combo.place(x=500, y= 80)

        print("combobox packed")

    def displayPresetSelector(self):
        directory = PresetManager.presetsPath
        elements = os.listdir(directory)
        files = [elemento for elemento in elements if os.path.isfile(os.path.join(directory, elemento))]
        jsonFiles = [e for e in files if e.endswith(".json")]

        if len(jsonFiles) < 1:
            return
        filesWithNoExtension = [os.path.splitext(archivo)[0] for archivo in jsonFiles]
        self.presetName = StringVar()
        self.presetCombobox = ttk.Combobox(self.canvas, values=filesWithNoExtension,
                                  textvariable=self.presetName, state="readonly")
        self.presetCombobox.place(x=0, y=0)
        self.presetCombobox.bind("<<ComboboxSelected>>", self.recoverPresetAction)

        tooltip = Tooltip(self.presetCombobox, "Saved presets")
        self.presetCombobox.bind("<Enter>", tooltip.show_tooltip)
        self.presetCombobox.bind("<Leave>", tooltip.hide_tooltip)


    def selectTematic(self, event):
        # Guardamos la temática seleccionada en el evento
        tematic = self.current_tematic.get()
        print("Seleccionado: ", tematic)

        self.modeState.tematica = [member.value for member in TematicEnum].index(tematic)
        print(self.modeState.tematica)

    def onSelectCheckbox(self):
        self.modeState.agua = self.underWater.get()
        self.modeState.retro = self.retro.get()
        self.modeState.lofi = self.lofi.get()
        self.modeState.vintage = self.vintage.get()
        self.modeState.espacial = self.spatial.get()
        self.modeState.dream = self.dream.get()

        # if(self.spatial.get()):
        #     self.setBackground("espacial")
        # else:
        #     if(self.retro.get()):
        #         if(self.underWater.get()):    
        #             self.setBackground("0_3")
        #         else:
        #             self.setBackground("0_1")
        #     elif(self.underWater.get()):    
        #         self.setBackground("0_2")

        #     if(self.lofi.get()):
        #         self.background_lofi_pil = Image.open("App/Images/Backgrounds/lofi.png")
        #         self.background_lofi = ImageTk.PhotoImage(self.background_lofi_pil)
        #         self.background_lofi_id = self.canvas.create_image(0, 0, anchor="nw", image=self.background_lofi)
        #     else:
        #         self.canvas.delete(self.background_lofi_id)
            
        #     if(self.vintage.get()):
        #         self.background_vintage_pil = Image.open("App/Images/Backgrounds/vintage.png")
        #         self.background_vintage = ImageTk.PhotoImage(self.background_vintage_pil)
        #         self.background_vintage_id = self.canvas.create_image(0, 0, anchor="nw", image=self.background_vintage)
        #     else:
        #         self.canvas.delete(self.background_vintage_id)

        #     if(self.dream.get()):
        #         self.background_dream_pil = Image.open("App/Images/Backgrounds/dream.png")
        #         self.background_dream = ImageTk.PhotoImage(self.background_dream_pil)
        #         self.background_dream_id = self.canvas.create_image(0, 0, anchor="nw", image=self.background_dream)
        #     else:
        #         self.canvas.delete(self.background_dream_id)
        self.resize_image()

    def setBackground(self, image):   

        # Cargar la imagen original
        self.background_image_pil = Image.open("App/Images/Backgrounds/"+ image +".png")
        
        # Crear una instancia de ImageTk para la imagen original
        self.background = ImageTk.PhotoImage(self.background_image_pil)
        
        # Crear la imagen en el canvas
        self.background_id = self.canvas.create_image(0, 0, anchor="nw", image=self.background)   
       

    def resize_image(self, event = None):
        # Redimensionar la imagen original cuando cambia el tamaño de la ventana
        new_width = self.tab.winfo_width()
        new_height = self.tab.winfo_height()
        resized_image_pil = self.background_image_pil.resize((new_width, new_height), Image.LANCZOS)
        self.background = ImageTk.PhotoImage(resized_image_pil)
        self.canvas.itemconfig(self.background_id, image=self.background)

    def playReaper(self):
        self.saveState()

        self.reaperStream.SetUp()

    def recoverState(self, modeState):
        self.modeState = modeState

        self.lofi.set(self.modeState.lofi)
        self.vintage.set(self.modeState.vintage)
        self.spatial.set(self.modeState.espacial)
        self.underWater.set(self.modeState.agua)
        self.retro.set(self.modeState.retro)
        self.dream.set(self.modeState.dream)

        tematica_value = list(TematicEnum)[self.modeState.tematica].value
        self.current_tematic.set(tematica_value)

    def recoverStateFromFile(self):
        jsonPath = globalConsts.Paths.mediaSettings
        modeState = ModeState.fromJSON(jsonPath)
        self.recoverState(modeState)

    def saveState(self):
        jsonPath = globalConsts.Paths.mediaSettings
        dataJSONString = self.modeState.toJSON()

        # Abre el archivo JSON en modo escritura
        with open(jsonPath, "w") as archivo:
            json.dump(dataJSONString, archivo, indent=4)

    def savePresetAction(self):
        self.presetManager.show_save_preset_popup(tab = self.tab, modeState=self.modeState)

    def recoverPresetAction(self, event=None):
        self.modeState = self.presetManager.recoverPreset(self.presetName.get())
        self.recoverState(self.modeState)
        