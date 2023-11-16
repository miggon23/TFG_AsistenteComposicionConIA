import Scale

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

onlyTriads = {
    "": Scale.Scale("1 3 5"),  # Mayor
    "-": Scale.Scale("1 b3 5"),  # Menor
    "-b5": Scale.Scale("1 b3 b5"),  # Disminuida
    "+": Scale.Scale("1 3 #5"),  # Aumentada
}

class Harmony:
    # Constructor de la clase
    def __init__(self, scale, possibleChords = allChords):

        self.possibleChords = possibleChords

        self.chords = {}
        self.scale = scale
                    
        self.scale.create_degrees() 

        for n in range(len(scale.scale)):

            chordList = self.chords[scale.scale[n].get_name()] = []

            for k, v in  self.possibleChords.items():
                if scale.contains(v, n):
                    chordList.append(k)

    def relativize_chords(self):

        self.relativizedChords = {}

        idx = 0
        for k, v in self.chords.items():

            offset = self.scale.scale[idx].semitones
            chordList = self.relativizedChords[k] = []

            for chord in v:

                intervals = []

                for interval in self.possibleChords[chord].scale:
                    intervals.append((interval.semitones + offset) % 12)
                
                chordList.append(Scale.Scale(intervals, False))

            idx += 1

    def print_chords(self):
        for k, v in self.chords.items():
            print(f"{k}: {v}")

    def print_relativized_chords(self):
        for k, v in self.relativizedChords.items():
            print(k, end=":\n")
            for chords in v:
                chords.print_scale()


