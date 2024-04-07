from tkinter import ttk
from tkinter import *

class ConfigurationTab:

    def __init__(self, tab):
        self.tab = tab

    def setUp(self):
        ttk.Label(self.tab, text="Reaper absolute path").grid(row=0, column=0)
        self.reaperPathEntry = ttk.Entry(self.tab, text="C:")
        self.reaperPathEntry.grid(row=0, column=1)

        self.applyButton = ttk.Button(self.tab, padding=[20, 30, 20, 0], text="Aplicar", command=self.applySettings).grid(row=10, column=0)

    def applySettings(self):
        reaperPathString = self.reaperPathEntry.get()
        print(reaperPathString)
        