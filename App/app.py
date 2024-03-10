import sys
sys.path.append('./Cadenas_Markov/')
sys.path.append('./Harmonizer/')
sys.path.append('./Drums/')
sys.path.append('./Basslines/')

from tkinter import *
from tkinter import ttk
import random # TO DELETE
import mainDemo as demo
from Cadenas_Markov import markovGenerator
from Harmonizer import harmonyGenerator

from Basslines import basslineGenerator
from Drums import enums
from Drums import drumGenerator
from Basslines import basslineGenerator
from PIL import Image, ImageTk

class App:

    melody = None
    canvas = None
    root = None
    mkv_generator = None

    # Widgets
    SpinBoxVar = None

    def __init__(self):
        #Creación de la aplicación raíz
        self.root = Tk()
        self.root.geometry("800x600")
        self.canvas = Canvas(self.root, width = 800, height = 600)
        self.canvas.pack(expand=True, fill="both")

        self.mkv_generator = markovGenerator.Markov_Generator(use_silences=False)
        demo.load_markov_chain(self.mkv_generator)
        #Setting de texto y botones
        self.setBackground()
        self.setStyle()
        self.setButtons()

        
    def run(self):
        self.root.mainloop()


    def generateMelodies(self):
        print("Generando " + str(self.SpinBoxVar.get()) + " compases")
        # melody = demo.generate_melodies(self.mkv_generator, self.SpinBoxVar.get(), 1)[0]
        self.melody = demo.generate_magenta(self.SpinBoxVar.get(), 1)[0]

    def armonice(self):
        if(self.melody == None):
            return
        
        print("Armonizando...")
        bassline = basslineGenerator.BasslineGenerator.generate()
        harmonyGenerator.HarmonyGenerator.generate(bassline, self.melody)

    def tamborice(self):
        print("Tamborizando...")

        drumGenerator.DrumGenerator.generateAllStyles()

    def setStyle(self):
        style = ttk.Style()
        style.configure("TButton", padding=6, relief="flat", background="#ccc")

        l1 = ttk.Label(self.canvas, text="Generador Musical", font=30, padding=[30, 30, 30, 30]).grid(column = 0, row = 0)
        #l1.anchor(N)

    def prueba(self):
        print("Saliendo")
        self.root.destroy()

    def setButtons(self):
        ttk.Button(self.canvas, text = "Generar melodías", command = self.generateMelodies).grid(column=0, row = 1)
        self.SpinBoxVar = IntVar()
        self.SpinBoxVar.set(4)
        ttk.Spinbox(self.canvas, from_=2, to=40, textvariable=self.SpinBoxVar).grid(column=1, row=1)
        ttk.Button(self.canvas, text = "Armonizar", command = self.armonice).grid(column=0, row = 2)
        ttk.Button(self.canvas, text = "Tamborizar", command = self.tamborice).grid(column=0, row = 3)

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

        







