// Este script genera una noteSeq con magenta en JS y lo escribe por la salida estandar, esta salida estandar 
// sera recogida por python con subprocess

const mm = require('@magenta/music/node/music_rnn');
const core = require('@magenta/music/node/core');
const config = require('./configMusicRNN.json');

// Guardar la referencia de la salida estándar original
const originalStdoutWrite = process.stdout.write;

// Suprimir la salida estándar
// Esto es necesario para evitar el mensaje de inicializacion de magenta en la salida estandar
process.stdout.write = function() {};

music_rnn_spec = config
// Restaura la función write original después de la inicialización del modelo
music_rnn = new mm.MusicRNN("https://storage.googleapis.com/magentadata/js/checkpoints/music_rnn/basic_rnn");
music_rnn.initialize().then(() => {
    process.stdout.write = originalStdoutWrite;
    // generamos la secuencia de notas
    generate();
});

input_melody = JSON.parse(process.argv[2]);
rnn_steps = parseInt(process.argv[3]);
rnn_temperature = parseInt(process.argv[4]);

function generate() {

    const INPUT_MEL = input_melody;

    music_rnn
        .continueSequence(INPUT_MEL, rnn_steps, rnn_temperature)
        .then(samples => {
            // Convertir NoteSequence a JSON y enviarlo a la salida estándar
            const jsonSequence = JSON.stringify(samples);
            process.stdout.write(jsonSequence + '\n');
        });
}