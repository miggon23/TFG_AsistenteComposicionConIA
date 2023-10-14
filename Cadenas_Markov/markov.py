from IPython.display import display
import pandas as pd
import numpy as np
from note_seq import NoteSequence, midi_io

from pydtmc import MarkovChain

def append_note(keys, k, ns, n_pitch, n_start_time, n_end_time, n_velocity):
    note = NoteSequence.Note(pitch=n_pitch, start_time=n_start_time, end_time=n_end_time, velocity=n_velocity)
    ns.notes.append(note)

    serializedNote = str(note.pitch) + "_" +  str(round(note.end_time - note.start_time, 2))
    n = keys.get(serializedNote, k)
            
    #si la key no estaba en el diccionario, n será igual que la k actual
    if n == k:
        #añadimos la key al diccionario con el indice actual
        keys[serializedNote] = k
        #avanzamos k
        k += 1
    
    return k

#Deserializa una secuencia de notas en formato "pitch_duracion" y devuelve el NoteSequence correspondiente
def deserialize_noteseq(note_list):
    start_time = 0

    ns = NoteSequence()
    for ser_note in note_list:
        #deserializacion del pitch y duracion
        data = ser_note.split('_')
        pitch = int(data[0])
        duration = float(data[1])
        
        #a partir de la duracion obtenemos el end_time
        end_time = start_time + duration

        if (pitch != 0):
            #añadimos la nota al NoteSequence
            note = NoteSequence.Note(pitch=pitch, start_time=start_time, end_time=end_time, velocity=100)
            ns.notes.append(note)
        
        #el start_time de la siguiente nota es el end_time de la anterior
        start_time = end_time

    return ns


#lee el json line desde la url y lo convierte en dataframe de pandas
df = pd.read_json(path_or_buf="datasets/bach-doodle.jsonl-00001-of-00192.gz", lines=True)

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
                #contamos la diferencia de tiempo entre la nota actual y la anterior, para ver si hay silencios
                time_diff = note_data.get("startTime", 0) - prev_end_time
                if (time_diff > 0.05):
                    k = append_note(keys, k, ns, 0, prev_end_time, note_data["startTime"], 100)

                k = append_note(keys, k, ns, note_data["pitch"], note_data.get("startTime", 0), note_data["endTime"], note_data["velocity"])
                prev_end_time = note_data["endTime"]

            #anadimos la secuencia al training data
            notes_to_train.append(ns)
            
differentNotes = len(keys.keys())
ocurrences = np.zeros(shape=(differentNotes, differentNotes))

for noteSeq in notes_to_train:
    ant = -1
    for note in noteSeq.notes:
        # if (note.pitch == 0):
        #     print(noteSeq.notes)

        serializedNote = str(note.pitch) + "_" +  str(round(note.end_time - note.start_time, 2))
        n = keys.get(serializedNote, -1)

        if n != -1 and ant != -1:
            ocurrences[ant][n] += 1
        
        ant = n

ocurrences_smoothed = ocurrences + 1

p = np.true_divide(ocurrences_smoothed, ocurrences_smoothed.sum(axis=1, keepdims=True))

mc = MarkovChain(p, list(keys))

simulations = []
note_seq_sims = []
num_simulations = 10
num_notes = 10
for i in range(num_simulations):
    curr_sim = mc.simulate(num_notes)
    simulations.append(curr_sim)
    note_seq_sims.append(deserialize_noteseq(curr_sim))
    midi_io.sequence_proto_to_midi_file(note_seq_sims[i], "outputs/markov_sim_" + str(i) + ".mid")


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