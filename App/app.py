import sys
sys.path.append('./Cadenas_Markov/')
sys.path.append('./Harmonizer/')
sys.path.append('./Drums/')
sys.path.append('./Basslines/')
sys.path.append('./App/Tabs/')
sys.path.append('./Utils/')

from tkinter import *
from tkinter import ttk
import sv_ttk

from Cadenas_Markov import markovGenerator

from PIL import Image, ImageTk

#Tabs
import generationTab
import modeSelectorTab
import configurationTab
import advancedConfigTab

class App:

    melody = None
    canvas = None
    root = None
    mkv_generator = None

    #Notebook, maneja las pestañas
    notebook = None

    #Pestañas de la App
    generationTab = None
    modeSelectorTab = None

    #Frames
    frame1 = None
    frame2 = None

    # Widgets
    SpinBoxVar = None

    def __init__(self):
        #Creación de la aplicación raíz
        self.root = Tk()
        self.root.title("Compositor Automatico")
        self.root.geometry("1152x648")
        self.root.resizable(False, False)
        sv_ttk.set_theme("dark")

        # Creamos el notebok que manejará las pestañas
        self.notebook = ttk.Notebook(self.root)

        #Crear pestañas
        self.frame1 = ttk.Frame(self.root, padding = 20)
        self.frame2 = ttk.Frame(self.root, padding = 20)
        self.frame3 = ttk.Frame(self.root, padding = 20)
        self.frame4 = ttk.Frame(self.root, padding = 20)

        # Agregar las pestañas al notebook
        self.notebook.add(self.frame1, text="Generación")
        self.notebook.add(self.frame2, text="Musicalización")
        self.notebook.add(self.frame3, text="Avanzado")
        self.notebook.add(self.frame4, text="Configuración")

        #Los hacemos pack
        self.notebook.pack(fill="both", expand=True)
        self.notebook.bind("<<NotebookTabChanged>>", self.onTabChanged)
        
        # Creamos las clases que representan cada pestaña de la App
        self.generationTab = generationTab.GenerationTab(self.frame1)
        self.modeSelectorTab = modeSelectorTab.ModeSelectorTab(self.frame2)
        self.advancedConfig = advancedConfigTab.AdvancedConfigTab(self.frame3)
        self.configTab = configurationTab.ConfigurationTab(self.frame4)

        self.modeSelectorTab.setUp(self.root)
        self.generationTab.setUp()
        self.advancedConfig.setUp()
        self.configTab.setUp()

     
    def run(self):
        self.root.mainloop()

    def onTabChanged(self, event):
        #curentTab = self.notebook.select()
        selectedTab = self.notebook.select()
        id = self.notebook.index(selectedTab)  

        if id == 0:
            self.generationTab.onEntryTab()
        elif id == 1:
            self.modeSelectorTab.onEntryTab()
        elif id == 2:
            self.advancedConfig.onEntryTab()
        elif id == 3:
            self.configTab.onEntryTab()

        







