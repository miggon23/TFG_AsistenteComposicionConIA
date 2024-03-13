from tkinter import ttk
from tkinter import *

import mainDemo as demo
from Cadenas_Markov import markovGenerator
from Harmonizer import harmonyGenerator
from Basslines import basslineGenerator
from Drums import enums
from Drums import drumGenerator
from Basslines import basslineGenerator

class GenerationTab:
    
    def __init__(self, tab):
        self.tab = tab

        # Ver si se genera por Magenta o por Markov
        #self.mkv_generator = markovGenerator.Markov_Generator(use_silences=False)
        #demo.load_markov_chain(self.mkv_generator)


    def setUp(self):
        self.setStyle()
        self.setButtons()

    def setStyle(self):
        style = ttk.Style()
        style.configure("TButton", padding=6, relief="flat", background="#ccc")

        ttk.Label(self.tab, text="Generador Musical", font=30, padding=[30, 30, 30, 30]).grid(column = 0, row = 0)

    def setButtons(self):
        ttk.Button(self.tab, text = "Generar melodías", command = self.generateMelodies).grid(column=0, row = 1)
        self.SpinBoxVar = IntVar()
        self.SpinBoxVar.set(8)
        ttk.Spinbox(self.tab, from_=2, to=40, textvariable=self.SpinBoxVar).grid(column=1, row=1)
        ttk.Button(self.tab, text = "Armonizar", command = self.armonice).grid(column=0, row = 2)
        ttk.Button(self.tab, text = "Tamborizar", command = self.tamborice).grid(column=0, row = 3)

    # Button callbacks
        
    
    def generateMelodies(self):
        print("Generando " + str(self.SpinBoxVar.get()) + " compases")
        #self.melody = demo.generate_melodies(self.mkv_generator, self.SpinBoxVar.get(), 1)[0]
        self.melody = demo.generate_magenta(self.SpinBoxVar.get(), 1)[0]

    def armonice(self):
        if(self.melody == None):
            return
        
        print("Armonizando...")
        bassline = basslineGenerator.BasslineGenerator.generate()
        harmonyGenerator.HarmonyGenerator.generate(bassline, self.melody)
        harmonyGenerator.HarmonyGenerator.generateModal(self.melody, "./midi/", "./midi/")
        print("Armonizacion completa")


    def tamborice(self):
        print("Tamborizando...")

        drumGenerator.DrumGenerator.generateAllStyles()
        print("Tamborizacion completa")
