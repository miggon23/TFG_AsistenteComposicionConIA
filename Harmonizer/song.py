import scale
import note
import harmony
import interval
import math

stdWeights = {
    "chordWeight": [1, 0.25, 0.5, 0.25],
    "tickWeights": [1.4, 1.1, 1.2, 1.1],
    "notPlayingAtTickPen": 0.75
}


possibleScales = {
    "Major": scale.Scale("1 2 3 4 5 6 7"), 
    "minor": scale.Scale("1 2 b3 4 5 b6 b7") 
}

class Song:

    def __init__(self, melody, tonic):

        self.tonic = tonic
        self.melody = melody

        p_tonic = -(tonic.pitch - 12) 

        intervals = [0]

        for note in melody:

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
            self.scale = possibleScales["Major"].copy_scale()
        elif possibleScales["minor"].contains(self.scale):
            self.scale = possibleScales["minor"].copy_scale()
        else:
            raise Exception("Escala ambigua: no hay escalas coincidentes")
        
        print("Escala final:")
        self.scale.print_scale()

    def armonize(self, ticksPerSlice = 4.0, weights = stdWeights):

        possibleChords = {
            "": scale.Scale("1 3 5"),
            "-": scale.Scale("1 b3 5"),
            "-b5": scale.Scale("1 b3 b5")
        }

        self.harmony = harmony.Harmony(self.scale, possibleChords)
        self.harmony.relativize_chords()
        self.__relativize_spread_song()

        self.chordAnalysis = []
        lastTick = list(self.relativazedSpreadSong.keys())[-1]
        nSlices = math.ceil(lastTick / ticksPerSlice)
        for _ in range(nSlices):
            self.chordAnalysis.append({})

        tickWeightTime = ticksPerSlice / len(weights["tickWeights"])
        tick = 0
        while (tick < nSlices * ticksPerSlice):
            if tick not in self.relativazedSpreadSong:
                self.relativazedSpreadSong[tick] = []
            tick += tickWeightTime  
        self.relativazedSpreadSong = dict(sorted(self.relativazedSpreadSong.items()))               

        notesPlaying = []

        for tick, notes in self.relativazedSpreadSong.items():

            slice = int(tick / ticksPerSlice)

            tickWeightNow = 1
            if tick % tickWeightTime == 0:
                tickWeightNow = weights["tickWeights"][int(tick - slice * ticksPerSlice)]

            newNotesPlaying = []

            for note in notes:
                if note[1]:
                    newNotesPlaying.append(note[0])
                    self.__calculate_chord_weights(slice, note[0], weights["chordWeight"], tickWeightNow)                      
                else:
                    notesPlaying.remove(note[0])    

            if tick % tickWeightTime == 0:
                for note in notesPlaying:
                    self.__calculate_chord_weights(slice, note, 
                        weights["chordWeight"], tickWeightNow, weights["notPlayingAtTickPen"])
            
            notesPlaying.extend(newNotesPlaying)

        self.print_chord_analysis()

        return self.melody + self.__translate_harmony(ticksPerSlice)

    def print_chord_analysis(self):
        idx = 0
        for chordList in self.chordAnalysis:
            print("Slice: ", idx)
            idx += 1
            for chord, w in chordList.items():
                print(chord[0], " ", self.harmony.chords[chord[0]][chord[1]], ": ", w)

    def __calculate_chord_weights(self, slice, note, 
        chordWeight, tickWeight, notPlayingAtTickPen = 1):
         
         for degree, chords in self.harmony.relativizedChords.items():
                        chordIdx = 0
                        for chord in chords:
                            intervalIdx = 0
                            for interval in chord.scale:
                                if note == interval:       
                                    key = (degree, chordIdx)  
                                    if key not in self.chordAnalysis[slice]:
                                        self.chordAnalysis[slice][key] = 0                       
                                    self.chordAnalysis[slice][key] += (chordWeight[intervalIdx] * tickWeight * notPlayingAtTickPen)
                                intervalIdx += 1
                            chordIdx += 1

    
    def __relativize_spread_song(self):

        self.relativazedSpreadSong = {}

        p_tonic = -(self.tonic.pitch - 12)

        for note in self.melody:

            i = interval.Interval((note["pitch"] + p_tonic) % 12)

            key = note['start_time']

            if key in self.relativazedSpreadSong:
                self.relativazedSpreadSong[key].append((i, True))
            else:
                self.relativazedSpreadSong[key] = [(i, True)]

            key += note['duration']

            if key in self.relativazedSpreadSong:
                self.relativazedSpreadSong[key].append((i, False))
            else:
                self.relativazedSpreadSong[key] = [(i, False)]

        return dict(sorted(self.relativazedSpreadSong.items()))
    
    def __translate_harmony(self, ticksPerSlice):

        songChordNotes = []

        idx = 0
        for slice in self.chordAnalysis:
            maxWeight = 0
            bestChord = None
            for chord, weight in slice.items():
                if weight > maxWeight:
                    maxWeight = weight
                    bestChord = chord

            if bestChord is not None:
                for interval in self.harmony.relativizedChords[bestChord[0]][0].scale:
                    songChordNotes.append({"pitch": note.get_pitch(interval, self.tonic, 4), "start_time": ticksPerSlice * idx, "duration": ticksPerSlice})
            
            idx += 1

        return songChordNotes




