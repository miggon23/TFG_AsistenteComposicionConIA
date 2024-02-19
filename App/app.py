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

class App:

    melody = None
    frame = None
    root = None
    mkv_generator = None

    # Widgets
    SpinBoxVar = None

    def __init__(self):
        #Creación de la aplicación raíz
        self.root = Tk()
        self.root.geometry("400x300")
        self.frame = ttk.Frame(self.root, padding = 20)
        self.frame.grid()

        self.mkv_generator = markovGenerator.Markov_Generator(use_silences=False)
        demo.load_markov_chain(self.mkv_generator)
        #Setting de texto y botones
        self.setStyle()
        self.setButtons()
        

        #Llama al bucle de la aplicación
        
    def run(self):
        self.root.mainloop()


    def generateMelodies(self):
        print("Generando " + str(self.SpinBoxVar.get()) + " compases")
        melody = demo.generate_melodies(self.mkv_generator, self.SpinBoxVar.get(), 1)[0]

    def armonice(self):
        if(self.melody == None):
            return
        
        print("Armonizando...")
        bassline = basslineGenerator.BasslineGenerator.generate()
        harmonyGenerator.HarmonyGenerator.generate(bassline, self.melody)

    def tamborice(self):
        print("Tamborizando...")

        style = enums.Style.BASIC
        drumGenerator.DrumGenerator.generate(style)

    def setStyle(self):
        style = ttk.Style()
        style.configure("TButton", padding=6, relief="flat", background="#ccc")

        l1 = ttk.Label(self.frame, text="Generador Musical", font=30,)
        l1.grid(column = 0, row = 0)
        l1.anchor(N)

    def prueba(self):
        print("Saliendo")
        self.root.destroy()

    def saveCompass(self):
        print(self.spinButton.get())

    def setButtons(self):
        ttk.Button(self.frame, text = "Generar melodías", command = self.generateMelodies).grid(column=0, row = 1)
        self.SpinBoxVar = IntVar()
        self.SpinBoxVar.set(4)
        ttk.Spinbox(self.frame, from_=2, to=40, textvariable=self.SpinBoxVar).grid(column=1, row=1)
        ttk.Button(self.frame, text = "Armonizar", command = self.armonice).grid(column=0, row = 2)
        ttk.Button(self.frame, text = "Tamborizar", command = self.tamborice).grid(column=0, row = 3)
        ttk.Button(self.frame, text = "Salir", command = self.prueba).grid(column=0, row = 10)
        





