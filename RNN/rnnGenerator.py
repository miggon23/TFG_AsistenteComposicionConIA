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
    df = df.drop('start', axis=1)
    df = df.drop('end', axis=1)

    # #separamos los datos entre input y output
    # X = df['curr_note']
    # y = df['next_note']

    # Aplicar one-hot encoding a las columnas 'curr_note' y 'next_note'
    X = df.drop(['next_note', 'curr_note'], axis=1)
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
    # X_encoded = label_encoder.transform(X)
    y_encoded = label_encoder.transform(y)

    # Convertir las notas codificadas a one-hot encoding
    # X_onehot = to_categorical(X_encoded)
    y_onehot = to_categorical(y_encoded)

    # Generamos secuencias de notas
    seq_length = 5  # Ajusta según la longitud de la secuencia que desees
    input_data, output_data = generate_sequences(X, y_onehot, seq_length)

    # Split the data into training and test sets
    x_train, x_val, y_train, y_val = train_test_split(input_data, output_data, test_size=0.2)

    early_stopping = EarlyStopping(
        monitor='val_loss',  # Métrica a monitorear (puede ser 'val_accuracy', 'val_loss', etc.)
        patience=10,          # Número de épocas sin mejora antes de detener el entrenamiento
        restore_best_weights=True  # Restaura los pesos del modelo al mejor logrado durante el entrenamiento
    )

    model = keras.Sequential()

    # Capa de entrada
    model.add(layers.Input(shape=(seq_length, 2)))

    # Capa LSTM
    model.add(layers.LSTM(64))

    # Capa de salida
    model.add(layers.Dense(n_out, activation='softmax'))

    model.summary()

    model.compile(
        loss='categorical_crossentropy',
        optimizer="adam",
        metrics=["accuracy"],
    )

    history = model.fit(
        x_train,
        y_train,
        batch_size=256,
        epochs=5000,
        validation_data=(x_val, y_val),
        callbacks=[early_stopping]
    )

    # Guardar el modelo en formato keras
    model.save('rnn_entrenado.keras')

def load_model():    
    return keras.models.load_model('rnn_entrenado.keras')

def predict_next_note(notes: np.ndarray, model: tf.keras.Model, temperature: float = 1.0) -> tuple[int, float, float]:
    """Generates a note as a tuple of (pitch, step, duration), using a trained sequence model."""

    assert temperature > 0

    # Add batch dimension
    inputs = tf.expand_dims(notes, 0)

    predictions = model.predict(inputs)

    # Aplicamos el muestreo estocástico con la temperatura dada
    predictions = np.log(predictions) / temperature
    exp_predictions = np.exp(predictions)
    predicted_probs = exp_predictions / np.sum(exp_predictions, axis=1, keepdims=True)

    # Muestreamos la próxima nota según las probabilidades predichas
    predicted_index = np.random.choice(range(len(predictions[0])), p=predicted_probs[0])

    return predicted_index, predicted_probs[0][predicted_index], predictions[0][predicted_index]

if __name__ == '__main__':
    # train_rnn()
    # exit()

    path = "Datasets/Cleaned/"

    keys = []
    #keys
    with open(path + "keys.txt", 'r') as file:
        # Lee el contenido del archivo y divide la cadena en una lista utilizando el espacio como separador
        keys = file.read().split()

    with open(path + "scaler_params.json", 'r') as file:
        scaler_params = json.load(file)

    model = load_model()

    num_bar = 32

    simulations = []
    note_seq_sims = []
    outputs = []
    for i in range(10):
        #realiza tantos pasos como sean necesarios para llegar al numero de compases pedidos
        curr_sim = [ "60_2", "60_2", "60_2", "60_2", "60_2" ]
        curr_sim_int = [tuple(map(float, sim.split('_'))) for sim in curr_sim]
        curr_sim_array = np.array(curr_sim_int)

        curr_sim_array[: , 0] = (curr_sim_array[: , 0] - scaler_params['mean'][0]) / scaler_params['std'][0]
        curr_sim_array[: , 1] = (curr_sim_array[: , 1] - scaler_params['mean'][1]) / scaler_params['std'][1]

        print(curr_sim_array)
        
        curr_duration = curr_sim_array.sum(axis=1)[1]
        
        j = 1
        while curr_duration < num_bar * 4:
            #predict de la nota
            next_note_index, _, _ = predict_next_note(curr_sim_array[-5:,:], model)
            # next_note_index = 10
            next_note = keys[next_note_index]
            print(next_note)

            #decodificamos la nota y la escalamos
            next_note_array = np.array([((float(next_note.split('_')[0]) - scaler_params['mean'][0]) / scaler_params['std'][0]), 
                                        ((float(next_note.split('_')[1]) - scaler_params['mean'][1]) / scaler_params['std'][1])])
            #añadimos la nota
            curr_sim_array = np.vstack([curr_sim_array, next_note_array])
            
            #actualizamos duraciones
            curr_duration += int((next_note.split('_'))[1])
            if curr_duration <= num_bar * 4:
                curr_sim.append(next_note)
            j += 1

        simulations.append(curr_sim)
        note_seq_sims.append(nc.deserialize_noteseq(curr_sim))

        #guarda el output en la lista para devolverlo al final
        output = "./midi/markov_melody_" + str(i) + ".mid"
        outputs.append(output)
        nc.save_to_midi(note_seq_sims[i], output)