import json
import os
import random

from tkinter import ttk
from tkinter import *
from enum import Enum
from tktooltip import ToolTip

from PIL import Image, ImageTk
from Reaper_Scripts import llamamosReaper
from App.AppState.modeState import ModeState
# from App.AppState.tooltip import Tooltip
from App.AppState.presetsManager import PresetManager
from App.AppState.backgroundSystem import BackgroundSystem
from App.AppEnums.tematicEnum import TematicEnum
from App.AppEnums.reverbModesEnum import ReverbEnum
from Utils import globalConsts
from Utils import stringUtils

class ModeSelectorTab:
    tooltip_delay = 0.6 # En segundos
    current_tematic = TematicEnum.PRADERA

    background_filter_id = None

    def __init__(self, tab):
        self.tab = tab

        self.canvas = Canvas(self.tab, width = 1152, height = 648)
        self.canvas.pack(fill="both", expand=True)

    def setUp(self, root):
        self.root = root
        self.backgroundSys = BackgroundSystem(self.canvas, self.tab)
        self.backgroundSys.init()
        self.setCheckboxes()
        self.displayEnumSelectors()
        self.displayPresetSelector()
        self.setButtons()

        self.recoverStateFromFile()
        self.setBackground()
        self.setTooltips()
        # Enlazar la función resize_image al evento de cambio de tamaño de la ventana
        # self.root.bind("<Configure>", self.resize_image)

        self.reaperStream = llamamosReaper.ReaperStream()
        self.presetManager = PresetManager()
        self.rerollSeed()

    def update(self):
        self.backgroundSys.update()
        
    def onEntryTab(self):
        self.resize_image()

    def setCheckboxes(self):
        self.retro = BooleanVar()
        Checkbutton(self.canvas, text="Retro", variable=self.retro, justify=LEFT, command=self.onSelectCheckbox, selectcolor="black").place(x=30, y=310)

        self.underWater = BooleanVar()
        Checkbutton(self.canvas, text="Bajo el agua", variable=self.underWater, justify=LEFT, command=self.onSelectCheckbox, selectcolor="black").place(x=30, y=350)

        self.lofi = BooleanVar()
        Checkbutton(self.canvas, text="Lofi", variable=self.lofi, justify=LEFT, command=self.onSelectCheckbox, selectcolor="black").place(x=30, y=390)

        self.vintage = BooleanVar()
        Checkbutton(self.canvas, text="Vintage", variable=self.vintage, justify=LEFT, command=self.onSelectCheckbox, selectcolor="black").place(x=30, y=430)
 
        self.dream = BooleanVar()
        Checkbutton(self.canvas, text="Dream", variable=self.dream, justify=LEFT, command=self.onSelectCheckbox, selectcolor="black").place(x=30, y=470)
    
        self.spatial = BooleanVar()
        Checkbutton(self.canvas, text="Espacial", variable=self.spatial, justify=LEFT, command=self.onSelectCheckbox, selectcolor="black").place(x=30, y=510)
   
    def setTooltips(self):
        ToolTip(self.seedEntry, msg = "Seed", delay = self.tooltip_delay)
        ToolTip(self.savePreset_button, msg = "Save preset", delay=self.tooltip_delay)
        ToolTip(self.playButton, msg = "Apply changes and play", delay=self.tooltip_delay)
        ToolTip(self.presetCombobox, msg= "Saved presets", delay=self.tooltip_delay)
        ToolTip(self.themes_combo, msg="Themes", delay=self.tooltip_delay)
        ToolTip(self.all_random_button, msg="Randomize seed", delay=self.tooltip_delay)        

    def playButtonACtivation(self):
        print("PlayBUttons")

    def setButtons(self):
      
        original_image = Image.open("App/Images/playButton.png")

        # Reduce el tamaño de la imagen
        resized_image = original_image.resize((100, 100), Image.LANCZOS) 
        self.playButtonImage = ImageTk.PhotoImage(resized_image)

        # Calcula las coordenadas para centrar el botón
        x = (1152) / 2 - 85
        y = (648) / 2 - 230

        # Crea y coloca el botón en las coordenadas calculadas
        self.playButton = ttk.Button(self.canvas, image=self.playButtonImage, command=self.playReaper)
        self.playButton.place(x=x, y=y)

        #  -----------  Botón de todo aleatorio ---------------
        original_image = Image.open("App/Images/dado6.png")

        # Reduce el tamaño de la imagen
        resized_image = original_image.resize((80, 80), Image.LANCZOS) 
        self.generateAllRandom_buttonImage = ImageTk.PhotoImage(resized_image)

        # Calcula las coordenadas para centrar el botón
        x = 1152 * 0.85
        y = 648 * 0.7

        # Crea y coloca el botón en las coordenadas calculadas
        self.all_random_button = Button(self.canvas, image=self.generateAllRandom_buttonImage, command=self.rerollSeed)
        self.all_random_button.place(x=x, y=y)

        self.seedString = StringVar()
        self.seedEntry = Entry(self.canvas, textvariable=self.seedString, justify="center")
        self.seedEntry.place(x=x, y=y-20, width=80)
        self.seedEntry.bind("<KeyRelease>", self.onUpdateSeed)

        #  -----------  Botón de guardar presets ---------------
        original_image = Image.open("App/Images/saveIcon.png")
        resized_image = original_image.resize((30, 30), Image.LANCZOS) 
        self.savePreset_image = ImageTk.PhotoImage(resized_image)

        x = 1152 * 0.85
        y = 648 * 0.04

        self.savePreset_button = Button(self.canvas, image=self.savePreset_image, command=self.savePresetAction)
        self.savePreset_button.place(x=x, y=y)


    def displayEnumSelectors(self):
        self.current_tematic = StringVar()
        self.themes_combo = ttk.Combobox(self.canvas, values=[option.value for option in TematicEnum],
                                  textvariable=self.current_tematic, state="readonly")

        self.themes_combo.bind("<<ComboboxSelected>>", self.selectTematic)

        x = (1152) / 2 - 130
        y = (648) / 2 - 270
        self.themes_combo.place(x=x, y=y)

        
        self.current_reverb = StringVar()
        self.comboReverb = ttk.Combobox(self.canvas, values=[option.value for option in ReverbEnum],
                                  textvariable=self.current_reverb, state="readonly")

        self.comboReverb.bind("<<ComboboxSelected>>", self.selectTematic)
        x = (1152) / 2 - 130
        y = (648) / 2 - 310
        self.comboReverb.place(x=x, y=y)


    def displayPresetSelector(self):
        
        self.presetName = StringVar()
        self.presetCombobox = ttk.Combobox(self.canvas, values=None,
                                  textvariable=self.presetName, state="readonly")
        self.presetCombobox.place(x=0, y=0)
        self.refreshPresets()
        self.presetCombobox.bind("<<ComboboxSelected>>", self.recoverPresetAction)

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
        themeName = self.idToEnumValue(self.modeState.tematica)
        self.background_image_array = self.backgroundSys.configure_background(theme=themeName, 
                                                                dream= self.modeState.dream,
                                                                lofi=self.modeState.lofi,
                                                                vintage=self.modeState.vintage,
                                                                spacial=self.modeState.espacial,
                                                                underwater=self.modeState.agua,
                                                                retro=self.modeState.retro
                                                                )
              
    

    def resize_image(self, event = None):
        self.backgroundSys.resize_image(self.tab) 
        

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
        self.setBackground()
        self.resize_image()

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