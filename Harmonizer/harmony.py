import scale as Scale
import interval as Interval

allChords = {
    "": Scale.Scale("1 3 5"),  # Mayor
    "-": Scale.Scale("1 b3 5"),  # Menor
    "-b5": Scale.Scale("1 b3 b5"),  # Disminuida
    "+": Scale.Scale("1 3 #5"),  # Aumentada
    "maj7": Scale.Scale("1 3 5 7"),  # Mayor séptima
    "7": Scale.Scale("1 3 5 b7"),  # Dominante 
    "-7": Scale.Scale("1 b3 5 b7"),  # Menor séptima
    "-maj7": Scale.Scale("1 b3 5 7"),  # Menor mayor séptima  
    "-7b5": Scale.Scale("1 b3 b5 b7"),  # Menor séptima disminuida (Semidisminuida)
    "º7": Scale.Scale("1 b3 b5 bb7"),  # Séptima disminuida (Disminuida)
    "+maj7": Scale.Scale("1 3 #5 7"),  # Aumentada mayor séptima
    "+7": Scale.Scale("1 3 #5 b7"),  # Aumentada dominante
}

majorProgressions = [
    {"Progression": [("1", ""), ("5", ""), ("6", "-"), ("4", ""), ("1", "")],
     "Transitions": []},
    {"Progression": [("1", ""), ("5", ""), ("6", "-"), ("3", "-"), ("4", ""), ("1", "")],
     "Transitions": []},
    {"Progression": [("1", ""), ("6", "-"), ("4", ""), ("5", ""), ("1", "")],
     "Transitions": []},
    {"Progression": [("1", ""), ("4", ""), ("6", "-"), ("5", ""), ("1", "")],
     "Transitions": []},
    {"Progression": [("1", ""), ("5", ""), ("4", ""), ("5", ""), ("1", "")],
     "Transitions": []},
    {"Progression": [("4", ""), ("2", "-"), ("1", ""), ("5", ""), ("1", ""), ("4", "")],
     "Transitions": []},
    {"Progression": [("1", ""), ("3", "-"), ("6", "-"), ("4", ""), ("1", "")],
     "Transitions": []},
    {"Progression": [("4", ""), ("1", ""), ("5", ""), ("4", "")],
     "Transitions": []},
    {"Progression": [("4", ""), ("1", ""), ("2", "-"), ("4", "")],
     "Transitions": []},
    {"Progression": [("1", ""), ("5", ""), ("1", ""), ("5", ""), ("1", "")],
     "Transitions": []},
    {"Progression": [("1", ""), ("4", ""), ("5", ""), ("1", "")],
     "Transitions": []},
    {"Progression": [("1", ""), ("4", ""), ("5", ""), ("4", ""), ("1", "")],
     "Transitions": []},
    {"Progression": [("1", ""), ("5", ""), ("6", "-"), ("5", ""), ("1", "")],
     "Transitions": []},
]

minorProgressions = [
    {"Progression": [("1", "-"), ("b7", ""), ("b6", ""), ("b7", ""), ("1", "-")],
     "Transitions": []},
    {"Progression": [("1", "-"), ("5", "-"), ("1", "-"), ("5", "-"), ("1", "-")],
     "Transitions": []},
    {"Progression": [("1", "-"), ("b6", ""), ("1", "-"), ("b6", ""), ("1", "-")],
     "Transitions": []},
    {"Progression": [("1", "-"), ("b6", ""), ("5", "-"), ("1", "-")],
     "Transitions": []},   
    {"Progression": [("1", "-"), ("b6", ""), ("b3", ""), ("b7", ""), ("1", "-")],
     "Transitions": []},
    {"Progression": [("1", "-"), ("4", "-"), ("b7", ""), ("b3", ""), ("b6", ""), ("2", "-b5"), ("5", "-"), ("1", "-")],
     "Transitions": []}
]

allChordProgressions = [
    {"Progression": [("1", ""), ("5", ""), ("1", ""), ("5", ""), ("1", "")],
     "Transitions": []},
    {"Progression": [("1", ""), ("4", ""), ("5", ""), ("1", "")],
     "Transitions": []},
    {"Progression": [("1", ""), ("4", ""), ("5", ""), ("4", ""), ("1", "")],
     "Transitions": []},
    {"Progression": [("1", ""), ("5", ""), ("6", "-"), ("5", ""), ("1", "")],
     "Transitions": []},
    {"Progression": [("1", ""), ("5", ""), ("6", "-"), ("4", ""), ("1", "")],
     "Transitions": []},
    {"Progression": [("1", ""), ("6", "-"), ("4", ""), ("5", ""), ("1", "")],
     "Transitions": []},

    {"Progression": [("1", "-"), ("5", "-"), ("1", "-"), ("5", "-"), ("1", "-")],
     "Transitions": []},
    {"Progression": [("1", "-"), ("b6", ""), ("1", "-"), ("b6", ""), ("1", "-")],
     "Transitions": []},
    {"Progression": [("1", "-"), ("b6", ""), ("5", "-"), ("1", "-")],
     "Transitions": []},
    {"Progression": [("1", "-"), ("b7", ""), ("b6", ""), ("b7", ""), ("1", "-")],
     "Transitions": []},
    {"Progression": [("1", "-"), ("b6", ""), ("b3", ""), ("b7", ""), ("1", "-")],
     "Transitions": []},
    {"Progression": [("1", "-"), ("4", "-"), ("b7", ""), ("b3", ""), ("b6", ""), ("2", "-b5"), ("5", "-"), ("1", "-")],
     "Transitions": []}
]

class Harmony:

    def __init__(self):
        self.chords = {}

    def create_harmony_from_chord_progression_list(self, chordProgressions = allChordProgressions):

        for degree in Interval.intervals:    
            self.chords[degree] = []

        for chordProggresion in chordProgressions:
            for degree, chordName in chordProggresion["Progression"]:
                if chordName not in self.chords[degree]:
                    self.chords[degree].append(chordName)
            for degree, chordName in chordProggresion["Transitions"]:
                if chordName not in self.chords[degree]:
                    self.chords[degree].append(chordName)

        self.chords = {clave: valor for clave, valor in self.chords.items() if valor}


    def create_harmony_from_scale(self, scale, possibleChords = allChords):
                    
        scale.create_degrees() 

        for idx in range(len(scale.scale)):

            chordList = self.chords[scale.scale[idx].get_name()] = []

            for chordName, chord in possibleChords.items():
                if scale.containsScale(chord, idx):
                    chordList.append(chordName)

    def relativize_chords(self):

        self.relativizedChords = {}

        for degree, chordList in self.chords.items():

            offset = Interval.Interval(degree).semitones
            relativizedChordList = self.relativizedChords[degree] = []

            for chord in chordList:

                intervals = []

                for interval in allChords[chord].scale:
                    intervals.append((interval.semitones + offset) % 12)
                
                relativizedChordList.append(Scale.Scale(intervals, False))

    def print_chords(self):
        for k, v in self.chords.items():
            print(f"{k}: {v}")

    def print_relativized_chords(self):
        for k, v in self.relativizedChords.items():
            print(k, end=":\n")
            for chords in v:
                chords.print_scale()


