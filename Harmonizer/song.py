import scale
import note

possibleScales = {
    "Major": scale.Scale("1 2 3 4 5 6 7"), 
    "minor": scale.Scale("1 2 b3 4 5 b6 b7") 
}

class Song:

    def __init__(self, song, tonic):

        p_tonic = -(tonic.pitch - 12) 

        intervals = [0]

        for note in song:

            interval = (note["pitch"] + p_tonic) % 12

            if interval not in intervals:
                intervals.append(interval)
            
        intervals.sort()

        self.scale = scale.Scale(intervals)

    def choose_scale(self):

        print("Escala inicial:")
        self.scale.print_scale()

        if (self.scale.len() > 7):
            raise Exception("Escala ambigua: más de 7 notas distintas")
        
        if possibleScales["Major"].contains(self.scale):
            self.scale = possibleScales["Major"]
        elif possibleScales["minor"].contains(self.scale):
            self.scale = possibleScales["minor"]
        else:
            raise Exception("Escala ambigua: no hay escalas coincidentes")
        
        print("Escala final:")
        self.scale.print_scale()

