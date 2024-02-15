import pandas as pd    
import numpy as np
import collections
import os
import json

from sklearn.preprocessing import StandardScaler

#QPM estandar para pasar a MIDI (1 negra por segundo)
QPM = 60

#Valor estandar de un step, para normalizar
STEP_VALUE = 1/4

MAX_SILENCE_STEPS = 8
MAX_SILENCE_SECONDS = 2

has_silences = False

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

def get_scale(noteSeq):
    keySignatures = noteSeq.get("keySignatures", 0)
    
    if (keySignatures != 0):
        return keySignatures[0].get("key", "C")

    return "C"

def clean_dataset(path = "https://storage.googleapis.com/magentadata/datasets/bach-doodle/bach-doodle.jsonl-00001-of-00192.gz"):
    #path_or_buf="datasets/bach-doodle.jsonl-00001-of-00192.gz"
    #lee el json line desde la url y lo convierte en dataframe de pandas
    notes = collections.defaultdict(list)

    for m in range(2):

        path = "https://storage.googleapis.com/magentadata/datasets/bach-doodle/bach-doodle.jsonl-0000" + str(m) + "-of-00192.gz"
        df = pd.read_json(path, lines=True)

        keys = {}

        #indice de la nota en keys
        k = 0
        inputs = df["input_sequence"]
                    
        for i in range(len(inputs)):
            for j in range(len(inputs[i])):
                #solo nos interesan las notas si el feedback es positivo ("2")
                if (df["feedback"][i][j] == "2"):
                    noteSeq = inputs[i][j]
                    
                    prev_end_time = 0
                    noteList = noteSeq["notes"]
                        
                    keySig = get_scale(noteSeq)
                    # if (keySig != "C"):
                    #     break

                    pitchVariation = name_pitch[keySig]

                    curr_note = collections.defaultdict(list)
                        
                    useNoteSeq = True

                    for q in range(len(noteList)):

                        note_data = noteList[q]
                        if (q < len(noteList)-1):
                            next_note = noteList[q+1]

                            nextNotePitch = next_note["pitch"]
                            nextNotePitch -= pitchVariation
                            nextNotePitch = max(nextNotePitch, nextNotePitch % 12 + 12*4)
                            nextNotePitch = min(nextNotePitch, nextNotePitch % 12 + 12*5)
                            next_start_time = int(next_note.get("quantizedStartStep", 0))
                            next_end_time = int(next_note.get("quantizedEndStep"))

                        start_time = 0
                        end_time = 0

                        start_time = int(note_data.get("quantizedStartStep", 0))
                        end_time = int(note_data.get("quantizedEndStep"))

                        notePitch = note_data["pitch"]

                        # Normalizacion de escala
                        notePitch -= pitchVariation
                        #si la nota no pertenece a la escala la descartamos
                        if (not is_CMajor_note[notePitch % 12]):
                            useNoteSeq = False
                            break

                        notePitch = max(notePitch, notePitch % 12 + 12*4)
                        notePitch = min(notePitch, notePitch % 12 + 12*5)

                        noteDuration = end_time - start_time

                        #contamos la diferencia de tiempo entre la nota actual y la anterior, para ver si hay silencios
                        time_diff = start_time - prev_end_time
                        if (has_silences and time_diff > 0.05):

                            prev_end_time, start_time

                            noteDuration = start_time - prev_end_time

                            curr_note['pitch'].append(0)
                            curr_note['start'].append(prev_end_time)
                            curr_note['end'].append(start_time)
                            curr_note['duration'].append(noteDuration)
                            curr_note['next_note'].append(str(notePitch) + "_" + str(noteDuration))
                            
                            serializedNote = str(0) + "_" + str(noteDuration)
        
                            n = keys.get(serializedNote, k)
                                    
                            #si la key no estaba en el diccionario, n será igual que la k actual
                            if n == k:
                                #añadimos la key al diccionario con el indice actual
                                keys[serializedNote] = k
                                #avanzamos k
                                k += 1

                        if (q < len(noteList)-1):
                            curr_note['pitch'].append(notePitch)
                            curr_note['start'].append(start_time)
                            curr_note['end'].append(end_time)
                            curr_note['duration'].append(noteDuration)
                            next_note_serialized = str(nextNotePitch) + "_" + str(next_end_time - next_start_time)
                            curr_note['next_note'].append(next_note_serialized)
                        
                        serializedNote = str(notePitch) + "_" + str(noteDuration)
        
                        n = keys.get(serializedNote, k)
                                
                        #si la key no estaba en el diccionario, n será igual que la k actual
                        if n == k:
                            #añadimos la key al diccionario con el indice actual
                            keys[serializedNote] = k
                            #avanzamos k
                            k += 1

                        prev_end_time = end_time
                    
                    #anadimos la secuencia al training data
                    if (useNoteSeq):
                        notes['pitch'].extend(curr_note['pitch'])
                        notes['start'].extend(curr_note['start'])
                        notes['end'].extend(curr_note['end'])
                        notes['duration'].extend(curr_note['duration'])
                        notes['next_note'].extend(curr_note['next_note'])
                    
        print("Dataset " + str(m) + " cleaned")

    cleaned_dataset = pd.DataFrame({name: np.array(value) for name, value in notes.items()})

    os.makedirs('Datasets/Cleaned', exist_ok=True)  

    with open('Datasets/Cleaned/keys.txt', 'w') as fp:
        for item in keys.keys():
            fp.write("%s " % item)
    
    cleaned_dataset.to_csv("Datasets/Cleaned/dataset.csv", index=False)

def normalize_for_rnn():
    path = "Datasets/Cleaned/"

    #carga del dataset
    df = pd.read_csv(path + "dataset.csv")

    # Divide la columna 'next_note' en dos columnas: 'next_note_pitch' y 'next_note_duration'
    df[['next_note_pitch', 'next_note_duration']] = df['next_note'].str.split('_', expand=True)

    # Convierte las columnas a tipos de datos apropiados si es necesario
    df['next_note_pitch'] = df['next_note_pitch'].astype(int)
    df['next_note_duration'] = df['next_note_duration'].astype(int)

    # Elimina la columna original 'next_note' si ya no la necesitas
    df = df.drop('next_note', axis=1)

    scaling = StandardScaler()
    scaling.fit(df)
    df = scaling.transform(df)

    params = {
    'mean': scaling.mean_.tolist(),
    'std': scaling.scale_.tolist()
    }

    with open('Datasets/Cleaned/scaler_params.json', 'w') as file:
        json.dump(params, file)

    df = pd.DataFrame(df)
    df.reset_index()
    df.to_csv("Datasets/Cleaned/dataset_rnn_normalized.csv", index=False, header=["pitch","start","end","duration","next_note_pitch","next_note_duration"])

def transform_to_label_rnn():
    path = "Datasets/Cleaned/"

    #carga del dataset
    df = pd.read_csv(path + "dataset.csv")

    print(df)

    # Combina las columnas 'pitch' y 'duration' en una nueva columna 'curr_note'
    df['curr_note'] = df['pitch'].astype(str) + '_' + df['duration'].astype(str)
    df.to_csv("Datasets/Cleaned/dataset_rnn_labeled.csv", index=False)

if __name__ == '__main__':
    transform_to_label_rnn()