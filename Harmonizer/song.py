import scale as Scale
import note as Note
import harmony as Harmony
import interval as Interval
import timeSignature as TimeSignature
from timeSignature import TimeSignature as ts

import math
import sys
import copy

'''
Reformatea la representación de la canción para que sea más fácil de operar para los diferentes algoritmos:
    song[tick] = (note_on[], note_off[])
'''
def note_seq(song):
    noteSeq = {}

    for note in song:

        key = note['start_time']

        for i in range(2):
            if key not in noteSeq:
                noteSeq[key] = ([],[])
            noteSeq[key][i].append(note['note'])

            key += note['duration']

    return dict(sorted(noteSeq.items()))

def debug_song(song, output_file):

    with open(output_file, 'w') as f:           
        for note in song:
            f.write(f"note: {note['note']}, Start Time: {note['start_time']}, Duration: {note['duration']}\n")

class Song:

    def __init__(self, notes, ticksPerBeat):

        self.ticksPerBeat = ticksPerBeat

        self.notes = notes

        self.tonic = Note.Note(self.notes[0]['note'] % 12)     
        pTonic = -(self.tonic.pitch - 12) 

        self.noteFrequencies = [0] * 12
        self.meanPitch = 0
        totalSoundDuration = 0

        intervals = []

        for note in self.notes:

            pitch = note['note']
            duration = note['duration']

            self.noteFrequencies[pitch % 12] += duration
            self.meanPitch += pitch * duration
            totalSoundDuration += duration

            interval = (pitch + pTonic) % 12
            if interval not in intervals:
                intervals.append(interval)

        self.meanPitch /= totalSoundDuration 
      
        intervals.sort()
        self.scale = Scale.Scale(intervals) 

    def __processed_chord_progressions(self, chordProgressions):

        processedChordProgressions = {}

        def add_chord(progresion):

            key = ""
            for chord in progresion:
                key += chord[0] + chord[1]
                    
            processedChordProgressions[key] = progresion

        for chordProgression in chordProgressions: 

            add_chord(copy.deepcopy(chordProgression["Progression"]))       

            for transition in chordProgression["Transitions"]:
                newProgresion = copy.deepcopy(chordProgression["Progression"])
                newProgresion.append(transition)
                add_chord(newProgresion)

        return list(processedChordProgressions.values())   
    
    def __choose_next_chord_progressions(self, previousChord, chordProgressions):
        
        newChordProgressions = []

        for chordProgression in chordProgressions:
            if previousChord == chordProgression[0]: 
                newChordProgressions.append(chordProgression)

        return newChordProgressions

    def find_chord_sequence(self, 
                            chordProgressions = Harmony.allChordProgressions,
                            chordWeights = [1, 0.25, 0.5, 0.125], 
                            timeSignatures = [
                                ts(4, 4).set_weights([1.4, 1.1, 1.2, 1.1]),
                                ts(2, 4).set_weights([1.4, 1.2]),
                                ts(1, 4).set_weights([1])
                            ],               
                            notPlayingAtTickPen = 0.75,):

        self.harmony = Harmony.Harmony()
        self.harmony.create_harmony_from_chord_progression_list(chordProgressions)
        self.harmony.relativize_chords()
        
        self.model = None

        chordProgressions = self.__processed_chord_progressions(chordProgressions)
        tonicPriority = sorted(range(len(self.noteFrequencies)), key=lambda i: self.noteFrequencies[i], reverse=True)

        bestSol = Song.ChordNode(-1, 0)
        bestTonic = None
        for tonic in tonicPriority:

            self.tonic = Note.Note(tonic)
            self.__win_armonize(chordWeights, timeSignatures, notPlayingAtTickPen)

            for idx, analysis in enumerate(self.chordAnalysis):
                self.chordAnalysis[idx] = dict(sorted(analysis.items(), key=lambda item: item[1], reverse=True))

            sol = self.__find_best_chord_sequence(chordProgressions)
            if sol is not None and sol.weight > bestSol.weight:
                bestSol = sol
                bestTonic = self.tonic


        if bestTonic is None:
            print("No hay solución")
        else:
            self.tonic = bestTonic
            self.__rebuild_solution(bestSol)
            self.__combine_best_chords(timeSignatures[-1].measure_size())
            return self.__absolutize_harmony()

    
    def __rebuild_solution(self, chordNode):

        self.chordAnalysis = [{} for _ in range(len(self.chordAnalysis))]

        chordProgression = None

        idx = len(self.chordAnalysis) - 1
        while chordNode is not None:
            if chordNode.chordProgression is not None:
                chordProgression = chordNode.chordProgression

            self.chordAnalysis[idx][chordProgression[chordNode.chord]] = 1
            idx -= 1

            chordNode = chordNode.last

    
    class ChordNode:
        def __init__(self, chord, weight, last = None):
            self.chord = chord
            self.weight = weight   
            self.last = last
            self.chordProgression = None

    def __find_best_chord_sequence(self, chordProgressions):

        nWindows = len(self.chordAnalysis)
        windows = [{} for _ in range(nWindows)]

        rootChordNode = Song.ChordNode(-1, 0)
        for chordProgression in chordProgressions:
            solutions = self.__chord_progression_combinatory(rootChordNode, chordProgression, -1)
            for depth, chordNode in solutions.items():
                lastChord = chordProgression[-1]
                if chordNode.chord not in windows[depth] or chordNode.weight > windows[depth][lastChord].weight:
                    chordNode.chordProgression = chordProgression
                    windows[depth][lastChord] = chordNode

        for n in range(nWindows - 1):
            for lastChord, ch in windows[n].items():
                selChordProg = self.__choose_next_chord_progressions(lastChord, chordProgressions)
                for chordProgression in selChordProg:
                    solutions = self.__chord_progression_combinatory(ch, chordProgression, n)
                    for depth, chordNode in solutions.items():
                        lastChord = chordProgression[-1]
                        if chordNode.chord not in windows[depth] or chordNode.weight > windows[depth][lastChord].weight:
                            chordNode.chordProgression = chordProgression
                            windows[depth][lastChord] = chordNode

        bestChordSequence = None
        for chordNode in windows[-1].values():
            if bestChordSequence is None or bestChordSequence.weight < chordNode.weight:
                bestChordSequence = chordNode

        return bestChordSequence


    
    def __chord_progression_combinatory(self, prevChordNode, chordProgresion, windowIdx):
        
        prevChordNodeChord = prevChordNode.chord
        prevChordNode.chord = min(prevChordNodeChord, 0)

        pendingChords = [prevChordNode]
        nextChords = []  
        solutions = {}

        for depth, chordAnalysis in enumerate(self.chordAnalysis[(windowIdx + 1):], start=windowIdx + 1):

            for chordNode in pendingChords:  

                chordIdx = chordNode.chord
                if chordIdx >=0 and chordProgresion[chordIdx] in chordAnalysis:
                    newChordNode = Song.ChordNode(chordIdx, 
                                chordNode.weight + chordAnalysis[chordProgresion[chordIdx]], 
                                chordNode)
                    nextChords.append(newChordNode)

                chordIdx += 1
                if chordProgresion[chordIdx] in chordAnalysis:
                    newChordNode = Song.ChordNode(chordIdx, 
                                chordNode.weight + chordAnalysis[chordProgresion[chordIdx]],
                                chordNode)
                    if chordIdx < len(chordProgresion) - 1:
                        nextChords.append(newChordNode)
                    elif depth not in solutions or newChordNode.weight > solutions[depth].weight:
                        solutions[depth] = newChordNode

            pendingChords = nextChords
            nextChords = []

            if not pendingChords:
                break
              
        if pendingChords:
            if depth in solutions:
                idx = 0        
            else:
                solutions[depth] = pendingChords[0]
                idx = 1
            for chordNode in pendingChords[idx:]:
                if chordNode.weight > solutions[depth].weight:
                    solutions[depth] = chordNode

        prevChordNode.chord = prevChordNodeChord

        return solutions                 

    '''
    Elige una escala entre la lista de escalas provista en el supuesto de que la canción tenga 
    menos de 7 notas (la escala formada originalmente es incompleta) con el siguiente criterio:
        Se prioriza la escala a elegir por su orden en la lista
        Si hay una escala que cubre el conjunto de notas con tónicas diferentes, 
        se elegira la nota más frecuente
        Existen dos iteraciones:
            1- Se asume que la tónica se encuantra en este conjunto
            2- No se ha encontrado ningún par (escala, tónica) que compla con 
            el criterio 1, así que se busca una escala cuya tónica no pertenezca 
            al conjunto original de notas
        A pesar de todo ello podría ocurrir que no se encuentre ninguna escala que cumpla
        los requisitos, en ese caso, se conservara la escala original y se devolverá False
    '''
    def fill_scale(self, possibleScales = Scale.allScales):
        if (self.scale.len() >= 7):
            return True
        
        print(f"Escala base:", end="\n")
        self.scale.create_degrees()
        self.scale.print_degrees()
        print(f"Tónica base: {self.tonic.name}")
        
        degrees = self.scale.degrees
        degrees.insert(0, self.scale)     

        fittingTonics = []

        for name, possibleScale in possibleScales.items():
            for degreeIdx, degree in enumerate(degrees):
                if possibleScale.containsScale(degree):
                    tonic = Note.Note((self.tonic.pitch + self.scale.scale[degreeIdx].semitones) % 12)
                    fittingTonics.append(tonic)
                    print(f"Escala {name} coincidente con tónica en {tonic.name}")
            if fittingTonics:
                self.scale = possibleScale
                break

        if not fittingTonics:
            print(f"No hay escala coincidente cuya tónica sea alguna de las notas del conjunto")

            for name, possibleScale in possibleScales.items():
                possibleScale.create_degrees()
                pDegrees = possibleScale.degrees
                for degreeIdx, degree in enumerate(degrees):
                    for pDegreeIdx, pDegree in enumerate(pDegrees, start=1):
                        if pDegree.containsScale(degree):
                            tonic = Note.Note((self.tonic.pitch + 
                                    self.scale.scale[degreeIdx].semitones - 
                                    possibleScale.scale[pDegreeIdx].semitones) % 12)
                            fittingTonics.append(tonic)
                            print(f"Escala {name} coincidente con tónica en {tonic.name}")
                if fittingTonics:
                    self.scale = possibleScale
                    break

        if not fittingTonics:
             print(f"No hay ninguna escala tonal coincidente")
             return False
        
        bestResult = -1
        for tonic in fittingTonics:
            result = self.noteFrequencies[tonic.pitch]
            if result > bestResult:
                bestResult = result
                self.tonic = tonic

        print(f"Escala elegida:", end="\n")
        self.scale.create_degrees()
        self.scale.print_degrees()
        print(f"Tónica elegida: {self.tonic.name}")
        self.scale.absolutize_scale(self.tonic)
        self.scale.print_absolutized_scale() 

        return True

    def most_frequent_note(self):
        return Note.Note(self.noteFrequencies.index(max(self.noteFrequencies))) 

    '''
    Establece la escala de la canción y su tónica
    En caso de omitir la tónica, esta se busca de forma que la tonalidad
    cuya tónica deje menos notas fuera de la escala es la elegida
    En caso de empata se elige la nota más frecuente como tónica
    '''
    def choose_sacle(self, scale, tonic = None):

        if tonic is not None:
            self.tonic = tonic
            self.scale = scale
            return

        self.scale.create_degrees()
        degrees = self.scale.degrees
        degrees.insert(0, self.scale)

        bestDegrees = []
        bestResult = scale.len()

        for idx, degree in enumerate(degrees):

            scaleIdx = 0
            degreeIdx = 0

            cont = scale.len()

            while scaleIdx < scale.len() and degreeIdx < degree.len():
                if scale.scale[scaleIdx] == degree.scale[degreeIdx]:
                    cont -= 1
                    scaleIdx += 1
                    degreeIdx += 1
                elif scale.scale[scaleIdx] < degree.scale[degreeIdx]:
                    scaleIdx += 1
                else:
                    degreeIdx += 1

            if cont == bestResult:
                bestDegrees.append(idx)
            elif cont < bestResult:
                bestDegrees = [idx]
                bestResult = cont

        bestResult = 0
            
        for idx in bestDegrees:
            result = self.noteFrequencies[(self.tonic.pitch + self.scale.scale[idx].semitones) % 12]
            if result > bestResult:
                bestResult = result
                bestDegree = idx
       
        self.tonic = Note.Note((self.tonic.pitch + self.scale.scale[bestDegree].semitones) % 12)
        self.scale = scale

        print(f"Tónica elegida: {self.tonic.name}") 

    '''
    Ajusta las notas a la escala, midiendo la distancia de edición:
        ditancia = distancia en semitonos * penalización por distancia + penalización de la nota
    Si las penalizaciones por cada nota son muy dispares puede ocurrir que notas que 
    originalmente sí pertenacían a la escala se reajusten a otras de menor penalización
    '''
    def fit_notes(self, distancePenalty = 1, notePenalties = None):

        if notePenalties is None:
            notePenalties = [0] * self.scale.len()
        elif len(notePenalties) != self.scale.len():
            raise Exception("Tamaños no coincidentes")

        scalePitches = []
        for interval in self.scale.scale:
            scalePitches.append((self.tonic.pitch + interval.semitones) % 12)
 
        for note in self.notes:
            notePitch = note['note'] % 12

            pitchDistances = []
            for scalePitch in scalePitches:
                if scalePitch < notePitch:
                    pitchDistances.append(min(notePitch - scalePitch, scalePitch + 12 - notePitch))
                elif scalePitch > notePitch:
                    pitchDistances.append(min(scalePitch - notePitch, notePitch + 12 - scalePitch))
                else:
                    pitchDistances.append(0)

            lowestDistance = sys.maxsize  
            for pitchIdx, (pitchDistance, notePenalty) in enumerate(zip(pitchDistances, notePenalties)):
                distance = pitchDistance * distancePenalty + notePenalty
                if distance < lowestDistance:
                    lowestDistance = distance
                    newPitchIdx = pitchIdx

            if (notePitch + pitchDistances[newPitchIdx]) % 12 == scalePitches[newPitchIdx]:
                note['note'] += pitchDistances[newPitchIdx]
            else:
                note['note'] -= pitchDistances[newPitchIdx]

    """
    Armoniza la música según ciertos parámetros.

    :param type: Algoritmo para la armonización ("std", "win", "off"). El bueno es el win.
    :type type: str

    :param possibleChords: Lista de acordes posibles (por ahora utiliza el valor por defecto).
    :type possibleChords: Lista de acordes

    :param chordWeights: Pesos de las notas de los acordes
    :type chordWeights: Lista de cuatro floats mayores que 0

    :param timeSignatures: Representan los tamaño de ventana y los pesos de los pulsos fuertes (por ahora utiliza el valor por defecto).
    :type TimeSignature[]: Lista de TimeSignatures 

    :param notPlayingAtTickPen: penalización por no sonar en un tic fuerte
    :type notPlayingAtTickPen: float entre 0 y 1

    :param offset: Desplazamiento a partir del cual empieza la armonización (por ahora utiliza el valor por defecto).
    :type offset: TimeSignature

    :return: Lista con todas las notas de todos los acordes
    :rtype: [{'note': note, 
                'start_time': start_time, 
                'duration': duration]},
            {'note': note2, 
                'start_time': start_time, 
                'duration': duration]}, 
            ...]
    """
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
                model = None
            ):
        
        self.model = model
        
        self.harmony = Harmony.Harmony()
        self.harmony.create_harmony_from_scale(self.scale, possibleChords)
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
        for note in self.notes:
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
        for note in self.notes:
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
        for tick, notes in note_seq(self.__relativized_notes()).items():
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
      
        self.__bias()

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

    '''
    Modifica los pesos con el objetivo de hacer una media entre 
    los datos obtenidos por el algoritmo y lo que dicte el modelo utilizado
    '''
    def __bias(self, ratio = 0.5, nChordSequence = 4, nBestChords = sys.maxsize, reverse = False):

        if self.model is None:
            return

        lastChord = None

        for idx, chords in enumerate(self.chordAnalysis):

            chords = dict(sorted(chords.items(), key=lambda x: x[1], reverse=True))
            chords = dict(list(chords.items())[:min(nBestChords, len(chords))])   

            for chord in chords:
                weight = chords[chord]
                chords[chord] = 2 * self.model.predict([lastChord], chord) * weight * ratio + weight * (1 - ratio)

            self.chordAnalysis[idx] = dict(sorted(chords.items(), key=lambda x: x[1], reverse=True))

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

    '''
    A partir de la tónica de la canción transforma las notas reales en intervalos 
    '''
    def __relativized_notes(self):

        relativazedNotes = []
        pTonic = -(self.tonic.pitch - 12)

        for note in self.notes:
            relativazedNotes.append({           
                'note': Interval.Interval((note['note'] + pTonic) % 12),  
                'start_time': note['start_time'], 
                'duration': note['duration']     
            })

        return relativazedNotes
 
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
    
    def divide_song(self, ticks):

        limit = self.ticksPerBeat * ticks

        song1 = []
        song2 = []

        for note in self.notes:
            if note['start_time'] + note['duration'] <= limit:
                song1.append({
                    'note': note['note'], 
                    'start_time': note['start_time'], 
                    'duration': note['duration']
                })
            elif note['start_time'] >= limit:
                song2.append({
                    'note': note['note'], 
                    'start_time': note['start_time'] - limit, 
                    'duration': note['duration']
                })
            else:
                song1.append({
                    'note': note['note'], 
                    'start_time': note['start_time'], 
                    'duration': limit - note['start_time']
                })
                song2.append({
                    'note': note['note'], 
                    'start_time': 0, 
                    'duration': note['start_time'] + note['duration'] - limit
                })
        
        return Song(song1, self.ticksPerBeat), Song(song2, self.ticksPerBeat)

    def __iadd__(self, song):

        for note in song.notes:
            self.notes.append(note)

        return Song(self.notes, self.ticksPerBeat)
    
    def traspose(self, semitones):
        for note in self.notes:
            note['note'] += semitones


                    
                    

                    


                    




    




