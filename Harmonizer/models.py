import pandas as pd
import numpy as np
import scale as Scale
import interval as Interval
import harmony as Harmony

def softmax(row):
    return row / row.sum()

def translate_chord(chord):

        if chord is None:
            return "start_end"
        else:
            return chord[0] + "_" + chord[1]

class Chain:

    def __init__(self, filePath):

        self.df = pd.read_excel(filePath, index_col=0)

        # if reverse:
        #     self.df = self.df.transpose()

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

    # modalChordProgressions = {
    #     "Dorian" : [
    #         {"Progression": [("1", "-"), ("4", "")],
    #         "Transitions": [("1", "-")]},
    #         {"Progression": [("1", "-"), ("5", "-")],
    #         "Transitions": [("1", "-")]},
    #         {"Progression": [("1", "-"), ("7", ""), ("4", "")],
    #         "Transitions": [("1", "-")]},
    #         {"Progression": [("1", "-"), ("3", ""), ("4", "")],
    #         "Transitions": [("1", "-")]}
    #     ],
    #     "Phrygian" : [
    #         {"Progression": [("1", "-"), ("4", "-")],
    #         "Transitions": [("1", "-")]},
    #         {"Progression": [("1", "-"), ("7", "-")],
    #         "Transitions": [("1", "-")]},
    #         {"Progression": [("1", "-"), ("b3", ""), ("4", "-")],
    #         "Transitions": [("1", "-")]}
    #     ],
    #     "Lydian" : [
    #         {"Progression": [("1", ""), ("5", "")],
    #         "Transitions": [("1", "")]},
    #         {"Progression": [("1", ""), ("3", ""), ("5", "")],
    #         "Transitions": [("1", "")]},
    #         {"Progression": [("1", ""), ("3", ""), ("6", "-")],
    #         "Transitions": [("1", "")]},
    #         {"Progression": [("1", ""), ("5", ""), ("2", "")],
    #         "Transitions": [("1", "")]}
    #     ],
    #     "Mixolydian" : [
    #         {"Progression": [("1", ""), ("4", "")],
    #         "Transitions": [("1", "")]},
    #         {"Progression": [("1", ""), ("5", "-")],
    #         "Transitions": [("1", "")]},
    #         {"Progression": [("1", ""), ("7", ""), ("4", "")],
    #         "Transitions": [("1", "")]},
    #         {"Progression": [("1", ""), ("6", "-"), ("4", "")],
    #         "Transitions": [("1", "")]}
    #     ],
    #     "Locrian" : [
    #         {"Progression": [("1", ""), ("4", "")],
    #         "Transitions": [("1", "")]},
    #         {"Progression": [("1", ""), ("5", "-")],
    #         "Transitions": [("1", "")]},
    #         {"Progression": [("1", ""), ("7", ""), ("4", "")],
    #         "Transitions": [("1", "")]},
    #         {"Progression": [("1", ""), ("6", "-"), ("4", "")],
    #         "Transitions": [("1", "")]}
    #     ]
    # }


    modes = [None, "Dorian", "Phrygian", "Lydian", "Mixolydian", None, "Locrian"]

    possibleChords = {
        "": Scale.Scale("1 3 5"),  # Mayor
        "-": Scale.Scale("1 b3 5"),  # Menor
        "maj7": Scale.Scale("1 3 5 7"),  # Mayor séptima
        "-7": Scale.Scale("1 b3 5 b7"),  # Menor séptima
    }

    def __init__(self, mode, suggestedChords = possibleChords):
        self.mode = mode 

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

        harmony = Harmony.Harmony()   
        harmony.create_harmony_from_scale(self.modalScale, self.possibleChords)  
        harmony.relativize_chords()

        primaryChords = []
        secondaryChords = []
        
        for (degree, chords), chordNames in zip(harmony.relativizedChords.items(), harmony.chords.values()):
            for chord, chordName in zip(chords, chordNames):

                if degree == "1":
                    primaryChords.append((degree, chordName))
                else:
                    idx = 0
                    while idx < len(self.colorNotes) and not chord.containsInterval(self.colorNotes[idx]):
                        idx += 1
                    if idx < len(self.colorNotes):
                        secondaryChords.append((degree, chordName))

        self.chordProgressions = []

        for primaryChord in primaryChords:
            for secondaryChord in secondaryChords:

                progression = {}
                progression["Progression"] = [primaryChord, secondaryChord]
                progression["Transitions"] = primaryChords + [chord for chord in secondaryChords if chord != secondaryChord]
                self.chordProgressions.append(progression)

                progression = {}
                progression["Progression"] = [secondaryChord, primaryChord]
                progression["Transitions"] = [chord for chord in primaryChords if chord != primaryChord] + secondaryChords
                self.chordProgressions.append(progression)
        
        return


    def predict(self, prevChords, chord):
        return 1
    


        
