import pandas as pd
import numpy as np

from sklearn.model_selection import train_test_split
from sklearn.preprocessing import LabelEncoder
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
    encoder = LabelEncoder()
    X = df['curr_note']
    y = df['next_note']

    label_encoder = LabelEncoder()
    label_encoder.fit(keys)
    X_encoded = label_encoder.transform(X)
    y_encoded = label_encoder.transform(y)

    # Convertir las notas codificadas a one-hot encoding
    X_onehot = to_categorical(X_encoded)
    y_onehot = to_categorical(y_encoded)

    # Split the data into training and test sets
    x_train, x_val, y_train, y_val = train_test_split(X_onehot, y_onehot, test_size=0.2)

    early_stopping = EarlyStopping(
        monitor='val_loss',  # Métrica a monitorear (puede ser 'val_accuracy', 'val_loss', etc.)
        patience=10,          # Número de épocas sin mejora antes de detener el entrenamiento
        restore_best_weights=True  # Restaura los pesos del modelo al mejor logrado durante el entrenamiento
    )

    model = keras.Sequential()

    model.add(layers.Dense(64, activation='relu', input_shape=(n_out,)))

    # Agrega una capa de Reshape para agregar la dimensión de los pasos de tiempo
    model.add(layers.Reshape((1, 64)))

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
        batch_size=32,
        epochs=5000,
        validation_data=(x_val, y_val),
        callbacks=[early_stopping]
    )

    # Guardar el modelo en formato keras
    model.save('rnn_entrenado.keras')

if __name__ == '__main__':
    train_rnn()