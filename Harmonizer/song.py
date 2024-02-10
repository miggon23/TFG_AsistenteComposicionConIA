import scale as Scale
import note as Note
import harmony as Harmony
import interval as Interval
import timeSignature as TimeSignature
from timeSignature import TimeSignature as ts

import math
import random
import pandas as pd

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


    def armonize(self, 
                 type = "std", 
                 possibleChords = Harmony.allChords,
                 chordWeights = [1, 0.25, 0.5, 0.125], 
                 timeSignatures = [
                     ts(4, 4).set_weights([1.4, 1.1, 1.2, 1.1]),
                     ts(2, 4).set_weights([1.4, 1.2]),
                     ts(1, 4).set_weights([1])
                 ],               
                 notPlayingAtTickPen = 0.75,
                 offset = ts(1, 4),
                 ):
        
        self.harmony = Harmony.Harmony(self.scale, possibleChords)
        self.harmony.relativize_chords()
        
        if type == "std":
            self.__armonize(chordWeights, timeSignatures[0], notPlayingAtTickPen)  
            self.__choose_best_chords(timeSignatures[0].measure_size())               
        elif type == "win":
            timeSignatures = sorted(timeSignatures, key=lambda x: x.measure_size(), reverse=True)
            self.__win_armonize(chordWeights, timeSignatures, notPlayingAtTickPen)
            self.__combine_best_chords(timeSignatures[-1].measure_size())
        elif type == "off":
            self.__off_armonize(chordWeights, timeSignatures[0], notPlayingAtTickPen, offset)
            self.__combine_best_chords(offset.measure_size())
        
        return self.__absolutize_harmony()
    
    def __off_armonize(self, chordWeights, timeSignature, notPlayingAtTickPen, offset):

        lastTick = 0
        for note in self.melody:
            lastTick = max(lastTick, note['start_time'] + note['duration'])

        measureSize = timeSignature.measure_size()
        offsetSize = offset.measure_size()

        nMeasures = math.ceil(lastTick / (offsetSize * self.ticksPerBeat))   
        measureRelation = offsetSize / measureSize
        nMeasures = math.ceil(math.ceil(nMeasures * measureRelation) / measureRelation)
        combinedChordAnalysis = [{} for _ in range(nMeasures)]

        offset = 0
        while offset < measureSize:
            self.__armonize(chordWeights, timeSignature, notPlayingAtTickPen, offset)
            for measure in range(nMeasures):
                idx = int((measure * offsetSize + offset) / (offsetSize / measureRelation))
                if idx >= len(self.chordAnalysis):
                    break
                analysis = combinedChordAnalysis[measure]
                for chord, weight in self.chordAnalysis[idx].items():
                    if chord not in analysis:
                        analysis[chord] = 0
                    analysis[chord] += weight                 
            offset += offsetSize

        self.chordAnalysis = combinedChordAnalysis 
    
    def __win_armonize(self, chordWeights, timeSignatures, notPlayingAtTickPen):

        lastTick = 0
        for note in self.melody:
            lastTick = max(lastTick, note['start_time'] + note['duration'])

        shortestMeasure = timeSignatures[-1].measure_size()
        largestMeasure = timeSignatures[0].measure_size()

        nMeasures = math.ceil(lastTick / (shortestMeasure * self.ticksPerBeat))
        measureRelation = shortestMeasure / largestMeasure
        nMeasures = math.ceil(math.ceil(nMeasures * measureRelation) / measureRelation)
        combinedChordAnalysis = [{} for _ in range(nMeasures)]
        
        for timeSignature in timeSignatures:
            self.__armonize(chordWeights, timeSignature, notPlayingAtTickPen)
            measureRelation = shortestMeasure / timeSignature.measure_size()
            for measure in range(nMeasures):
                idx = int(measure * measureRelation)
                if idx >= len(self.chordAnalysis):
                    break
                analysis = combinedChordAnalysis[measure]
                for chord, weight in self.chordAnalysis[idx].items():
                    if chord not in analysis:
                        analysis[chord] = 0
                    analysis[chord] += weight

        self.chordAnalysis = combinedChordAnalysis            
    
    '''
    Divide la canción en compases uniformes para las cuales se busca el acorde más coherente
    Realiza un análisis armónico de la canción asignando pesos a los acordes dependiendo de varios factores:
        - La posición de la nota dentro del acorde (chordWeights)
        - El momento en el que suena la nota dentro de la propia ventana (chordWeights.weights)
        - Si la nota acaba de sonar o ya estaba sonando de antes (notPlayingAtTickPen)
    '''
    def __armonize(self, chordWeights, timeSignature, notPlayingAtTickPen, offset = 0):

        ticksPerMeasure = int(self.ticksPerBeat * timeSignature.measure_size())   
        ticksBetweenMeasureWeights = ticksPerMeasure // timeSignature.numerator     
        
        '''
        Relativizamos la canción,
        cambiamos su formato a canción separada
        y añadimos el offset 
        '''
        song = {0 : ([],[])} 
        offset = int(offset * self.ticksPerBeat)
        for tick, notes in spread_song(self.__relativize_melody()).items():
            song[tick + offset] = notes

        '''
        Calculo cuánto dura la canción mirando el tick en el que ocurren los últimos eventos   
        Creo la lista de compases, a las cuales les corresponderán un grupo de acordes con diferentes pesos
        '''    
        lastTick = list(song.keys())[-1]
        nMeasures = math.ceil(lastTick / ticksPerMeasure)
        self.chordAnalysis = [{} for _ in range(nMeasures)]

        '''
        A la hora de asignar pesos, el algoritmo tiene en cuenta los ticks clave dentro de cada compás,
        cada compás se subdivide equitativamente en el número de fragmentos que indique el numerador del compás
        Además, el peso que se asigne a un acorde se ve mermado dependiendo si la nota acaba 
        de empezar a sonar en el tick clave, o si sonaba anteriormente ("notPlayingAtTickPen")
        Puede dar la casualidad de que en un tick clave no termine ni comience una nota,
        para ello, incluyo en el diccionario de notas ticks "fantasma" en esos ticks clave, 
        para que el algoritmo tenga en cuenta también las notas que hayan comenzado a sonar anteriormente
        '''     
        tick = 0
        while (tick < nMeasures * ticksPerMeasure):
            if tick not in song:
                song[tick] = ([],[])
            tick += ticksBetweenMeasureWeights  
        song = dict(sorted(song.items()))  

        notesPlaying = []

        for tick, notes in song.items():

            measure = int(tick / ticksPerMeasure)
            if measure < nMeasures:
                analysis = self.chordAnalysis[measure]
            else:
                break

            #Notas que abacan de terminar, se eliminan de la lista
            volatileNotes = []      
            for note in notes[1]:
                if note in notesPlaying: 
                    notesPlaying.remove(note) 
                else:
                    notes[0].remove(note)
                    volatileNotes.append(note)

            '''
            Comprueba si toca tick clave
            En caso afirmativo, actualizo el incremento de peso por tick clave a su correspondiente (tickWeightNow)
            Además, recorro las notas que empezaron a sonar en ticks anteriores para incrementar los pesos
            '''    
            tickWeight = 1
            if tick % ticksBetweenMeasureWeights == 0:
                weightIdx = (tick - measure * ticksPerMeasure) // ticksBetweenMeasureWeights
                if timeSignature.weights[weightIdx] != None:
                    tickWeight = timeSignature.weights[weightIdx]
                    for note in notesPlaying:
                        self.__calculate_chord_weights(note, analysis, 
                            chordWeights, tickWeight, notPlayingAtTickPen)

            #Notas que acaban de empezar a sonar
            for note in notes[0]:
                notesPlaying.append(note)
                self.__calculate_chord_weights(note, analysis, chordWeights, tickWeight) 

            for note in volatileNotes:
                self.__calculate_chord_weights(note, analysis, chordWeights, tickWeight) 
    
    '''
    Dada una nota (y una serie de pesos), recorre toda la lista de acordes posibles para 
    comprobar que la nota esté en el acorde y sumarle el correspondiente peso en el correspondiente fragmento
    Dependiendo de la posición de la nota en el acorde los pesos serán distintos
    '''
    def __calculate_chord_weights(self, note, analysis, 
        chordWeights, tickWeight, notPlayingAtTickPen = 1):
         
        for (degree, chords), chordNames in zip(self.harmony.relativizedChords.items(), self.harmony.chords.values()):
            #Recorro todos los acordes de la lista de acordes
            for chord, chordName in zip(chords, chordNames):
                #Recorro todos los intervalos del acorde
                for intervalIdx, interval in enumerate(chord.scale):
                    if note == interval:       
                        value = (degree, chordName)  
                        if value not in analysis:
                            analysis[value] = 0                       
                        analysis[value] += (chordWeights[intervalIdx] * tickWeight * notPlayingAtTickPen)
                        break

    def print_chord_analysis(self):
        for idx, chordList in enumerate(self.chordAnalysis):
            print(f"Slice {idx}:")
            for chord, w in chordList.items():
                print(f"{chord[0]} {chord[1]}: {w}")

    def print_best_chords(self):
        for idx, chordInfo in enumerate(self.bestChords):

            chord = chordInfo[0]
            chordTicks = chordInfo[1]

            if chord is not None:
                print(f"Slice {idx} ({chordTicks} ticks): {chord[0]} {chord[1]}")  
            else:
                print(f"Slice {idx}")

    '''
    Elige el acorde con más peso de cada compás 
    '''
    def __choose_best_chords(self, measureSize):
    
        ticksPerChord = int(measureSize * self.ticksPerBeat)
        self.bestChords = []

        for analysis in self.chordAnalysis:
            maxWeight = 0
            bestChord = None
            for chord, weight in analysis.items():
                if weight > maxWeight:
                    maxWeight = weight
                    bestChord = chord

            self.bestChords.append([bestChord, ticksPerChord])

    '''
    Elige el acorde con más peso de cada compás 
    y combina las iguales adyacentes
    '''
    def __combine_best_chords(self, measureSize):
        
        ticksPerChord = int(measureSize * self.ticksPerBeat)
        self.bestChords = [[(0, ""), 0]] 

        for analysis in self.chordAnalysis:
            maxWeight = 0
            bestChord = None
            for chord, weight in analysis.items():
                if weight > maxWeight:
                    maxWeight = weight
                    bestChord = chord

            if bestChord == self.bestChords[-1][0]:
                self.bestChords[-1][1] += ticksPerChord
            else:
                self.bestChords.append([bestChord, ticksPerChord])

        self.bestChords = self.bestChords[1:]

    def save_data(self, filePath):
        self.__save_matrix(filePath + ".xlsx")
        self.__save_raw(filePath + ".csv")

    def __save_raw(self, filePath):

        try:
            df = pd.read_csv(filePath)  
            data = {'chord': [], 'duration': []}       
        except FileNotFoundError:
            df = pd.DataFrame(columns=['chord', 'duration'])
            data = {'chord': ["start_end"], 'duration': [0]} 

        for chordInfo in self.bestChords:

            chord = chordInfo[0]
            if chord is not None:
                chord = chord[0] + "_" + chord[1]
                duration = chordInfo[1]

                data['chord'].append(chord)
                data['duration'].append(duration)

        data['chord'].append("start_end")
        data['duration'].append(0)       

        df = pd.concat([df, pd.DataFrame(data)], ignore_index=True)
        df.to_csv(filePath, index=False)

    def __save_matrix(self, filePath):

        lastChord = "start_end"

        try:
            df = pd.read_excel(filePath, index_col=0)
        except FileNotFoundError:
            initialData = {lastChord: [0]}
            df = pd.DataFrame(initialData, index=[lastChord])

        reorganize = False

        for chordInfo in self.bestChords:

            chord = chordInfo[0]
            if chord is not None:
                chord = chord[0] + "_" + chord[1]

                if chord not in df.index:
                    df[chord] = 0
                    df.loc[chord] = 0
                    reorganize = True

                df.at[lastChord, chord] += 1

                lastChord = chord

        df.at[lastChord, "start_end"] += 1

        if reorganize:  

            def foo(chord):
                chord = str(chord)
                if chord == "start_end":
                    return -1
                else:
                    degree, chordName = chord.split("_")
                    v1 = Interval.intervals.index(degree)
                    v2 = list(Harmony.allChords.keys()).index(chordName)
                    return v1 * len(Harmony.allChords) + v2

            indexes = sorted(df.index.tolist(), key=foo)
            df = df.reindex(index=indexes, columns=indexes)       

        df.to_excel(filePath)

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

                idx = self.harmony.chords[chord[0]].index(chord[1])
                relativazedChord = self.harmony.relativizedChords[chord[0]][idx]

                for interval in relativazedChord.scale:
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
                    
                    

                    


                    




    




