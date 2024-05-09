from tkinter import ttk
from tkinter import *
from tkinter import filedialog
from Utils import globalConsts

import json

class ConfigurationTab:

    def __init__(self, tab):
        self.tab = tab

    def setUp(self):
        ttk.Label(self.tab, text="Reaper absolute path").grid(row=0, column=0)
        
        self.pathString = StringVar()
        self.reaperPathEntry = ttk.Entry(self.tab, textvariable=self.pathString, width=100)
        self.reaperPathEntry.grid(row=0, column=1)

        self.applyButton = ttk.Button(self.tab, text="Aplicar", command=self.applySettings)
        self.applyButton.grid(row=10, column=0, pady=40)

        self.find_reaper_button = ttk.Button(self.tab, text="Buscar", command=self.ask_reaper_path)
        self.find_reaper_button.grid(row=0, column=2)
        
    def onEntryTab(self):
        jsonPath = globalConsts.Paths.appConfigPath

        with open(jsonPath, "r") as archivo: # <- with se encarga de cerrar el archivo cuando acaba
            # Cargamos el contenido del archivo en un diccionario
            datos = json.load(archivo)

        reaper_path = datos["reaperPath"]
        self.pathString.set(reaper_path)


    def update(self):
        return

    def applySettings(self):
        reaperPathString = self.pathString.get()
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

    def ask_reaper_path(self):
        file_path = filedialog.askopenfilename(filetypes=[("reaper executable", "reaper.exe"), ("All files", "*.*")])
        if(file_path == ""):
            return
        
        self.pathString.set(file_path)
        self.applySettings()

        