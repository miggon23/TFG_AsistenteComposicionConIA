import pandas as pd
import numpy as np
import scale as Scale
import interval as Interval
import harmony as Harmony
from song import possibleScales

def softmax(row):
    return row / row.sum()

def translate_chord(chord):

        if chord is None:
            return "start_end"
        else:
            return chord[0] + "_" + chord[1]

class Chain:

    def __init__(self, filePath):
        self.filePath = filePath

    def load_model(self, reverse = False):
        self.df = pd.read_excel(self.filePath, index_col=0)

        if reverse:
            self.df = self.df.transpose()

        self.df = self.df.apply(softmax, axis=1)

        # self.df.to_excel('datasets/debug.xlsx')

    def predict(self, prevChords, chord):

        prevChord = translate_chord(prevChords[0])
        chord = translate_chord(chord)

        if prevChord in self.df.index and chord in self.df.index:
            return self.df.at[prevChord, chord]
        else:
            return 0
              
class ModalPerspective():

    modes = [None, "Dorian", "Phrygian", "Lydian", "Mixolydian", None, "Locrian"]

    possibleChords = {
        "": Scale.Scale("1 3 5"),  # Mayor
        "-": Scale.Scale("1 b3 5"),  # Menor
        "maj7": Scale.Scale("1 3 5 7"),  # Mayor séptima
        "-7": Scale.Scale("1 b3 5 b7"),  # Menor séptima
    }

    def __init__(self, mode, chordWeights = [1, 0.5, 0.05], suggestedChords = possibleChords):
        self.mode = mode
        self.chordWeights = chordWeights  

        if self.mode == "Locrian":
            self.possibleChords["-b5"] = Scale.Scale("1 b3 b5")    
            self.possibleChords["-7b5"] = Scale.Scale("1 b3 b5 b7")

        self.possibleChords = {clave: self.possibleChords[clave] for clave in self.possibleChords if clave in suggestedChords} 

        majorScale = Scale.Scale("1 2 3 4 5 6 7")
        majorScale.create_degrees()
        self.modalScale = majorScale.degrees[self.modes.index(self.mode) - 1]

        if self.modalScale.scale[2] == Interval.Interval("3"):
            scale = majorScale
        else:
            scale = Scale.Scale("1 2 b3 4 5 b6 b7")
            scale.create_degrees()

        self.colorNotes = []

        for scaleInterval, modalInterval in zip(scale.scale, self.modalScale.scale): 
            if scaleInterval != modalInterval:
                self.colorNotes.append(modalInterval.__copy__())

    def load_model(self, reverse = False):

        harmony = Harmony.Harmony(self.modalScale, self.possibleChords)     
        harmony.relativize_chords()

        dic = {"start" : ["end"]}
        dic.update(harmony.chords.copy())

        self.weights = {}
        
        for (degree, chords), chordNames in zip(harmony.relativizedChords.items(), harmony.chords.values()):
            for chord, chordName in zip(chords, chordNames):

                weight = self.chordWeights[2]
                if degree == "1":
                    weight = self.chordWeights[0]
                else:
                    idx = 0
                    while idx < len(self.colorNotes) and not chord.containsInterval(self.colorNotes[idx]):
                        idx += 1
                    if idx < len(self.colorNotes):
                        weight = self.chordWeights[1]

                # self.weights[degree + "_" + chordName] = weight
                self.weights[(degree, chordName)] = weight

        values = softmax(np.array(list(self.weights.values())))
        self.weights = dict(zip(self.weights.keys(), values))

        # df = pd.DataFrame(list(self.weights.items()), columns=['Clave', 'Valor'])
        # df.to_excel('datasets/debug.xlsx')

    def predict(self, prevChords, chord):
        if chord in self.weights:
            return self.weights[chord]
    


        
