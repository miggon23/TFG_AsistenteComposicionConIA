from tkinter import ttk
from tkinter import *
from Utils import globalConsts

import json

class ConfigurationTab:

    def __init__(self, tab):
        self.tab = tab

    def setUp(self):
        ttk.Label(self.tab, text="Reaper absolute path").grid(row=0, column=0)
        
        self.pathString = StringVar()
        self.reaperPathEntry = ttk.Entry(self.tab, text="C:", textvariable=self.pathString)
        self.reaperPathEntry.grid(row=0, column=1)

        self.applyButton = ttk.Button(self.tab, text="Aplicar", command=self.applySettings).grid(row=10, column=0, pady=40)
        
    def onEntryTab(self):
        jsonPath = globalConsts.Paths.appConfigPath

        with open(jsonPath, "r") as archivo: # <- with se encarga de cerrar el archivo cuando acaba
            # Cargamos el contenido del archivo en un diccionario
            datos = json.load(archivo)

        reaper_path = datos["reaperPath"]
        self.pathString.set(reaper_path)

    def applySettings(self):
        reaperPathString = self.reaperPathEntry.get()
        jsonPath = globalConsts.Paths.appConfigPath
        
        # Leemos el JSON
        with open(jsonPath, "r") as archivo:
            datos = json.load(archivo)

        # Modifica la variable deseada en el diccionario
        datos["reaperPath"] = reaperPathString

        # Abre el archivo JSON en modo escritura
        with open(jsonPath, "w") as archivo:
            json.dump(datos, archivo, indent=4)

        print("'" + reaperPathString + "'" + " guardado como ruta a Reaper")


        