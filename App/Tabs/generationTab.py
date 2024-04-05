from tkinter import ttk
from tkinter import *

from timidity import Parser, play_notes
import numpy as np

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
        self.SpinBoxVar.set(4)
        ttk.Spinbox(self.tab, from_=2, to=40, textvariable=self.SpinBoxVar).grid(column=1, row=1)
        ttk.Button(self.tab, text = "Reproducir", command = self.playPreview).grid(column=0, row = 2)
        ttk.Button(self.tab, text = "Armonizar", command = self.armonice).grid(column=0, row = 3)
        ttk.Button(self.tab, text = "Tamborizar", command = self.tamborice).grid(column=0, row = 4)

    # Button callbacks
        
    
    def generateMelodies(self):
        print("Generando " + str(self.SpinBoxVar.get()) + " compases")
        #self.melody = demo.generate_melodies(self.mkv_generator, self.SpinBoxVar.get(), 1)[0]
        self.bars = self.SpinBoxVar.get()
        self.melody = demo.generate_magenta(self.bars * 2, 1)[0]
        self.melody = harmonyGenerator.HarmonyGenerator.treatMelody(input=self.melody, output="./midi/trasposed_melody.mid")


    def armonice(self):
        # if(self.melody == None):
        #     return

        print("Armonizando...")

        letters = ['A', 'B', 'C', 'D']

        songs, tonics, models = harmonyGenerator.HarmonyGenerator.generateModalMelodies(self.melody)
        for song in songs:
            semiSongs = harmonyGenerator.HarmonyGenerator.spreadSong(song, ticks=self.bars*4)
            for idx, semiSong in enumerate(semiSongs):
                harmonyGenerator.HarmonyGenerator.spreadSong(semiSong,
                    output1=song[:-4] + letters[idx * 2] + ".mid",
                    output2=song[:-4] + letters[idx * 2 + 1] + ".mid",
                    ticks=self.bars*2)
            harmonyGenerator.HarmonyGenerator.combineSongs(semiSongs[0], semiSongs[1],
                                             output=song.replace("_output_", "_input_"))
        harmonyGenerator.HarmonyGenerator.generateModalHarmony(tonics, models)

        semiSongs = harmonyGenerator.HarmonyGenerator.spreadSong(self.melody, ticks=self.bars*4)
        for idx, semiSong in enumerate(semiSongs):
            harmonyGenerator.HarmonyGenerator.spreadSong(semiSong, 
                output1="./midi/output_song" + letters[idx * 2] + ".mid",
                output2="./midi/output_song" + letters[idx * 2 + 1] + ".mid",
                ticks=self.bars*2)
        harmonyGenerator.HarmonyGenerator.generate(harmonyGenerator.HarmonyGenerator.combineSongs(semiSongs[0], semiSongs[1]))
    
        print("Armonizacion completa")


    def tamborice(self):
        print("Tamborizando...")

        drumGenerator.DrumGenerator.generateAllStyles()
        print("Tamborizacion completa")

    def playPreview(self):
        ps = Parser("./midi/output_song.mid")

        play_notes(*ps.parse(), np.sin)