import json
import pandas as pd
import numpy as np

from sklearn.model_selection import train_test_split
from sklearn.preprocessing import LabelEncoder
from sklearn.preprocessing import StandardScaler
from sklearn.preprocessing import OneHotEncoder
import tensorflow as tf
from tensorflow import keras
from keras.utils import to_categorical
from keras import layers
from keras import regularizers
from keras.callbacks import EarlyStopping
from sklearn.metrics import accuracy_score
from sklearn.metrics import precision_score
from sklearn.metrics import recall_score
from sklearn.metrics import confusion_matrix

import sys
sys.path.append('./NoteSeqUtils/')

import noteseqConverter as nc

def generate_sequences(X, y, seq_length):
    input_sequences = []
    output_sequences = []

    for i in range(len(X) - seq_length):
        seq_in = X[i:i + seq_length, :]
        seq_out = y[i + seq_length, :]
        input_sequences.append(seq_in)
        output_sequences.append(seq_out)

    return np.array(input_sequences), np.array(output_sequences)

@keras.saving.register_keras_serializable()
def mse_with_positive_pressure(y_true: tf.Tensor, y_pred: tf.Tensor):
    mse = (y_true - y_pred) ** 2
    positive_pressure = 10 * tf.maximum(-y_pred, 0.0)
    return tf.reduce_mean(mse + positive_pressure)

def train_rnn():
    path = "Datasets/Cleaned/"

    #carga del dataset
    df = pd.read_csv(path + "dataset_rnn_labeled.csv")

    keys = []
    #keys
    with open(path + "keys.txt", 'r') as file:
        # Lee el contenido del archivo y divide la cadena en una lista utilizando el espacio como separador
        keys = file.read().split()

    n_out = len(keys)

    #quitamos el start y el end, para no ensuciar la generacion
    # df = df.drop('start', axis=1)
    df = df.drop('end', axis=1)

    # #separamos los datos entre input y output
    X = df.drop(['next_note', 'next_note_start', 'next_note_pitch', 'next_note_duration'], axis=1)
    y = df['next_note']

    scaling = StandardScaler()
    scaling.fit(X)
    X = scaling.transform(X)
    
    params = {
    'mean': scaling.mean_.tolist(),
    'std': scaling.scale_.tolist()
    }

    with open('Datasets/Cleaned/scaler_params.json', 'w') as file:
        json.dump(params, file)
    
    # X = X.values

    label_encoder = LabelEncoder()
    label_encoder.fit(keys)
    y_encoded = label_encoder.transform(y)

    # Convertir las notas codificadas a one-hot encoding
    y_onehot = to_categorical(y_encoded)
    next_note_start  = df[['next_note_start']].to_numpy()

    y_combined = np.concatenate((y_onehot, next_note_start), axis=1)

    # Generamos secuencias de notas
    seq_length = 5  # Ajusta según la longitud de la secuencia que desees
    input_data, output_data = generate_sequences(X, y_combined, seq_length)

    # Split the data into training and test sets
    # x_train, x_val, y_train, y_val = train_test_split(input_data, output_data, test_size=0.2)
    input_split = int(input_data.shape[0] * 0.8)
    output_split = int(output_data.shape[0] * 0.8)
    x_train = input_data[:input_split,:]
    x_val = input_data[input_split:,:]
    y_train = output_data[:output_split,:]
    y_val = output_data[output_split:,:]

    early_stopping = EarlyStopping(
        monitor='val_loss',  # Métrica a monitorear (puede ser 'val_accuracy', 'val_loss', etc.)
        patience=10,          # Número de épocas sin mejora antes de detener el entrenamiento
        restore_best_weights=True  # Restaura los pesos del modelo al mejor logrado durante el entrenamiento
    )

    # Capa de entrada
    inputs = tf.keras.Input(shape=(seq_length, 3))

    # Capa LSTM
    x = tf.keras.layers.LSTM(128)(inputs)

    # Capa de salida
    outputs = {
        'next_note': tf.keras.layers.Dense(n_out, activation='softmax', name='next_note')(x),
        'next_note_start': tf.keras.layers.Dense(1, name='next_note_start')(x),
    }

    model = tf.keras.Model(inputs, outputs)
    model.summary()

    loss = {
      'next_note': 'categorical_crossentropy',
      'next_note_start': mse_with_positive_pressure,
    }

    model.compile(
        loss=loss,
        loss_weights={
        'next_note_start': 0.05,
        'step': 1.0,
        },
        optimizer="adam",
        metrics=["accuracy"],
    )

    # history = model.fit(
    #     x_train,
    #     y_train,
    #     batch_size=256,
    #     epochs=5000,
    #     validation_data=(x_val, y_val),
    #     callbacks=[early_stopping]
    # )

    history = model.fit(
        x_train,
        {"next_note": y_train[:, :n_out], "next_note_start": y_train[:, n_out:]},
        batch_size=256,
        epochs=5000,
        validation_data=(x_val, {"next_note": y_val[:, :n_out], "next_note_start": y_val[:, n_out:]}),
        callbacks=[early_stopping]
    )

    # Guardar el modelo en formato keras
    model.save('rnn_entrenado.keras')

