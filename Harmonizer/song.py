import Scale
import Note
import Harmony
import Interval
import math
import random

stdWeights = {
    "chordWeight": [1, 0.25, 0.5, 0.25],
    "tickWeights": [1.4, 1.1, 1.2, 1.1],
    "notPlayingAtTickPen": 0.75
}


possibleScales = {
    "Major": Scale.Scale("1 2 3 4 5 6 7"), 
    "minor": Scale.Scale("1 2 b3 4 5 b6 b7") 
}

'''
Reformatea la representación de la canción para que sea más fácil de operar para los diferentes algoritmos:
    song[tick] = (note_on[], note_off[])
'''
def spread_song(song):
    spreadSong = {}

    for note in song:

        key = note['start_time']

        for i in range(2):
            if key not in spreadSong:
                spreadSong[key] = ([],[])
            spreadSong[key][i].append(note['note'])

            key += note['duration']

    return dict(sorted(spreadSong.items()))

def debug_song(song, output_file):

    with open(output_file, 'w') as f:           
        for note in song:
            f.write(f"note: {note['note']}, Start Time: {note['start_time']}, Duration: {note['duration']}\n")

class Song:

    def __init__(self, melody, tonic = None):

        self.melody = melody

        if tonic == None:
            self.tonic = Note.Note(self.melody[0]['note']  % 12)
        else:
            self.tonic = tonic       

        pTonic = -(self.tonic.pitch - 12) 

        intervals = [0]

        for note in self.melody:

            interval = (note["note"] + pTonic) % 12

            if interval not in intervals:
                intervals.append(interval)
            
        intervals.sort()

        self.scale = Scale.Scale(intervals) 
        
    def choose_scale(self):
        if (self.scale.len() >= 7):
            return
        
        self.scale.create_degrees()
        degrees = self.scale.degrees
        degrees.insert(0, self.scale)

        print(f"Escala base: ", end="")
        self.scale.print_scale()
        print(f"Tónica base: {self.tonic.name}")

        fittingScales = []

        idx = 0
        for degree in degrees:

            for name, scale in possibleScales.items():

                if scale.contains(degree):
                    tonic = Note.Note((self.tonic.pitch + self.scale.scale[idx].semitones) % 12)
                    fittingScales.append((tonic, name))
                    print(f"Escala {name} coincidente con tónica en {tonic.name}")
            idx += 1

        if not fittingScales:

            print(f"No hay escala tonal coincidente cuya tónica sea alguna de las notas de la melodía")

            majorDegrees = possibleScales["Major"].copy_scale()
            majorDegrees.create_degrees()
            majorDegrees = majorDegrees.degrees

            idx = 0
            for degree in degrees:

                degree.print_scale()
                idj = 1
                for majorDegree in majorDegrees:

                    if majorDegree.contains(degree):
                        tonic = Note.Note(self.tonic.pitch + self.scale.scale[idx].semitones)
                        print(f"Modo {possibleScales['Major'].scale[idj].get_name()} coincidente con tónica en {tonic.name}")
                        tonic = Note.Note(tonic.pitch - possibleScales['Major'].scale[idj].semitones)
                        print(f"Se traduce a una escala Mayor con tónica en {tonic.name}")
                        fittingScales.append((tonic, "Major"))
                    idj += 1
                idx += 1

        if not fittingScales:
             print(f"No hay ninguna escala tonal coincidente")
             return

        finalScale = fittingScales[random.randint(0, len(fittingScales) - 1)]
        self.tonic = finalScale[0]
        self.scale = possibleScales[finalScale[1]].copy_scale()
        self.scale.absolutize_scale(self.tonic)
        print("Escala elegida:")
        self.scale.print_scale()
        self.scale.print_absolutized_scale()    
        
    '''
    Divide la canción en slices (fragmentos) equivalentes para los cuales se busca el acorde más coherente
    Genera la armonía de la canción asignando pesos a los acordes dependiendo de varios factores:
        - La posición de la nota dentro del acorde ("chordWeight": [w1ª, w3ª, w5ª, ...])
        - El momento en el que suena la nota dentro del fragmento ("tickWeights": [w0, w1, w2, ...])
        - Si la nota acaba de sonar o ya estaba sonando de antes ("notPlayingAtTickPen" = w)
    '''
    def armonize(self, ticksPerSlice = 4.0, weights = stdWeights, possibleChords = None):

        if possibleChords == None:
            self.harmony = Harmony.Harmony(self.scale)
        else:
            self.harmony = Harmony.Harmony(self.scale, possibleChords)
        self.harmony.relativize_chords()
        self.__relativize_song()
        relativizedSpreadSong = spread_song(self.relativazedSong)

        '''
        Calculo cuanto dura la canción mirando el tick en el que acaba la última nota
        Divido entonces entre el número de ticks por slice (fragmentos de canción) 
        A cada fragmento le corresponderá un único acorde, que será el que más peso tenga
        '''    
        self.chordAnalysis = []
        lastTick = list(relativizedSpreadSong.keys())[-1]
        nSlices = math.ceil(lastTick / ticksPerSlice)
        for _ in range(nSlices):
            self.chordAnalysis.append({})

        '''
        A la hora de asignar pesos, el algoritmo tiene en cuenta ticks clave dentro de cada fragmento,
        cada fragmento se subdivide equitativamente en el número de fragmentos que haya en la lista ("tickWeights": [w0, w1, w2, ...])
        Además, el peso que se asigne a un acorde se ve mermado dependiendo si la nota acaba 
        de empezar a sonar en el tick clave, o sonaba anteriormente ("notPlayingAtTickPen": w)
        Puede dar la casualidad de que en un tick clave no termine ni comience una nota,
        para ello, incluyo en el diccionario de notas ticks "fantasma" en esos ticks clave, 
        para que el algoritmo tenga en cuenta también las notas que hayan comenzado a sonar anteriormente
        '''    
        tickWeightTime = ticksPerSlice / len(weights["tickWeights"])
        tick = 0
        while (tick < nSlices * ticksPerSlice):
            if tick not in relativizedSpreadSong:
                relativizedSpreadSong[tick] = ([],[])
            tick += tickWeightTime  
        relativizedSpreadSong = dict(sorted(relativizedSpreadSong.items()))               

        notesPlaying = []

        for tick, notes in relativizedSpreadSong.items():

            #Notas que abacan de terminar, se eliminan de la lista
            for note in notes[1]:
                #Si hay un error aquí es posible que haya notas de 0 segundos de duración
                notesPlaying.remove(note) 

            slice = int(tick / ticksPerSlice)

            '''
            Comprueba si toca tick clave
            En caso afirmativo, actualizo el incremento de peso por tick clave a su correspondiente (tickWeightNow)
            Además, recorro las notas que empezaron a sonar en ticks anteriores para incrementar los pesos
            '''    
            tickWeightNow = 1
            if tick % tickWeightTime == 0:
                tickWeightNow = weights["tickWeights"][int((tick - slice * ticksPerSlice) / tickWeightTime)]
                for note in notesPlaying:
                    self.__calculate_chord_weights(note, slice, 
                        weights["chordWeight"], tickWeightNow, weights["notPlayingAtTickPen"])

            #Notas que acaban de empezar a sonar
            for note in notes[0]:
                notesPlaying.append(note)
                self.__calculate_chord_weights(note, slice, weights["chordWeight"], tickWeightNow) 

        self.__choose_best_chords()
        return self.__translate_harmony(ticksPerSlice)
    
    '''
    Dada una nota (y una serie de pesos), recorre toda la lista de acordes posibles para 
    comprobar que la nota esté en el acorde y sumarle el correspondiente peso en el correspondiente fragmento
    Dependiendo de la posición de la nota en el acorde los pesos serán distintos
    '''
    def __calculate_chord_weights(self, note, slice, 
        chordWeight, tickWeight, notPlayingAtTickPen = 1):
         
        for degree, chords in self.harmony.relativizedChords.items():
                    chordIdx = 0
                    #Recorro todos los acordes de la lista de acordes
                    for chord in chords:
                        intervalIdx = 0
                        #Recorro todos los intervalos del acorde
                        for interval in chord.scale:
                            if note == interval:       
                                value = (degree, chordIdx)  
                                if value not in self.chordAnalysis[slice]:
                                    self.chordAnalysis[slice][value] = 0                       
                                self.chordAnalysis[slice][value] += (chordWeight[intervalIdx] * tickWeight * notPlayingAtTickPen)
                                break
                            intervalIdx += 1
                        chordIdx += 1

    def print_chord_analysis(self):
        idx = 0
        for chordList in self.chordAnalysis:
            print(f"Slice {idx}:")
            idx += 1
            for chord, w in chordList.items():
                print(f"{chord[0]} {self.harmony.chords[chord[0]][chord[1]]}: {w}")

    def print_best_chords(self):
        idx = 0
        for chord in self.bestChords:
            if chord is not None:
                print(f"Slice {idx}: {chord[0]} {self.harmony.chords[chord[0]][chord[1]]}")  
            else:
                print(f"Slice {idx}")
            idx += 1

    '''
    Dada la tónica de la canción, se relativizan todas las notas, 
    transformándose en el intervalo correspondiente que ocupan en la escala
    '''    
    def __relativize_song(self):

        self.relativazedSong = []

        pTonic = -(self.tonic.pitch - 12)

        for note in self.melody:
            self.relativazedSong.append({           
                'note': Interval.Interval((note['note'] + pTonic) % 12),  
                'start_time': note['start_time'], 
                'duration': note['duration']     
            })

    '''
    Elige el acorde con más peso de cada fragmento 
    '''
    def __choose_best_chords(self):

        self.bestChords = []

        for slice in self.chordAnalysis:
            maxWeight = 0
            bestChord = None
            for chord, weight in slice.items():
                if weight > maxWeight:
                    maxWeight = weight
                    bestChord = chord

            self.bestChords.append(bestChord)
    
    '''
    A partir de la tónica de la canción transforma los intervalos
    en notas reales traduciendo el análisis de armonía en "acordes de misa"
    '''
    def __translate_harmony(self, ticksPerSlice):

        songChordNotes = []

        idx = 0
        for chord in self.bestChords:

            if chord is not None:
                for interval in self.harmony.relativizedChords[chord[0]][chord[1]].scale:
                    songChordNotes.append({
                        "note": Note.get_pitch(interval, self.tonic, 3), 
                        "start_time": ticksPerSlice * idx, 
                        "duration": ticksPerSlice})
            
            idx += 1

        return songChordNotes




