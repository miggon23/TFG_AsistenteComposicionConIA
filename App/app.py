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
        
        #Background frame2
        self.canvas = Canvas(self.frame2, width = 800, height = 600)
        self.canvas.pack(expand=True, fill="both")

        # Agregar las pestañas al notebook
        self.notebook.add(self.frame1, text="Generación")
        self.notebook.add(self.frame2, text="Musicalización")

        self.generationTab = generationTab.GenerationTab(self.frame1)

        #Los hacemos pack
        self.notebook.pack(fill="both", expand=True)
        

        #Setting de texto y botones
        self.setBackground()
        self.generationTab.setUp()


        
    def run(self):
        self.root.mainloop()


    def setBackground(self):
        # Cargar la imagen original
        self.background_image_pil = Image.open("App/Images/DarkRiders.png")
        
        # Crear una instancia de ImageTk para la imagen original
        self.background = ImageTk.PhotoImage(self.background_image_pil)
        
        # Crear la imagen en el canvas
        self.background_id = self.canvas.create_image(0, 0, anchor="nw", image=self.background)
        
        # Enlazar la función resize_image al evento de cambio de tamaño de la ventana
        self.root.bind("<Configure>", self.resize_image)

    def resize_image(self, event):
        # Redimensionar la imagen original cuando cambia el tamaño de la ventana
        new_width = event.width
        new_height = event.height
        resized_image_pil = self.background_image_pil.resize((new_width, new_height), Image.LANCZOS)
        self.background = ImageTk.PhotoImage(resized_image_pil)
        self.canvas.itemconfig(self.background_id, image=self.background)

        







