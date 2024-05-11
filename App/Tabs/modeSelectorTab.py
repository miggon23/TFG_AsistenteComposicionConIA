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

    tab_width = 1152
    tab_height = 648

    def __init__(self, tab):
        self.tab = tab

        self.canvas = Canvas(self.tab, width = 1152, height = 648)
        self.canvas.pack(fill="both", expand=True)

    # MARK: SET UP

    def setUp(self, root):
        self.root = root
        self.backgroundSys = BackgroundSystem(self.canvas, self.tab)
        self.backgroundSys.init()

        self.setCheckboxes()
        self.displayComboboxes()
        self.displayPresetSelector()
        self.setButtons()

        self.recoverStateFromFile()
        self.setBackground()
        self.setTooltips()
        # Enlazar la función resize_image al evento de cambio de tamaño de la ventana
        # self.root.bind("<Configure>", self.resize_image)

        self.reaperStream = llamamosReaper.ReaperStream()
        self.presetManager = PresetManager()
        self.rerollAllSeeds()

    def update(self):
        self.backgroundSys.update()
        
    def onEntryTab(self):
        self.resize_image()
        self.check_mixed_themes()

    def onExitTab(self):
        return

    # MARK: CHECKBOXES
    
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
   

    def get_state(self):
        return self.modeState

    # MARK: TOOLTIPS

    def setTooltips(self):
        ToolTip(self.instrument_seedEntry, msg = "Semilla de instrumentos", delay = self.tooltip_delay)
        ToolTip(self.instrument_seedEntry, msg = "Semilla de arreglos", delay = self.tooltip_delay)
        ToolTip(self.savePreset_button, msg = "Guardar preset", delay=self.tooltip_delay)
        ToolTip(self.playButton, msg = "Guardar cambios y reproducir", delay=self.tooltip_delay)
        ToolTip(self.presetCombobox, msg= "presets guardados", delay=self.tooltip_delay)
        ToolTip(self.themes_combo, msg="Temáticas", delay=self.tooltip_delay)
        ToolTip(self.all_random_button, msg="Aleatorizar todas las semillas", delay=self.tooltip_delay)  
        ToolTip(self.instrument_random_button, msg="Aleatorizar semilla de instrumentos", delay=self.tooltip_delay)      
        ToolTip(self.arrangement_random_button, msg="Aleatorizar semilla de arreglos", delay=self.tooltip_delay)    
        ToolTip(self.combo_reverb, msg = "Entorno", delay=self.tooltip_delay)  

    def check_mixed_themes(self):
        x = (self.tab_width) / 2 - 130
        y = (self.tab_height) / 2 - 270

        if self.modeState.mezclar_tematicas:
            self.themes_combo.place_forget()
            self.mixed_themes_label.place(x = x + 25, y = y + 10)
        else:
            self.themes_combo.place(x = x, y = y)
            self.mixed_themes_label.place_forget()


    # MARK: BUTTONS

    def setButtons(self):
      
        tab_width = 1152
        tab_height = 648

        original_image = Image.open("App/Images/playButton.png")

        # Reduce el tamaño de la imagen
        resized_image = original_image.resize((100, 100), Image.LANCZOS) 
        self.playButtonImage = ImageTk.PhotoImage(resized_image)

        # Calcula las coordenadas para centrar el botón
        x = (tab_width) / 2 - 85
        y = (tab_height) * 0.16

        # Crea y coloca el botón en las coordenadas calculadas
        self.playButton = ttk.Button(self.canvas, image=self.playButtonImage, command=self.playReaper)
        self.playButton.place(x=x, y=y)

        #  -----------  Botón de todo aleatorio ---------------
        original_image = Image.open("App/Images/dado6.png")

        # Reduce el tamaño de la imagen
        resized_image = original_image.resize((100, 100), Image.LANCZOS) 
        self.generateAllRandom_buttonImage = ImageTk.PhotoImage(resized_image)

        # Calcula las coordenadas para centrar el botón
        x = tab_width * 0.84
        y = tab_height * 0.52

        # Botón de re-roll de todas las semillas
        self.all_random_button = Button(self.canvas, image=self.generateAllRandom_buttonImage, command=self.rerollAllSeeds)
        self.all_random_button.place(x=x, y=y)

        y = tab_height * 0.75

        # Semilla de instrumentos
        x = tab_width * 0.9
        instrument_image = Image.open("App/Images/dado5.png")

        resized_image = instrument_image.resize((60, 60), Image.LANCZOS) 
        self.generate_instrument_buttonImage = ImageTk.PhotoImage(resized_image)

        self.instrument_random_button = Button(self.canvas, image=self.generate_instrument_buttonImage, command=self.rerollInstrumentSeed)
        self.instrument_random_button.place(x=x, y=y)

        self.seed_instrument_string = StringVar()

        self.instrument_seedEntry = Entry(self.canvas, textvariable=self.seed_instrument_string, justify="center")
        self.instrument_seedEntry.place(x=x, y=y-20, width=65)
        self.instrument_seedEntry.bind("<KeyRelease>", self.onUpdateSeed)

        # Semilla de arreglos
        x = tab_width * 0.82
        arrangement_image = Image.open("App/Images/dado3.png")

        resized_image = arrangement_image.resize((60, 60), Image.LANCZOS) 
        self.generate_arrangement_buttonImage = ImageTk.PhotoImage(resized_image)

        self.arrangement_random_button = Button(self.canvas, image=self.generate_arrangement_buttonImage, command=self.rerollArrangementSeed)
        self.arrangement_random_button.place(x=x, y=y)


        self.seed_arrangement_string = StringVar()

        self.arrangement_seedEntry = Entry(self.canvas, textvariable=self.seed_arrangement_string, justify="center")
        self.arrangement_seedEntry.place(x=x, y=y-20, width=65)
        self.arrangement_seedEntry.bind("<KeyRelease>", self.onUpdateSeed)

        #  -----------  Botón de guardar presets ---------------
        original_image = Image.open("App/Images/saveIcon.png")
        resized_image = original_image.resize((30, 30), Image.LANCZOS) 
        self.savePreset_image = ImageTk.PhotoImage(resized_image)

        x = 220
        y = 8

        self.savePreset_button = Button(self.canvas, image=self.savePreset_image, command=self.savePresetAction)
        self.savePreset_button.place(x=x, y=y)

    # MARK: COMBOBOXES

    def displayComboboxes(self):
        self.current_tematic = StringVar()
        self.themes_combo = ttk.Combobox(self.canvas, values=[option.value for option in TematicEnum],
                                  textvariable=self.current_tematic, state="readonly")

        self.themes_combo.bind("<<ComboboxSelected>>", self.selectTematic)

        x = (1152) / 2 - 130
        y = (648) / 2 - 270
        self.themes_combo.place(x=x, y=y)
        self.mixed_themes_label = Label(self.canvas, text="\"Mezclar temáticas activo\"", foreground="green")

        
        self.current_reverb = StringVar()
        self.combo_reverb = ttk.Combobox(self.canvas, values=[option.value for option in ReverbEnum],
                                  textvariable=self.current_reverb, state="readonly")

        self.combo_reverb.bind("<<ComboboxSelected>>", self.selectReverb)
        x = (1152) / 2 - 130
        y = (648) / 2 - 310
        self.combo_reverb.place(x=x, y=y)

    def displayPresetSelector(self):
        
        self.presetName = StringVar()
        self.presetCombobox = ttk.Combobox(self.canvas, values=None,
                                  textvariable=self.presetName, state="readonly")
        self.presetCombobox.place(x=10, y=10)
        self.refreshPresets()
        self.presetCombobox.bind("<<ComboboxSelected>>", self.recoverPresetAction)

        original_image = Image.open("App/Images/saveIcon.png")
        resized_image = original_image.resize((30, 30), Image.LANCZOS) 
        self.redreshButton_Image = ImageTk.PhotoImage(resized_image)

    # MARK: COMBOBOX CALLBACKS

    def selectTematic(self, event):
        # Guardamos la temática seleccionada en el evento
        tematic = self.current_tematic.get()
        print("Seleccionado: ", tematic)

        self.modeState.tematica = self.NameEnumToId(tematic, TematicEnum)
        self.setBackground()
        self.resize_image()

    def selectReverb(self, event):
        reverb = self.current_reverb.get()

        self.modeState.reverb = self.NameEnumToId(reverb, ReverbEnum)
        return

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
        themeName = self.idToEnumValue(self.modeState.tematica, TematicEnum)
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
        self.onUpdateSeed()

        self.save_state()
        self.reaperStream.SetUp()

    def idToEnumValue(self, id, enum):
        return list(enum)[id].value
    
    def NameEnumToId(self, themeName, enum):
        return [member.value for member in enum].index(themeName)
    
    # MARK: PERSISTENCE

    def recoverState(self, modeState):
        self.modeState = modeState

        self.lofi.set(self.modeState.lofi)
        self.vintage.set(self.modeState.vintage)
        self.spatial.set(self.modeState.espacial)
        self.underWater.set(self.modeState.agua)
        self.retro.set(self.modeState.retro)
        self.dream.set(self.modeState.dream)
        self.seed_instrument_string.set(self.modeState.seed_instrument)
        self.seed_arrangement_string.set(self.modeState.seed_arrangement)
        
        tematica_value = self.idToEnumValue(self.modeState.tematica, TematicEnum)
        self.current_tematic.set(tematica_value)

        reverb_value = self.idToEnumValue(self.modeState.reverb, ReverbEnum)
        self.current_reverb.set(reverb_value)

    def recoverStateFromFile(self):
        jsonPath = globalConsts.Paths.mediaSettings
        modeState = ModeState.fromJSON(jsonPath)
        self.recoverState(modeState)

    def save_state(self):
        jsonPath = globalConsts.Paths.mediaSettings
        dataJSONString = self.modeState.toJSON()

        # Abre el archivo JSON en modo escritura
        with open(jsonPath, "w") as archivo:
            json.dump(dataJSONString, archivo, indent=4)

    # MARK: PRESETS

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
        
    # MARK: SEEDS

    def rerollAllSeeds(self):
        self.rerollInstrumentSeed()
        self.rerollArrangementSeed()

    def rerollInstrumentSeed(self):
        self.seed_instrument_string.set(stringUtils.generate_random_string(5, None))

    def rerollArrangementSeed(self):
        self.seed_arrangement_string.set(stringUtils.generate_random_string(5, None))
        self.modeState.seed_arrangement = self.seed_arrangement_string.get()

    def onUpdateSeed(self, event = None):
        self.modeState.seed_instrument = self.seed_instrument_string.get()
        self.modeState.seed_arrangement = self.seed_arrangement_string.get()