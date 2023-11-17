import pandas as pd
import numpy as np
from note_seq import NoteSequence, midi_io

from pydtmc import MarkovChain
import os
from pathlib import Path

from enum import Enum

#QPM estandar para pasar a MIDI (1 negra por segundo)
QPM = 60

#Valor estandar de un step, para normalizar#
STEP_VALUE = 1/4

MAX_SILENCE_STEPS = 8
MAX_SILENCE_SECONDS = 2

name_pitch = {
    "C": 0,
    "C_SHARP": 1,
    "D_FLAT": 1,
    "D": 2,
    "D_SHARP": 3,
    "E_FLAT": 3,
    "E": 4,
    "F": 5,
    "F_SHARP": 6,
    "G_FLAT": 6,
    "G": 7,
    "G_SHARP": 8,
    "A_FLAT": 8,
    "A": 9,
    "A_SHARP": 10,
    "B_FLAT": 10,
    "B": 11,
}

CMajor_notes = [ 0, 2, 4, 5, 7, 9, 11 ]

is_CMajor_note = [ True, False, True, False, True, True, False, True, False, True, False, True ]

class Markov_Generator:

    def __init__(self, use_steps = True, use_silences = True, smooth_ocurrences = True, normalize_scale = True):
        self.step_mode = use_steps
        self.has_silences = use_silences
        self.smooth_ocurrences = smooth_ocurrences
        self.normalize_scale = normalize_scale

    def getScale(self, noteSeq):
        keySignatures = noteSeq.get("keySignatures", 0)
        
        if (keySignatures != 0):
            return keySignatures[0].get("key", "C")

        return "C"

    #Anade una nota a la NoteSequence "ns" y al diccionario de claves "keys" con el indice "k"
    def append_note(self, keys, k, ns, n_pitch, n_start_time, n_end_time, n_velocity):
        note = NoteSequence.Note(pitch=n_pitch, velocity=n_velocity)

        if (self.step_mode):
            note.quantized_start_step = n_start_time
            note.quantized_end_step = n_end_time

        else:
            note.start_time = n_start_time
            note.end_time = n_end_time

        ns.notes.append(note)

        serializedNote = self.serialize_note(note)
        
        n = keys.get(serializedNote, k)
                
        #si la key no estaba en el diccionario, n será igual que la k actual
        if n == k:
            #añadimos la key al diccionario con el indice actual
            keys[serializedNote] = k
            #avanzamos k
            k += 1
        
        return k

    #Serializa una nota en formato "pitch_duracion" y devuelve la string serializada
    def serialize_note(self, note):
        ser_note = ""

        if (self.step_mode):
            ser_note = str(note.pitch) + "_" +  str(note.quantized_end_step - note.quantized_start_step)
        else:
            ser_note = str(note.pitch) + "_" +  str(round(note.end_time - note.start_time, 2))

        return ser_note

    #Deserializa una secuencia de notas en formato "pitch_duracion" y devuelve el NoteSequence correspondiente
    def deserialize_noteseq(self, note_list):
        start_time = 0

        ns = NoteSequence()
        for ser_note in note_list:
            #deserializacion del pitch y duracion
            data = ser_note.split('_')
            pitch = int(data[0])
            duration = float(data[1])

            #cap de maxima duracion de silencios
            if  (pitch == 0):
                if (self.step_mode):
                    duration = min(duration, MAX_SILENCE_STEPS)
                else:
                    duration = min(duration, MAX_SILENCE_SECONDS)
            
            #a partir de la duracion obtenemos el end_time
            end_time = start_time + duration

            if (pitch != 0):
                #añadimos la nota al NoteSequence
                note = NoteSequence.Note(pitch=pitch, velocity=100)
                
                if (self.step_mode):
                    note.quantized_start_step = int(start_time)
                    note.quantized_end_step = int(end_time)

                    note.start_time = (start_time * STEP_VALUE) * (60.0 / QPM)
                    note.end_time = (end_time * STEP_VALUE) * (60.0 / QPM)
                else:
                    note.start_time = start_time
                    note.end_time = end_time

                ns.notes.append(note)
            
            #el start_time de la siguiente nota es el end_time de la anterior
            start_time = end_time

        return ns

    #Crea y entrena una cadena de Markov y la devuelve al final
    def train_markov_chain(self, path = "https://storage.googleapis.com/magentadata/datasets/bach-doodle/bach-doodle.jsonl-00001-of-00192.gz"):
        #path_or_buf="datasets/bach-doodle.jsonl-00001-of-00192.gz"
        #lee el json line desde la url y lo convierte en dataframe de pandas
        df = pd.read_json(path, lines=True)

        notes_to_train = []
        keys = {}

        #indice de la nota en keys
        k = 0
        inputs = df["input_sequence"]
            
        for i in range(len(inputs)):
            for j in range(len(inputs[i])):
                #solo nos interesan las notas si el feedback es positivo ("2")
                if (df["feedback"][i][j] == "2"):
                    noteSeq = inputs[i][j]
                    
                    # Create a NoteSequence
                    ns = NoteSequence()
                    prev_end_time = 0
                    noteList = noteSeq["notes"]
                        
                    keySig = self.getScale(noteSeq)
                    pitchVariation = name_pitch[keySig]

                    useNoteSeq = True
                        
                    for note_data in noteList:

                        start_time = 0
                        end_time = 0

                        if (self.step_mode):
                            start_time = int(note_data.get("quantizedStartStep", 0))
                            end_time = int(note_data.get("quantizedEndStep"))
                        else:
                            start_time = note_data.get("startTime", 0)
                            end_time = note_data.get("endTime")

                        #contamos la diferencia de tiempo entre la nota actual y la anterior, para ver si hay silencios
                        time_diff = start_time - prev_end_time
                        if (self.has_silences and time_diff > 0.05):
                            k = self.append_note(keys, k, ns, 0, prev_end_time, start_time, 100)

                        notePitch = note_data["pitch"]

                        #si queremos normalizar la escala 
                        if (self.normalize_scale):
                            notePitch -= pitchVariation
                            #si la nota no pertenece a la escala la descartamos
                            if (not is_CMajor_note[notePitch % 12]):
                                useNoteSeq = False
                                break

                            notePitch = max(notePitch, notePitch % 12 + 12*4)
                            notePitch = min(notePitch, notePitch % 12 + 12*5)

                        
                        k = self.append_note(keys, k, ns, notePitch, start_time, end_time, note_data["velocity"])
                        prev_end_time = end_time

                    #anadimos la secuencia al training data
                    if (useNoteSeq):
                        notes_to_train.append(ns)
                    
        differentNotes = len(keys.keys())
        ocurrences = np.zeros(shape=(differentNotes, differentNotes))

        with open("b", "w") as archivo:
            for key in keys.keys():
                data = key.split('_')

                noteName = ""
                for name, pitch in reversed(name_pitch.items()):
                    if pitch == int(data[0]) % 12:
                        noteName = name
                        break

                archivo.write(str(noteName) + "_" + str(int(int(data[0])/12)) + "_" + str(data[1]) + "\n")

        for noteSeq in notes_to_train:
            ant = -1
            for note in noteSeq.notes:
                # if (note.pitch == 0):
                #     print(note)
                #     print("------------------------------------------------")

                serializedNote = self.serialize_note(note)
                n = keys.get(serializedNote, -1)

                if n != -1 and ant != -1:
                    ocurrences[ant][n] += 1
                
                ant = n

        ocurrences_smoothed = ocurrences + 1

        if (self.smooth_ocurrences):
            sum = ocurrences_smoothed.sum(axis=1, keepdims=True)
            p = np.true_divide(ocurrences_smoothed, sum)

        else:
            # Calcula el sumatorio por fila
            sum_row = ocurrences.sum(axis=1, keepdims=True)

            # Encuentra las filas cuyo sumatorio es igual a cero
            zero_sum_rows = np.where(sum_row == 0)[0]

            # Elimina las filas y columnas correspondientes
            ocurrences = np.delete(ocurrences, zero_sum_rows, axis=0)
            ocurrences = np.delete(ocurrences, zero_sum_rows, axis=1)

            # Elimina las claves correspondientes a las filas y columnas borradas
            keys = [key for idx, key in enumerate(keys) if idx not in zero_sum_rows]

            # Calcula el nuevo sumatorio por fila después de la eliminación
            sum_row = ocurrences.sum(axis=1, keepdims=True)

            print(ocurrences.shape)

            p = np.true_divide(ocurrences, sum_row)

        self.mc = MarkovChain(p, list(keys))

        print("[MarkovGenerator]: Markov Chain created and trained succesfully")

    def run_markov_chain(self, chain = None, num_simulations = 10, num_notes = 44):
        if chain is None:
            chain = self.mc
            if chain is None:
                print("[MarkovGenerator][Error]: chain was None in run_markov_chain()")
                return False
        
        if not os.path.isdir("./outputs"):
            os.mkdir("outputs")

        simulations = []
        note_seq_sims = []
        outputs = []
        for i in range(num_simulations):
            curr_sim = chain.simulate(num_notes)
            simulations.append(curr_sim)
            note_seq_sims.append(self.deserialize_noteseq(curr_sim))

            #guarda el output en la lista para devolverlo al final
            output = "./outputs/markov_sim_" + str(i) + ".mid"
            outputs.append(output)
            midi_io.sequence_proto_to_midi_file(note_seq_sims[i], output)

        print("[MarkovGenerator]: Melodies generated and placed in 'outputs' folder")
        return outputs
    
    def load_markov_chain_from_json(self, path):
        silence_string = "_silences"

        if not self.has_silences:
            silence_string = "_no_silences"

        path += silence_string + ".json"

        try:
            self.mc = MarkovChain.from_file(path)
        except Exception as ex:
            raise Exception(ex)
        
        print("[MarkovGenerator]: Markov Chain loaded successfully from file")
        

    def save_markov_chain_to_json(self, path, filename):
        silence_string = "_silences"

        if not self.has_silences:
            silence_string = "_no_silences"
        
        filename += silence_string
        
        dir_path = Path(path)
        file_path = Path(path + filename + ".json")

        #si no existe el directorio de salida lo crea
        if not os.path.isdir(dir_path):
            os.mkdir(dir_path)
            
        #si no existe el archivo de salida lo crea
        if not os.path.isfile(file_path):
            with open(os.path.join(path, filename + ".json"), 'w') as fp: 
                pass
            
        try:
            self.mc.to_file(file_path)
        except Exception as ex:
            raise Exception(ex)

        print("[MarkovGenerator]: Markov Chain saved successfully into a file")

# import json

# data = []
# with open('datasets/tmpcFDwkB') as f:
#     for line in f:
#         data.append(json.loads(line))

# for i in range(len(data)):
#     #
#     for j in range(len(data[i]["input_sequence"])):
#         #solo nos interesan las notas si el feedback es positivo ("2")
#         if (data[i]["feedback"][j] == "2"):
#             notes = data[i]["input_sequence"][j]
#             print(notes["notes"])
#             print("----------------------------------------------------------")