from tkinter import ttk
from tkinter import *
from App.AppEnums.generationModesEnum import GenerationMode
from App.AppEnums.tematicEnum import TematicEnum
from App.AppEnums.semitonesEnum import Semitones

class AdvancedConfigTab: 
    def __init__(self, tab):
        self.tab = tab

    def setUp(self):
        ttk.Label(self.tab, text="Generador de Melodías:         ").grid(row=0, column=0)
        self.generationMode = StringVar()
        self.comboGeneration = ttk.Combobox(self.tab, values=[option.value for option in GenerationMode],
                                        textvariable=self.generationMode, state="readonly")
        self.comboGeneration.grid(row=0, column=1)

        ttk.Label(self.tab, text="Variar tonalidad (semitonos):  ").grid(row=1, column=0)
        self.variarSemitonos = StringVar()
        self.comboSemitonos = ttk.Combobox(self.tab, values=[option.value for option in Semitones],
                                        textvariable=self.variarSemitonos, state="readonly")
        self.comboSemitonos.grid(row=1, column=1)


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


    def update(self):
        return
    
    def onEntryTab(self):
        return