from tkinter import ttk
from tkinter import *
from tkinter import filedialog

from timidity import Parser, play_notes
import numpy as np
import json

import mainDemo as demo
from App.Strategies import generationStrategy
from Cadenas_Markov import markovGenerator
from Harmonizer import harmonyGenerator
from Drums import drumGenerator
from Utils import globalConsts
import shutil


class GenerationTab:
    
    preview_player = None
    generation_strategy = None

    def __init__(self, tab):
        self.tab = tab
        self.melody = None
        # Ver si se genera por Magenta o por Markov
        self.mkv_generator = markovGenerator.Markov_Generator(use_silences=False)
        demo.load_markov_chain(self.mkv_generator)

    def setUp(self):
        self.setStyle()
        self.setButtons()

    def onEntryTab(self):  
        self.load_generation_strategy_() 
    
    
    def onExitTab(self):
        return

    def update(self):
        return

    def setStyle(self):
        style = ttk.Style()
        style.configure("TButton", padding=6, relief="flat", background="#ccc")

        ttk.Label(self.tab, text="Generador Musical", font=30, padding=[30, 30, 30, 30]).grid(column = 0, row = 0, padx=30)

    def setButtons(self):
        ttk.Button(self.tab, text="Cargar archivo MIDI", command=self.selectMIDIFile).grid(column=1, row=1, padx=0, pady=10)
        self.file_loaded_label = ttk.Label(self.tab, text="No hay archivo cargado", font=("Arial", 10, "italic"), foreground="white")
        self.file_loaded_label.grid(column=2, row=0, padx=10, pady=10)
        ttk.Button(self.tab, text = "Generar melodías", command = self.generateMelodies).grid(column=0, row = 1, padx=30, pady=10)
        ttk.Button(self.tab, text = "Reproducir", command = self.playPreview).grid(column=0, row = 2, padx=30, pady=10)
        ttk.Button(self.tab, text= "Stop", command= self.stopPreview).grid(column=1, row=2)
        ttk.Button(self.tab, text = "Armonizar", command = self.armonice).grid(column=0, row = 3, padx=30, pady=10)
        ttk.Button(self.tab, text = "Tamborizar", command = self.tamborice).grid(column=0, row = 4, padx=30, pady=10)
        ttk.Button(self.tab, text = "Guardar melodía", command = self.saveMelody).grid(column=0, row = 5, padx=30, pady=10)
        self.melody_saved_lavel = ttk.Label(self.tab, text="", font=("Arial", 10, "italic"), foreground="white")
        self.melody_saved_lavel.grid(column=2, row=5, padx=10, pady=10)

    def selectMIDIFile(self):
        file_path = filedialog.askopenfilename(filetypes=[("MIDI files", "*.mid"), ("All files", "*.*")])
        if file_path:
            self.melody = file_path
            self.melody = harmonyGenerator.HarmonyGenerator.treatMelody(input=self.melody, output="./Media/midi/trasposed_song.mid")

            self.file_loaded_label.config(text="Archivo cargado correctamente: \n" + file_path, foreground="green")

    def saveMelody(self):
        file_path = filedialog.asksaveasfilename(filetypes=[("MIDI files", "*.mid"), ("All files", "*.*")])
        if file_path and self.melody:
            if not file_path.lower().endswith(".mid"):
                file_path += ".mid"

            shutil.copyfile(self.melody, file_path)

            self.melody_saved_lavel.config(text="Melodía guardada correctamente en: \n" + file_path, foreground="white")
    
    def generateMelodies(self):
        self.file_loaded_label.config(text="No hay archivo cargado", foreground="white")
        self.melody_saved_lavel.config(text="", foreground="white")

        self.bars = 8

        print(f"Generando con {self.temperature} de temperatura")
        # MAGENTA
        self.melody = self.generation_strategy.generate_melodies(markov=self.mkv_generator, n_bars=self.bars, n_sims=1, temperature=self.temperature)[0]
        # self.melody = demo.generate_magenta(64, 1, temperature)[0]
        
        self.melody = harmonyGenerator.HarmonyGenerator.treatMelody(input=self.melody, output="./Media/midi/trasposed_song.mid")


    def armonice(self):
        print("Armonizando...")

        # A(2) + B(2) 
        # A(2) = A1(1) + A2(1)
        # B(2) = B1(1) + B2(1)
        # Armonización secuencial: (A + B)(4)

        # esto lo tengo que hacer porque no se puede hacer generate de 4
        melody = harmonyGenerator.HarmonyGenerator.spreadSong(input="./Media/midi/trasposed_song.mid",
                                                    output1="./Media/midi/output_melody.mid",
                                                    output2="./Media/midi/trah.mid",
                                                    ticks=4*4)[0]
        
        melody_list = harmonyGenerator.HarmonyGenerator.generate(input=melody,
                                                                output_melody="./Media/midi/output_melody_X_.mid",
                                                                output_harmony="./Media/midi/output_harmony_X_.mid",
                                                                output_std_harmony="./Media/midi/output_std_harmony_X_.mid")[0]

        for melody in melody_list: 
            A, B = harmonyGenerator.HarmonyGenerator.spreadSong(input=melody,
                                                        output1=melody[:-4] + "A.mid",
                                                        output2=melody[:-4] + "B.mid",
                                                        ticks=2*4)
            
            A1, A2 = harmonyGenerator.HarmonyGenerator.spreadSong(input=A,
                                                        output1=melody[:-4] + "A1.mid",
                                                        output2=melody[:-4] + "A2.mid",
                                                        ticks=1*4)
            
            B1, B2 = harmonyGenerator.HarmonyGenerator.spreadSong(input=B,
                                                        output1=melody[:-4] + "B1.mid",
                                                        output2=melody[:-4] + "B2.mid",
                                                        ticks=1*4)

        # A(4) + B(4) 
        # A(4) = A1(2) + A2(2)
        # B(4) = B1(2) + B2(2)
        # Armonización combinada: (A + B)(4)
      
        melody_list = harmonyGenerator.HarmonyGenerator.generate2(input="./Media/midi/trasposed_song.mid",
                                                                output_melody="./Media/midi/output_melody_Y_.mid",
                                                                output_harmony="./Media/midi/output_harmony_Y_.mid",
                                                                output_std_harmony="./Media/midi/output_std_harmony_Y_.mid")[0]

        for melody in melody_list: 
            A, B = harmonyGenerator.HarmonyGenerator.spreadSong(input=melody,
                                                        output1=melody[:-4] + "A.mid",
                                                        output2=melody[:-4] + "B.mid",
                                                        ticks=4*4)
            
            A1, A2 = harmonyGenerator.HarmonyGenerator.spreadSong(input=A,
                                                        output1=melody[:-4] + "A1.mid",
                                                        output2=melody[:-4] + "A2.mid",
                                                        ticks=2*4)
            
            B1, B2 = harmonyGenerator.HarmonyGenerator.spreadSong(input=B,
                                                        output1=melody[:-4] + "B1.mid",
                                                        output2=melody[:-4] + "B2.mid",
                                                        ticks=2*4)

        # A(8)
        # Armonización completa: (A)(8)

        harmonyGenerator.HarmonyGenerator.generate3(input="./Media/midi/trasposed_song.mid",
                                                    output_melody="./Media/midi/output_melody_Z_.mid",
                                                    output_harmony="./Media/midi/output_harmony_Z_.mid",
                                                    output_std_harmony="./Media/midi/output_std_harmony_Z_.mid")[0]
        
        print("Armonizacion completa")


    def tamborice(self):
        print("Tamborizando...")

        drumGenerator.DrumGenerator.generateAllStyles()
        print("Tamborizacion completa")

    def playPreview(self):
        if(self.preview_player != None and self.preview_player.is_playing()):
            self.preview_player.stop()

        ps = Parser("./Media/midi/trasposed_song.mid")
        # TODO salida de errores si falla al parsear .mid
        audio, self.preview_player = play_notes(*ps.parse(), np.sin, wait_done=False)

    def stopPreview(self):
        if(self.preview_player == None):
            return
        
        self.preview_player.stop()
        self.preview_player = None
    
    def load_generation_strategy_(self):
        jsonPath = globalConsts.Paths.appConfigPath

        with open(jsonPath, "r") as archivo:
            datos = json.load(archivo)

        generator = datos["melodyGenerator"]
        temperature = datos["temperature"]

        if generator in generationStrategy.strategy_per_mode:
            self.generation_strategy = generationStrategy.strategy_per_mode[generator]

        # Recuperamos también la temperatura para el generador
        self.temperature = temperature
        
        

