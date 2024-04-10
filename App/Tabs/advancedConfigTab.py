from tkinter import ttk
from tkinter import *

class AdvancedConfigTab: 
    def __init__(self, tab):
        self.tab = tab

    def setUp(self):

        ttk.Label(self.tab, text="Esta ventana aún no tiene efecto en las melodías").grid(row=0, column=0)

        self.mezclarTematicas = BooleanVar()
        ttk.Checkbutton(self.tab, text="Mezclar temáticas", variable=self.mezclarTematicas).grid(row=1, column=0)