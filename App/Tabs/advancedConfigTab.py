from tkinter import ttk
from tkinter import *
import json

from App.AppEnums.generationModesEnum import GenerationMode
from App.AppEnums.tematicEnum import TematicEnum
from App.AppEnums.tematicEnum import TematicDrumEnum
from App.AppEnums.semitonesEnum import Semitones
from App.AppEnums.melodicComplexityEnum import MelodicComplexity
from Utils import globalConsts
import random

class AdvancedConfigTab: 
    generationComboboxes = []
    generationLabels = []

    def __init__(self, tab, *, modeSelectorTab):
        self.tab = tab
        self.modeSelectorTab = modeSelectorTab

    def setUp(self):
       self.setCombobox()
       self.setSliders()

    def setSliders(self):
        # ---- Temperature ----
        self.temperature_label = ttk.Label(self.tab, text="Temperatura:  0", justify="left", anchor="w")
        self.temperature_label.grid(row=2, column=0)
        estilo = ttk.Style()

        estilo.configure("TScale", background="lightgray")
        estilo.map("TScale",
            background=[("active", "red")],
            foreground=[("active", "red")]
            )
        self.temperature_var = DoubleVar()
        self.slider_temperature = ttk.Scale(self.tab, from_=1.0, to=4.0, style="TScale", command=self.update_temperature, variable=self.temperature_var)
        self.slider_temperature.grid(row=2, column=1)

        # ---- Semitones ----
        self.vary_semitones_label = ttk.Label(self.tab, text="Variar semitonos:  0", justify="left", anchor="w")
        self.vary_semitones_label.grid(row=3, column=0)

        self.semitones_var = IntVar()
        slider = ttk.Scale(self.tab, from_=-6, to=6, orient="horizontal", command=self.update_semitones, value= 0, variable=self.semitones_var)
        slider.grid(row=3, column=1)

    # MARK: COMBOBOX

    def setCombobox(self):
        ttk.Label(self.tab, text="Generador de Melodías:  ").grid(row=0, column=0)
        self.generation_mode_var = StringVar()
        self.comboGeneration = ttk.Combobox(self.tab, values=[option.value for option in GenerationMode],
                                        textvariable=self.generation_mode_var, state="readonly")
        self.comboGeneration.grid(row=0, column=1)
        self.comboGeneration.bind("<<ComboboxSelected>>", self.save_generator)

        self.complexity_label = ttk.Label(self.tab, text="Complejidad melódica:    ")
        self.complexity_label.grid(row=1, column=0)
        self.complexity_var = StringVar()
        self.comboComplexity = ttk.Combobox(self.tab, values=[option.value for option in MelodicComplexity],
                                        textvariable=self.complexity_var, state="readonly")
        self.comboComplexity.grid(row=1, column=1)

        # ttk.Label(self.tab, text="Variar tonalidad:              ").grid(row=2, column=0)
        # self.variarSemitonos = StringVar()
        # self.comboSemitonos = ttk.Combobox(self.tab, values=[option.value for option in Semitones],
        #                                 textvariable=self.variarSemitonos, state="readonly")
        # self.comboSemitonos.grid(row=2, column=1)



        ttk.Label(self.tab, text="                                     ", justify=RIGHT).grid(row=0, column=2)

        self.mezclar_tematicas_var = BooleanVar()
        ttk.Checkbutton(self.tab, text="Mezclar temáticas              ", variable=self.mezclar_tematicas_var, command=self.toggleMixedThemes).grid(row=0, column=3)
        self.tematicas_aleatorias_var = BooleanVar()
        self.tematica_aleatoria_checkbutton = ttk.Checkbutton(self.tab, text="Temáticas aleatorias           ", variable=self.tematicas_aleatorias_var, command=self.mix_themes)
        self.tematica_aleatoria_checkbutton.grid(row=1, column=3)
        
        self.tLabel1 = ttk.Label(self.tab, text="Temática melodía 1:                  ")
        self.tLabel1.grid(row=2, column=3)
        self.tematicaPista1 = StringVar()
        self.comboGeneration1 = ttk.Combobox(self.tab, values=[option.value for option in TematicEnum],
                                        textvariable=self.tematicaPista1, state="readonly")
        self.comboGeneration1.grid(row=2, column=4)
        self.comboGeneration1.bind("<<ComboboxSelected>>", self.save_mixed_themes)

        self.generationComboboxes.append(self.comboGeneration1)
        self.generationLabels.append(self.tLabel1)

        self.tLabel2 = ttk.Label(self.tab, text="Temática melodía 2:                 ")
        self.tLabel2.grid(row=3, column=3)
        self.tematicaPista2 = StringVar()
        self.comboGeneration2 = ttk.Combobox(self.tab, values=[option.value for option in TematicEnum],
                                        textvariable=self.tematicaPista2, state="readonly")
        self.comboGeneration2.grid(row=3, column=4)
        self.comboGeneration2.bind("<<ComboboxSelected>>", self.save_mixed_themes)
        self.generationComboboxes.append(self.comboGeneration2)
        self.generationLabels.append(self.tLabel2)

        self.tLabel3 = ttk.Label(self.tab, text="Temática acompañamiento 1:   ")
        self.tLabel3.grid(row=4, column=3)
        self.tematicaPista3 = StringVar()
        self.comboGeneration3 = ttk.Combobox(self.tab, values=[option.value for option in TematicEnum],
                                        textvariable=self.tematicaPista3, state="readonly")
        self.comboGeneration3.grid(row=4, column=4)
        self.comboGeneration3.bind("<<ComboboxSelected>>", self.save_mixed_themes)
        self.generationComboboxes.append(self.comboGeneration3)
        self.generationLabels.append(self.tLabel3)

        self.tLabel4 = ttk.Label(self.tab, text="Temática acompañamiento 2:  ")
        self.tLabel4.grid(row=5, column=3)
        self.tematicaPista4 = StringVar()
        self.comboGeneration4 = ttk.Combobox(self.tab, values=[option.value for option in TematicEnum],
                                        textvariable=self.tematicaPista4, state="readonly")
        self.comboGeneration4.grid(row=5, column=4)
        self.comboGeneration4.bind("<<ComboboxSelected>>", self.save_mixed_themes)
        self.generationComboboxes.append(self.comboGeneration4)
        self.generationLabels.append(self.tLabel4)

        self.tLabel5 = ttk.Label(self.tab, text="Temática pads:                         ")
        self.tLabel5.grid(row=6, column=3)
        self.tematicaPista5 = StringVar()
        self.comboGeneration5 = ttk.Combobox(self.tab, values=[option.value for option in TematicEnum],
                                        textvariable=self.tematicaPista5, state="readonly")
        self.comboGeneration5.bind("<<ComboboxSelected>>", self.save_mixed_themes)
        self.comboGeneration5.grid(row=6, column=4)
        self.generationComboboxes.append(self.comboGeneration5)
        self.generationLabels.append(self.tLabel5)

        self.tLabel6 = ttk.Label(self.tab, text="Temática bajo:                         ")
        self.tLabel6.grid(row=7, column=3)
        self.tematicaPista6 = StringVar()
        self.comboGeneration6 = ttk.Combobox(self.tab, values=[option.value for option in TematicEnum],
                                        textvariable=self.tematicaPista6, state="readonly")
        self.comboGeneration6.grid(row=7, column=4)
        self.comboGeneration6.bind("<<ComboboxSelected>>", self.save_mixed_themes)
        self.generationComboboxes.append(self.comboGeneration6)
        self.generationLabels.append(self.tLabel6)

        self.tLabel7 = ttk.Label(self.tab, text="Temática batería:                     ")
        self.tLabel7.grid(row=8, column=3)
        self.tematicaPista7 = StringVar()
        self.comboGeneration7 = ttk.Combobox(self.tab, values=[option.value for option in TematicDrumEnum],
                                        textvariable=self.tematicaPista7, state="readonly")
        self.comboGeneration7.grid(row=8, column=4)
        self.comboGeneration7.bind("<<ComboboxSelected>>", self.save_mixed_themes)
        self.generationComboboxes.append(self.comboGeneration7)
        self.generationLabels.append(self.tLabel7)

    def update_semitones(self, event = None):
        semitones = self.semitones_var.get()
        self.vary_semitones_label.config(text = f"Variar semitonos: {semitones}")

    def update_temperature(self, event = None):
        temperature = self.temperature_var.get()
        temperature = round(temperature, 1)
        self.temperature_var.set(temperature)

        self.temperature_label.config(text=f"Temperatura: {temperature}")

    

    def setTooltips():
        return

    def update(self):
        return
    
    def onEntryTab(self):
        self.recover_state()
        self.toggleMixedThemes()
    
    def onExitTab(self):
        self.save_mixed_themes()
        self.save_configuration_()

    # MARK: CALLBACKS

    def toggleMixedThemes(self):
        mixThemes = self.mezclar_tematicas_var.get()

        if(mixThemes):
            self.show_combo()
        else:
            self.hide_combo()

        modeState = self.modeSelectorTab.get_state()
        modeState.mezclar_tematicas = mixThemes

    def show_combo(self):
        self.tematica_aleatoria_checkbutton.grid()

        for combo in self.generationComboboxes:
            combo.grid()

        for label in self.generationLabels:
            label.grid()
  

    def hide_combo(self):
        self.tematica_aleatoria_checkbutton.grid_remove()

        for combo in self.generationComboboxes:
            combo.grid_remove()

        for label in self.generationLabels:
            label.grid_remove()

    def mix_themes(self):

        if self.tematicas_aleatorias_var.get() == True:
            for combo in self.generationComboboxes:
                theme = random.choice(list(TematicEnum))
                combo.set(theme.value)
        else:
            current_theme = self.modeSelectorTab.get_state().tematica
            theme_string = self.idToEnumValue(current_theme, TematicEnum)
            for combo in self.generationComboboxes:
                combo.set(theme_string)


    def save_mixed_themes(self, event = None):
        themes_array = []

        for combo in self.generationComboboxes:
            theme = combo.get()
            if(theme != ""):
                themes_array.append(self.NameEnumToId(theme, TematicDrumEnum))

        modeState = self.modeSelectorTab.get_state()
        modeState.tematica_pistas = themes_array

    def idToEnumValue(self, id, enum):
        return list(enum)[id].value
    
    def NameEnumToId(self, themeName, enum):
        return [member.value for member in enum].index(themeName)

    def save_generator(self, event = None):
        generator = self.generation_mode_var.get()
        jsonPath = globalConsts.Paths.appConfigPath

        # Leemos el JSON
        with open(jsonPath, "r") as archivo:
            datos = json.load(archivo)

        # Modifica la variable deseada en el diccionario
        datos["melodyGenerator"] = generator

        # Abre el archivo JSON en modo escritura
        with open(jsonPath, "w") as archivo:
            json.dump(datos, archivo, indent=4)

    def recover_state(self):
        jsonPath = globalConsts.Paths.appConfigPath

        with open(jsonPath, "r") as archivo:
            datos = json.load(archivo)

        generator = datos["melodyGenerator"]
        temperature = datos["temperature"]

        self.generation_mode_var.set(generator)
        self.temperature_var.set(temperature)
        self.update_temperature()

        modeState = self.modeSelectorTab.get_state()
        semitones = modeState.semitonos
        self.semitones_var.set(semitones)
        self.update_semitones()
        self.mezclar_tematicas_var.set(modeState.mezclar_tematicas)
  
        complexity = self.idToEnumValue(modeState.complejidad, MelodicComplexity)
        self.complexity_var.set(complexity)

        mix_themes_array = modeState.tematica_pistas

        i = 0
        for combo in self.generationComboboxes:
            combo.set(self.idToEnumValue(mix_themes_array[i], TematicEnum))
            i+=1

    # MARK: PERSISTENCE

    def save_configuration_(self):
        temperature = self.temperature_var.get()

        jsonPath = globalConsts.Paths.appConfigPath

        with open(jsonPath, "r") as archivo:
            datos = json.load(archivo)

        datos["temperature"] = temperature

        with open(jsonPath, "w") as archivo:
            json.dump(datos, archivo, indent=4)

        semitones = self.semitones_var.get()
        complexity = self.complexity_var.get()

        modeState = self.modeSelectorTab.get_state()
        modeState.semitonos = semitones
        modeState.complejidad = self.NameEnumToId(complexity, MelodicComplexity)

        self.modeSelectorTab.save_state()


