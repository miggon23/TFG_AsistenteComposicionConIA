from tkinter import ttk
from tkinter import *
from App.AppEnums.generationModesEnum import GenerationMode

class AdvancedConfigTab: 
    def __init__(self, tab):
        self.tab = tab

    def setUp(self):
        ttk.Label(self.tab, text="Esta ventana aún no tiene efecto en las melodías", justify=RIGHT).grid(row=0, column=0)

        self.mezclarTematicas = BooleanVar()
        ttk.Checkbutton(self.tab, text="Mezclar temáticas", variable=self.mezclarTematicas).grid(row=1, column=0)

        ttk.Label(self.tab, text="Generador de Melodías").grid(row=2, column=0)
        self.generationMode = StringVar()
        self.comboGeneration = ttk.Combobox(self.tab, values=[option.value for option in GenerationMode],
                                        textvariable=self.generationMode, state="readonly")
        self.comboGeneration.grid(row=2, column=1)