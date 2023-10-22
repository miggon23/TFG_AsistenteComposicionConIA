import scale

allChords = {
    "": scale.Scale("1 3 5"),
    "-": scale.Scale("1 b3 5"),
    "-b5": scale.Scale("1 b3 b5"),
    "maj7": scale.Scale("1 3 5 7"),
    "7": scale.Scale("1 3 5 b7"),
    "-7": scale.Scale("1 b3 5 b7"),
    "-maj7": scale.Scale("1 b3 5 7"),  
    "-7b5": scale.Scale("1 b3 b5 b7"),
    "º7": scale.Scale("1 b3 b5 bb7"),
    "+maj7": scale.Scale("1 3 #5 7")   
}

class Harmony:
    # Constructor de la clase
    def __init__(self, scale):

        self.chords = {}
        self.scale = scale
                    
        self.scale.create_degrees() 

        for n in range(len(scale.scale)):

            chordList = self.chords[scale.scale[n].get_interval()] = []

            for k, v in allChords.items():
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

                for interval in allChords[chord].scale:
                    intervals.append((interval.semitones + offset) % 12)
                
                chordList.append(scale.Scale(intervals, False))

            idx += 1

    def print_chords(self):
        for k, v in self.chords.items():
            print(f"{k}: {v}")

    def print_relativized_chords(self):
        for k, v in self.relativizedChords.items():
            print(k, end=":\n")
            for chords in v:
                chords.print_scale()


