from tkinter import ttk
from tkinter import *
from App.AppEnums.generationModesEnum import GenerationMode
from App.AppEnums.tematicEnum import TematicEnum
from App.AppEnums.semitonesEnum import Semitones
from App.AppEnums.melodicComplexityEnum import MelodicComplexity

class AdvancedConfigTab: 
    def __init__(self, tab):
        self.tab = tab

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
        self.temperature_var = IntVar()
        self.slider_temperature = ttk.Scale(self.tab, from_=0, to=4, style="TScale", command=self.saveTemperature, variable=self.temperature_var)
        self.slider_temperature.grid(row=2, column=1)

        # ---- Semitones ----
        self.vary_semitones_label = ttk.Label(self.tab, text="Variar semitonos:  0", justify="left", anchor="w")
        self.vary_semitones_label.grid(row=3, column=0)

        self.semitones_var = IntVar()
        slider = ttk.Scale(self.tab, from_=-6, to=6, orient="horizontal", command=self.saveSemitones, value= 0, variable=self.semitones_var)
        slider.grid(row=3, column=1)

    def setCombobox(self):
        ttk.Label(self.tab, text="Generador de Melodías:  ").grid(row=0, column=0)
        self.generationMode = StringVar()
        self.comboGeneration = ttk.Combobox(self.tab, values=[option.value for option in GenerationMode],
                                        textvariable=self.generationMode, state="readonly")
        self.comboGeneration.grid(row=0, column=1)

        ttk.Label(self.tab, text="Complejidad melódica:    ").grid(row=1, column=0)
        self.complejidad = StringVar()
        self.comboComplejidad = ttk.Combobox(self.tab, values=[option.value for option in MelodicComplexity],
                                        textvariable=self.complejidad, state="readonly")
        self.comboComplejidad.grid(row=1, column=1)

        # ttk.Label(self.tab, text="Variar tonalidad:              ").grid(row=2, column=0)
        # self.variarSemitonos = StringVar()
        # self.comboSemitonos = ttk.Combobox(self.tab, values=[option.value for option in Semitones],
        #                                 textvariable=self.variarSemitonos, state="readonly")
        # self.comboSemitonos.grid(row=2, column=1)



        ttk.Label(self.tab, text="                                     ", justify=RIGHT).grid(row=0, column=2)

        self.mezclarTematicas = BooleanVar()
        ttk.Checkbutton(self.tab, text="Mezclar temáticas              ", variable=self.mezclarTematicas).grid(row=0, column=3)
        self.tematicasAleatorias = BooleanVar()
        ttk.Checkbutton(self.tab, text="Temáticas aleatorias           ", variable=self.tematicasAleatorias).grid(row=1, column=3)
        
        ttk.Label(self.tab, text="Temática melodía 1:                  ").grid(row=2, column=3)
        self.tematicaPista1 = StringVar()
        self.comboGeneration = ttk.Combobox(self.tab, values=[option.value for option in TematicEnum],
                                        textvariable=self.tematicaPista1, state="readonly")
        self.comboGeneration.grid(row=2, column=4)

        ttk.Label(self.tab, text="Temática melodía 2:                 ").grid(row=3, column=3)
        self.tematicaPista2 = StringVar()
        self.comboGeneration = ttk.Combobox(self.tab, values=[option.value for option in TematicEnum],
                                        textvariable=self.tematicaPista2, state="readonly")
        self.comboGeneration.grid(row=3, column=4)

        ttk.Label(self.tab, text="Temática acompañamiento 1:   ").grid(row=4, column=3)
        self.tematicaPista3 = StringVar()
        self.comboGeneration = ttk.Combobox(self.tab, values=[option.value for option in TematicEnum],
                                        textvariable=self.tematicaPista3, state="readonly")
        self.comboGeneration.grid(row=4, column=4)

        ttk.Label(self.tab, text="Temática acompañamiento 2:  ").grid(row=5, column=3)
        self.tematicaPista4 = StringVar()
        self.comboGeneration = ttk.Combobox(self.tab, values=[option.value for option in TematicEnum],
                                        textvariable=self.tematicaPista4, state="readonly")
        self.comboGeneration.grid(row=5, column=4)

        ttk.Label(self.tab, text="Temática pads:                         ").grid(row=6, column=3)
        self.tematicaPista5 = StringVar()
        self.comboGeneration = ttk.Combobox(self.tab, values=[option.value for option in TematicEnum],
                                        textvariable=self.tematicaPista5, state="readonly")
        self.comboGeneration.grid(row=6, column=4)

        ttk.Label(self.tab, text="Temática bajo:                         ").grid(row=7, column=3)
        self.tematicaPista6 = StringVar()
        self.comboGeneration = ttk.Combobox(self.tab, values=[option.value for option in TematicEnum],
                                        textvariable=self.tematicaPista6, state="readonly")
        self.comboGeneration.grid(row=7, column=4)

        ttk.Label(self.tab, text="Temática batería:                     ").grid(row=8, column=3)
        self.tematicaPista7 = StringVar()
        self.comboGeneration = ttk.Combobox(self.tab, values=[option.value for option in TematicEnum],
                                        textvariable=self.tematicaPista7, state="readonly")
        self.comboGeneration.grid(row=8, column=4)

    def saveSemitones(self, event):
        semitones = self.semitones_var.get()
        self.vary_semitones_label.config(text = f"Variar semitonos: {semitones}")

    def saveTemperature(self, event):
        temperature = self.temperature_var.get()
        self.temperature_label.config(text=f"Temperatura: {temperature}")

    def setTooltips():
        return

    def update(self):
        return
    
    def onEntryTab(self):
        return