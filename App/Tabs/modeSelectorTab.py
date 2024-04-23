import json
import os
import random

from tkinter import ttk
from tkinter import *
from enum import Enum

from PIL import Image, ImageTk
from Reaper_Scripts import llamamosReaper
from App.AppState.modeState import ModeState
from App.AppState.tooltip import Tooltip
from App.AppState.presetsManager import PresetManager
from App.AppState.backgroundSystem import BackgroundSystem
from App.AppEnums.tematicEnum import TematicEnum
from Utils import globalConsts
from Utils import stringUtils

class ModeSelectorTab:

    current_tematic = TematicEnum.PRADERA

    background_filter_id = None

    def __init__(self, tab):
        self.tab = tab

        self.canvas = Canvas(self.tab, width = 800, height = 600)
        self.canvas.pack(fill="both", expand=True)

    def setUp(self, root):
        self.root = root
        self.backgroundSys = BackgroundSystem()
        self.setCheckboxes()
        self.displayEnumSelectors()
        self.displayPresetSelector()
        self.setButtons()

        self.recoverStateFromFile()
        self.setBackground()

        # Enlazar la función resize_image al evento de cambio de tamaño de la ventana
        self.root.bind("<Configure>", self.resize_image)

        self.reaperStream = llamamosReaper.ReaperStream()
        self.presetManager = PresetManager()
        self.rerollSeed()


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
        Button(self.canvas, image=self.generateAllRandom_buttonImage, command=self.rerollSeed).place(x=x, y=y)

        self.seedString = StringVar()
        self.seedEntry = Entry(self.canvas, textvariable=self.seedString, justify="center")
        self.seedEntry.place(x=x, y=y-20, width=80)
        self.seedEntry.bind("<KeyRelease>", self.onUpdateSeed)

        seed_tooltip = Tooltip(self.seedEntry, "Seed")
        self.seedEntry.bind("<Enter>", seed_tooltip.show_tooltip)
        self.seedEntry.bind("<Leave>", seed_tooltip.hide_tooltip)
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
        
        self.presetName = StringVar()
        self.presetCombobox = ttk.Combobox(self.canvas, values=None,
                                  textvariable=self.presetName, state="readonly")
        self.presetCombobox.place(x=0, y=0)
        self.refreshPresets()
        self.presetCombobox.bind("<<ComboboxSelected>>", self.recoverPresetAction)

        tooltip = Tooltip(self.presetCombobox, "Saved presets")
        self.presetCombobox.bind("<Enter>", tooltip.show_tooltip)
        self.presetCombobox.bind("<Leave>", tooltip.hide_tooltip)

        original_image = Image.open("App/Images/saveIcon.png")
        resized_image = original_image.resize((30, 30), Image.LANCZOS) 
        self.redreshButton_Image = ImageTk.PhotoImage(resized_image)


    def selectTematic(self, event):
        # Guardamos la temática seleccionada en el evento
        tematic = self.current_tematic.get()
        print("Seleccionado: ", tematic)

        self.modeState.tematica = self.NameEnumToId(tematic)
        self.setBackground()
        self.resize_image()

    def onSelectCheckbox(self):
        self.modeState.agua = self.underWater.get()
        self.modeState.retro = self.retro.get()
        self.modeState.lofi = self.lofi.get()
        self.modeState.vintage = self.vintage.get()
        self.modeState.espacial = self.spatial.get()
        self.modeState.dream = self.dream.get()

        self.setBackground()
        self.resize_image()

    def setBackground(self):   

        # Cargar la imagen original
        #self.background_image_pil = Image.open("App/Images/Backgrounds/"+ image +".png")
        
        themeName = self.idToEnumValue(self.modeState.tematica)
        self.background_image_pil = self.backgroundSys.configure_background(theme=themeName, 
                                                                dream= self.modeState.dream,
                                                                lofi=self.modeState.lofi,
                                                                vintage=self.modeState.vintage,
                                                                spacial=self.modeState.espacial)[0]
        
        self.background = ImageTk.PhotoImage(self.background_image_pil)
        
        # Crear la imagen en el canvas
        self.background_id = self.canvas.create_image(0, 0, anchor="nw", image=self.background)   
       

    def resize_image(self, event = None):
        if(self.background_image_pil == None):
            return
        # Redimensionar la imagen original cuando cambia el tamaño de la ventana
        new_width = self.tab.winfo_width()
        new_height = self.tab.winfo_height()
        resized_image_pil = self.background_image_pil.resize((new_width, new_height), Image.LANCZOS)
        self.background = ImageTk.PhotoImage(resized_image_pil)
        self.canvas.itemconfig(self.background_id, image=self.background)

    def playReaper(self):
        self.modeState.seed = self.seedString.get()
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
        self.seedString.set(self.modeState.seed)
        
        tematica_value = self.idToEnumValue(self.modeState.tematica)
        self.current_tematic.set(tematica_value)

    def idToEnumValue(self, id):
        return list(TematicEnum)[id].value
    
    def NameEnumToId(self, themeName):
        return [member.value for member in TematicEnum].index(themeName)

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
        self.presetManager.show_save_preset_popup(tab = self.tab, modeState=self.modeState, onSavedCallback=self.refreshPresets)

    def recoverPresetAction(self, event=None):
        self.modeState = self.presetManager.recoverPreset(self.presetName.get())
        self.recoverState(self.modeState)

    def refreshPresets(self):
        directory = PresetManager.presetsPath
        elements = os.listdir(directory)
        files = [elemento for elemento in elements if os.path.isfile(os.path.join(directory, elemento))]
        jsonFiles = [e for e in files if e.endswith(".json")]

        filesWithNoExtension = [os.path.splitext(archivo)[0] for archivo in jsonFiles]

        self.presetCombobox['values'] = filesWithNoExtension
        self.presetCombobox.update()
        
    def rerollSeed(self):
        self.seedString.set(stringUtils.generate_random_string(5, None))
        self.modeState.seed = self.seedString.get()

    def onUpdateSeed(self, event):
        self.modeState.seed = self.seedString.get()