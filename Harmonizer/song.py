import scale as Scale
import note as Note
import harmony as Harmony
import interval as Interval
import math
import random

stdWeights = {
    "chordWeight": [1, 0.25, 0.5, 0.25],
    "tickWeights": [1.4, 1.1, 1.2, 1.1],
    "advancedTickWeights": None,
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

    def __init__(self, melody, ticksPerBeat):

        self.ticksPerBeat = ticksPerBeat

        self.melody = melody
        self.tonic = Note.Note(self.melody[0]['note']  % 12)
        
        pTonic = -(self.tonic.pitch - 12) 
        intervals = []
  
        self.meanPitch = 0
        totalSoundDuration = 0

        for note in self.melody:

            pitch = note['note']
            duration = note['duration']

            self.meanPitch += pitch * duration
            totalSoundDuration += duration

            interval = (pitch + pTonic) % 12
            if interval not in intervals:
                intervals.append(interval)
      
        intervals.sort()
        self.scale = Scale.Scale(intervals) 

        self.meanPitch /= totalSoundDuration   
        
    def choose_scale(self):
        if (self.scale.len() > 7):
            return
        
        print(f"Escala base: ", end="")
        self.scale.print_scale()
        print(f"Tónica base: {self.tonic.name}")
        print(f"Grados:", end="\n")
        self.scale.create_degrees()
        self.scale.print_degrees()

        degrees = self.scale.degrees
        degrees.insert(0, self.scale)     

        fittingScales = []

        for i, degree in enumerate(degrees):
            for name, scale in possibleScales.items():
                if scale.contains(degree):
                    tonic = Note.Note((self.tonic.pitch + self.scale.scale[i].semitones) % 12)
                    fittingScales.append((tonic, name))
                    print(f"Escala {name} coincidente con tónica en {tonic.name}")

        if not fittingScales:

            print(f"No hay escala tonal coincidente cuya tónica sea alguna de las notas de la melodía")

            majorDegrees = possibleScales["Major"].copy()
            majorDegrees.create_degrees()
            majorDegrees = majorDegrees.degrees

            for i, degree in enumerate(degrees):
                for j, majorDegree in enumerate(majorDegrees, start=1):
                    if majorDegree.contains(degree):
                        tonic = Note.Note(self.tonic.pitch + self.scale.scale[i].semitones)
                        print(f"Modo {possibleScales['Major'].scale[j].get_name()} coincidente con tónica en {tonic.name}")
                        tonic = Note.Note(tonic.pitch - possibleScales['Major'].scale[j].semitones)
                        print(f"Se traduce a una escala Mayor con tónica en {tonic.name}")
                        fittingScales.append((tonic, "Major"))

        if not fittingScales:
             print(f"No hay ninguna escala tonal coincidente")
             return

        finalScale = fittingScales[random.randint(0, len(fittingScales) - 1)]
        self.tonic = finalScale[0]
        self.scale = possibleScales[finalScale[1]].copy()

        self.scale.absolutize_scale(self.tonic)
        print("Escala elegida:")
        self.scale.print_scale()
        self.scale.print_absolutized_scale()    


    def armonize(self, type = "std", 
                 windowSize = 4, windowSizes = [1, 2, 4], offset = 1,
                 weights = stdWeights, 
                 possibleChords = Harmony.allChords):
        
        self.harmony = Harmony.Harmony(self.scale, possibleChords)
        self.harmony.relativize_chords()
        
        if type == "std":
            self.__armonize(windowSize, weights)  
            self.__choose_best_chords(windowSize)               
        elif type == "win":
            self.__win_armonize(windowSizes, weights)
            self.__combine_best_chords(windowSizes[0])
        elif type == "off":
            self.__off_arminize(windowSize, offset, weights)
            self.__combine_best_chords(windowSize)
        
        return self.__absolutize_harmony()
    
    def __off_arminize(self, windowSize, offset, weights):
        return
    
    def __win_armonize(self, windowSizes, weights):

        if weights['advancedTickWeights'] is None:

            advancedTickWeights = weights['advancedTickWeights'] = []
            nWeights = len(weights['tickWeights'])

            for windowSize in windowSizes:
                if windowSize <= 1:
                    advancedTickWeights.append([1])
                else:
                    advancedTickWeights.append(weights['tickWeights'][:min(windowSize, nWeights)])

        weights['tickWeights'] = weights['advancedTickWeights'][0]
        self.__armonize(windowSizes[0], weights)
        
        combinedChordAnalysis = self.chordAnalysis.copy()
        # for _ in range(math.ceil(math.ceil(len(combinedChordAnalysis) * windowSizes[0] / windowSizes[-1]) * (windowSizes[-1] / windowSizes[0])) - len(combinedChordAnalysis)):
        #     combinedChordAnalysis.append({})
        nWindows = len(combinedChordAnalysis)
        
        for windowIdx, windowSize in enumerate(windowSizes[1:], start=1):
            weights['tickWeights'] = weights['advancedTickWeights'][windowIdx]
            self.__armonize(windowSize, weights)
            windowsRelation = windowSizes[0] / windowSize
            for window in range(nWindows):
                windowIdx = int(window * windowsRelation)
                if windowIdx >= len(self.chordAnalysis):
                    break
                chords = self.chordAnalysis[windowIdx]
                windowAnalysis = combinedChordAnalysis[window]
                for chord, weight in chords.items():
                    if chord not in windowAnalysis:
                        windowAnalysis[chord] = 0
                    windowAnalysis[chord] += weight

        self.chordAnalysis = combinedChordAnalysis            
    
    '''
    Divide la canción en ventanas equivalentes para las cuales se busca el acorde más coherente
    Realiza un análisis armónico de la canción asignando pesos a los acordes dependiendo de varios factores:
        - La posición de la nota dentro del acorde ("chordWeight": [w1ª, w3ª, w5ª, ...])
        - El momento en el que suena la nota dentro de la propia ventana ("tickWeights": [w0, w1, w2, ...])
        - Si la nota acaba de sonar o ya estaba sonando de antes ("notPlayingAtTickPen" = w)
    '''
    def __armonize(self, windowSize, weights):

        '''
        Queremos saber cuántos ticks ocupa una ventana
        El problema viene cuando se quieren generar ventanas más peqeñas que una negra (beat)
        Si en una negra no caben exactamente n ventanas habrá un desplazamiento en los ticks,
        ya que estos son una representación simbólica del tiempo
        Para solucionar esto se reescala toda la canción, es decir, se aumentan los ticks que
        duran todas las notas, aumentamndo también la cantidad de ticks que dura una negra (beat)
        Se utiliza el mínimo común múltiplo para realizar este reescalado, de esta forma se 
        asegura que en un beat quepan n ventanas exactas
        '''
        if windowSize >= 1:  
            ticksPerWindow = windowSize * self.ticksPerBeat
        else:
            windowsPerBeat = int(1 / windowSize)
            if self.ticksPerBeat % windowsPerBeat != 0:
                self.__resize_song(windowsPerBeat)
            ticksPerWindow = self.ticksPerBeat // windowsPerBeat

        '''
        Pasa algo similar a la hora de dividir la ventana en 
        puntos clave para valorar los pesos
        '''
        windowSlices = len(weights["tickWeights"])
        if ticksPerWindow % windowSlices != 0:
            ticksPerWindow *= self.__resize_song(windowSlices)
        weightTickIterval = ticksPerWindow // len(weights["tickWeights"])

        '''
        La canción ya no sufrirá más reescalados, así que la podemos
        reconvertir en la representación final que utilizará el algoritmo
        Relativizamos toda la canción y cambiamos su formato a canción separada
        '''
        relativizedSong = self.__relativize_melody()
        relativizedSpreadSong = spread_song(relativizedSong)

        '''
        Calculo cuánto dura la canción mirando el tick en el que ocurren los últimos eventos   
        Creo la lista de ventanas, a las cuales les corresponderán un grupo de acordes con diferentes pesos
        '''    
        lastTick = list(relativizedSpreadSong.keys())[-1]
        nWindows = math.ceil(lastTick / ticksPerWindow)
        self.chordAnalysis = [{} for _ in range(nWindows)]

        '''
        A la hora de asignar pesos, el algoritmo tiene en cuenta ticks clave dentro de cada ventana,
        cada ventana se subdivide equitativamente en el número de fragmentos que haya en la lista ("tickWeights": [w0, w1, w2, ...])
        Además, el peso que se asigne a un acorde se ve mermado dependiendo si la nota acaba 
        de empezar a sonar en el tick clave, o sonaba anteriormente ("notPlayingAtTickPen": w)
        Puede dar la casualidad de que en un tick clave no termine ni comience una nota,
        para ello, incluyo en el diccionario de notas ticks "fantasma" en esos ticks clave, 
        para que el algoritmo tenga en cuenta también las notas que hayan comenzado a sonar anteriormente
        '''  
        tick = 0
        while (tick < nWindows * ticksPerWindow):
            if tick not in relativizedSpreadSong:
                relativizedSpreadSong[tick] = ([],[])
            tick += weightTickIterval  
        relativizedSpreadSong = dict(sorted(relativizedSpreadSong.items()))  

        notesPlaying = []

        for tick, notes in relativizedSpreadSong.items():

            #Notas que abacan de terminar, se eliminan de la lista
            for note in notes[1]:
                #Si hay un error aquí es posible que haya notas de 0 segundos de duración
                notesPlaying.remove(note) 

            window = int(tick / ticksPerWindow)

            '''
            Comprueba si toca tick clave
            En caso afirmativo, actualizo el incremento de peso por tick clave a su correspondiente (tickWeightNow)
            Además, recorro las notas que empezaron a sonar en ticks anteriores para incrementar los pesos
            '''    
            tickWeight = 1
            if tick % weightTickIterval == 0:
                weightIdx = (tick - window * ticksPerWindow) // weightTickIterval
                tickWeight = weights["tickWeights"][weightIdx]
                for note in notesPlaying:
                    self.__calculate_chord_weights(note, window, 
                        weights["chordWeight"], tickWeight, weights["notPlayingAtTickPen"])

            #Notas que acaban de empezar a sonar
            for note in notes[0]:
                notesPlaying.append(note)
                self.__calculate_chord_weights(note, window, weights["chordWeight"], tickWeight) 
    
    '''
    Dada una nota (y una serie de pesos), recorre toda la lista de acordes posibles para 
    comprobar que la nota esté en el acorde y sumarle el correspondiente peso en el correspondiente fragmento
    Dependiendo de la posición de la nota en el acorde los pesos serán distintos
    '''
    def __calculate_chord_weights(self, note, window, 
        chordWeight, tickWeight, notPlayingAtTickPen = 1):
         
        for degree, chords in self.harmony.relativizedChords.items():
            #Recorro todos los acordes de la lista de acordes
            for chordIdx, chord in enumerate(chords):
                #Recorro todos los intervalos del acorde
                for intervalIdx, interval in enumerate(chord.scale):
                    if note == interval:       
                        value = (degree, chordIdx)  
                        if value not in self.chordAnalysis[window]:
                            self.chordAnalysis[window][value] = 0                       
                        self.chordAnalysis[window][value] += (chordWeight[intervalIdx] * tickWeight * notPlayingAtTickPen)
                        break

    def print_chord_analysis(self):
        for idx, chordList in enumerate(self.chordAnalysis):
            print(f"Slice {idx}:")
            for chord, w in chordList.items():
                print(f"{chord[0]} {self.harmony.chords[chord[0]][chord[1]]}: {w}")

    def print_best_chords(self):
        for idx, chordInfo in enumerate(self.bestChords):

            chord = chordInfo[0]
            chordTicks = chordInfo[1]

            if chord is not None:
                print(f"Slice {idx} ({chordTicks} ticks): {chord[0]} {self.harmony.chords[chord[0]][chord[1]]}")  
            else:
                print(f"Slice {idx}")

    def __resize_song(self, newTicksPerBeat):

        newTicksPerBeat = math.lcm(self.ticksPerBeat, newTicksPerBeat)
        increment = newTicksPerBeat // self.ticksPerBeat

        for note in self.melody:
            note['start_time'] *= increment
            note['duration'] *= increment

        self.ticksPerBeat = newTicksPerBeat

        return increment

    '''
    Elige el acorde con más peso de cada ventana 
    '''
    def __choose_best_chords(self, beatsPerWindow):
    
        ticksPerChord = int(beatsPerWindow * self.ticksPerBeat)
        self.bestChords = []

        for slice in self.chordAnalysis:
            maxWeight = 0
            bestChord = None
            for chord, weight in slice.items():
                if weight > maxWeight:
                    maxWeight = weight
                    bestChord = chord

            self.bestChords.append([bestChord, ticksPerChord])

    '''
    Elige el acorde con más peso de cada ventana 
    y combina las iguales adyacentes
    '''
    def __combine_best_chords(self, beatsPerWindow):
        
        ticksPerChord = int(beatsPerWindow * self.ticksPerBeat)
        self.bestChords = [[(-1, 0), 0]] 

        for slice in self.chordAnalysis:
            maxWeight = 0
            bestChord = None
            for chord, weight in slice.items():
                if weight > maxWeight:
                    maxWeight = weight
                    bestChord = chord

            if bestChord == self.bestChords[-1][0]:
                self.bestChords[-1][1] += ticksPerChord
            else:
                self.bestChords.append([bestChord, ticksPerChord])

        self.bestChords = self.bestChords[1:]


    '''
    A partir de la tónica de la canción transforma las notas reales en intervalos 
    '''
    def __relativize_melody(self):

        relativazedMelody = []
        pTonic = -(self.tonic.pitch - 12)

        for note in self.melody:
            relativazedMelody.append({           
                'note': Interval.Interval((note['note'] + pTonic) % 12),  
                'start_time': note['start_time'], 
                'duration': note['duration']     
            })

        return relativazedMelody
 
    '''
    A partir de la tónica de la canción transforma los intervalos
    en notas reales traduciendo el análisis de armonía en "acordes de misa"
    '''
    def __absolutize_harmony(self):

        absolutizedHarmony = []

        startTime = 0
        for chordInfo in self.bestChords:

            chord = chordInfo[0]
            chordTicks = chordInfo[1]

            if chord is not None:
                for interval in self.harmony.relativizedChords[chord[0]][chord[1]].scale:
                    absolutizedHarmony.append({
                        "note": Note.get_nearest_pitch(interval, self.tonic, self.meanPitch - 12), 
                        "start_time": startTime, 
                        "duration": chordTicks})
                    
            startTime += chordTicks

        return absolutizedHarmony
    
    def process_bassline_4x4(self, bassline):
        
        processedBassline = []
        
        bar = 0
        note = None
        for chord in self.bestChords:

            tonic = Interval.Interval(chord[0])
            tonicIdx = 0
            for intrval in self.scale.scale:
                if tonic == intrval:
                    break
                tonicIdx += 1

            tick = 0
            for i in bassline[bar % len(bassline)]:

                if i >= 0:  

                    if note is not None:
                        note['duration'] += 0.25 * self.ticksPerBeat
                        processedBassline.append(note)
                    
                    if i > 0:
                        interval = self.scale.scale[(tonicIdx + (i - 1)) % self.scale.len()]
                        note  = {
                            "note": Note.get_nearest_pitch(interval, self.tonic, self.meanPitch - 12 * 2), 
                            "start_time": bar + tick * 0.25, 
                            "duration": 0 }                       
                    else:
                        note = None

                elif i < 0 and note is not None:
                    note['duration'] += 0.25 * self.ticksPerBeat

                tick += 1 * self.ticksPerBeat

            bar += 1

        if note is not None:
            note['duration'] += 0.25 * self.ticksPerBeat
            processedBassline.append(note)

        return processedBassline
    

    def process_bassline_4x4_v2(self, bassline, harmony):
        
        processedBassline = []

        note = None

        chordNoteIdx = 0
        bar = harmony[chordNoteIdx]['start_time']
        lowestPitch = harmony[chordNoteIdx]['note']
        chordNoteIdx += 1

        patternIdx = 0

        while chordNoteIdx < len(harmony):

            while chordNoteIdx < len(harmony) and bar == harmony[chordNoteIdx]['start_time']:
                lowestPitch = min(lowestPitch, harmony[chordNoteIdx]['note'])
                chordNoteIdx += 1

            tonic = Interval.Interval(abs((lowestPitch - self.tonic.pitch) % 12))
            tonicIdx = 0
            for intrval in self.scale.scale:
                if tonic == intrval:
                    break
                tonicIdx += 1

            tick = 0

            for i in bassline[patternIdx]:

                if i >= 0:  

                    if note is not None:
                        note['duration'] += 0.25 * self.ticksPerBeat
                        processedBassline.append(note)
                    
                    if i > 0:
                        interval = self.scale.scale[(tonicIdx + (i - 1)) % self.scale.len()]
                        note  = {
                            "note": Note.get_nearest_pitch(interval, self.tonic, self.meanPitch - 12 * 2), 
                            "start_time": bar + tick * 0.25, 
                            "duration": 0 }                       
                    else:
                        note = None

                elif i < 0 and note is not None:
                    note['duration'] += 0.25 * self.ticksPerBeat

                tick += 1 * self.ticksPerBeat

            if chordNoteIdx < len(harmony):
                bar = harmony[chordNoteIdx]['start_time']
                lowestPitch = harmony[chordNoteIdx]['note']

            chordNoteIdx += 1
            patternIdx = (patternIdx + 1) % len(bassline)

        if note is not None:
            note['duration'] += 0.25 * self.ticksPerBeat
            processedBassline.append(note)

        return processedBassline
                    
                    

                    


                    




    




