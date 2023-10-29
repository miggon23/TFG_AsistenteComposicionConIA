from IPython.display import display
import pandas as pd
import numpy as np
from note_seq import NoteSequence, midi_io

from pydtmc import MarkovChain
from pydtmc import plot_graph
import os
from pathlib import Path

#QPM estandar para pasar a MIDI (1 negra por segundo)
QPM = 60

#Valor estandar de un step, para normalizar
STEP_VALUE = 1/4

MAX_SILENCE_STEPS = 8
MAX_SILENCE_SECONDS = 2

class Markov_Generator:

    def __init__(self, use_steps = True, use_silences = True):
        self.step_mode = use_steps
        self.has_silences = use_silences

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
            #
            for j in range(len(inputs[i])):
                #solo nos interesan las notas si el feedback es positivo ("2")
                if (df["feedback"][i][j] == "2"):
                    notes = inputs[i][j]
                    
                    # Create a NoteSequence
                    ns = NoteSequence()
                    prev_end_time = 0
                    for note_data in notes["notes"]:

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

                        k = self.append_note(keys, k, ns, note_data["pitch"], start_time, end_time, note_data["velocity"])
                        prev_end_time = end_time

                    #anadimos la secuencia al training data
                    notes_to_train.append(ns)
                    
        differentNotes = len(keys.keys())
        ocurrences = np.zeros(shape=(differentNotes, differentNotes))

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

        p = np.true_divide(ocurrences_smoothed, ocurrences_smoothed.sum(axis=1, keepdims=True))

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
        for i in range(num_simulations):
            curr_sim = chain.simulate(num_notes)
            simulations.append(curr_sim)
            note_seq_sims.append(self.deserialize_noteseq(curr_sim))
            midi_io.sequence_proto_to_midi_file(note_seq_sims[i], "./outputs/markov_sim_" + str(i) + ".mid")

        print("[MarkovGenerator]: Melodies generated and placed in 'outputs' folder")
    
    def load_markov_chain_from_json(self, path):
        try:
            self.mc = MarkovChain.from_file(path)
        except Exception as ex:
            raise Exception(ex)
        
        print("[MarkovGenerator]: Markov Chain loaded successfully from file")
        

    def save_markov_chain_to_json(self, path, filename):
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

    def print_chain(self):
        return plot_graph(self.mc, dpi=300)

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