def load_model():    
    return keras.models.load_model('rnn_entrenado.keras')

def predict_next_note(notes: np.ndarray, model: tf.keras.Model, temperature: float = 1.0) -> tuple[int, float]:
    """Generates the index of the next note and its predicted start time, using a trained sequence model."""

    assert temperature > 0

    # Add batch dimension
    inputs = tf.expand_dims(notes, 0)

    predictions = model.predict(inputs)

    # Obtenemos las predicciones para la próxima nota y el tiempo de inicio
    next_note_probs = predictions['next_note'][0]
    next_note_start = predictions['next_note_start'][0][0]

    # Aplicamos el muestreo estocástico a las probabilidades de la próxima nota con la temperatura dada
    next_note_index = np.random.choice(range(len(next_note_probs)), p=next_note_probs)

    return next_note_index, next_note_start

def generate(n_steps = 64, temperature = 1):
    path = "Datasets/Cleaned/"

    keys = []
    # Leer las claves (keys)
    with open(path + "keys.txt", 'r') as file:
        # Dividir la cadena del archivo en una lista utilizando el espacio como separador
        keys = file.read().split()

    with open(path + "scaler_params.json", 'r') as file:
        scaler_params = json.load(file)

    model = load_model()

    num_bar = 8

    simulations = []
    note_seq_sims = []
    outputs = []
    
    # Generar una secuencia inicial de notas con tiempos de inicio
    curr_sim = [("60", 2, 0), ("60", 2, 2), ("60", 2, 4), ("60", 2, 6), ("60", 2, 8)]
    
    # Convertir la secuencia de notas en un array numpy
    curr_sim_array = np.array(curr_sim, dtype=float)
    
    # Normalizar los datos
    curr_sim_array[:, 0] = (curr_sim_array[:, 0] - scaler_params['mean'][0]) / scaler_params['std'][0]
    curr_sim_array[:, 1] = (curr_sim_array[:, 1] - scaler_params['mean'][1]) / scaler_params['std'][1]
    curr_sim_array[:, 2] = (curr_sim_array[:, 2] - scaler_params['mean'][2]) / scaler_params['std'][2]

    curr_duration = 0

    while curr_duration < n_steps:
        # Predecir la próxima nota y su tiempo de inicio
        next_note_index, next_note_start = predict_next_note(curr_sim_array[-5:,:], model, temperature)
        next_note = keys[next_note_index]
        next_note_pitch = int(next_note.split('_')[0])
        next_note_dur = int(next_note.split('_')[1])

        # Decodificar y escalar la nota
        next_pitch = (int(next_note.split('_')[0]) - scaler_params['mean'][0]) / scaler_params['std'][0]
        next_duration = (int(next_note.split('_')[1]) - scaler_params['mean'][1]) / scaler_params['std'][1]
        next_start = (next_note_start - scaler_params['mean'][2]) / scaler_params['std'][2]

        # Añadir la próxima nota a la secuencia
        curr_sim_array = np.vstack([curr_sim_array, [next_pitch, next_duration, next_start]])

        # Actualizar la duración acumulada
        curr_duration += int(next_note.split('_')[1])

        if (curr_duration > n_steps):
            last_note_dur = next_note_dur - (curr_duration - n_steps)
            next_note = str(next_note_pitch) + "_" + str(last_note_dur)

        # Añadir la próxima nota a la lista de simulaciones
        curr_sim.append(next_note)

    simulations.append(curr_sim[5:])
    note_seq_sims.append(nc.deserialize_noteseq(curr_sim[5:]))

    # Guardar la secuencia en un archivo MIDI
    output = f"./Media/midi/output_song.mid"
    outputs.append(output)
    nc.save_to_midi(note_seq_sims[0], output)

    return outputs

if __name__ == '__main__':
    # train_rnn()
    # exit()

    generate()