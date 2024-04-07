import sys
sys.path.append('./Cadenas_Markov/')
sys.path.append('./Harmonizer/')
sys.path.append('./Drums/')
sys.path.append('./Basslines/')
sys.path.append('./App/Tabs/')

from tkinter import *
from tkinter import ttk

from Cadenas_Markov import markovGenerator

from PIL import Image, ImageTk

#Tabs
import generationTab
import modeSelectorTab
import configurationTab


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
        self.root.geometry("800x600")
        
        # Creamos el notebok que manejará las pestañas
        self.notebook = ttk.Notebook(self.root)

        #Crear pestañas
        self.frame1 = ttk.Frame(self.root, padding = 20)
        self.frame2 = ttk.Frame(self.root, padding = 20)
        self.frame3 = ttk.Frame(self.root, padding = 20)

        # Agregar las pestañas al notebook
        self.notebook.add(self.frame1, text="Generación")
        self.notebook.add(self.frame2, text="Musicalización")
        self.notebook.add(self.frame3, text="Config")

        #Los hacemos pack
        self.notebook.pack(fill="both", expand=True)
        
        # Creamos las clases que representan cada pestaña de la App
        self.generationTab = generationTab.GenerationTab(self.frame1)
        self.modeSelectorTab = modeSelectorTab.ModeSelectorTab(self.frame2)
        self.configTab = configurationTab.ConfigurationTab(self.frame3)

        self.modeSelectorTab.setUp(self.root)
        self.generationTab.setUp()
        self.configTab.setUp()

     
    def run(self):
        self.root.mainloop()


        







