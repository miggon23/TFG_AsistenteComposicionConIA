// Este script genera una noteSeq con magenta en JS y lo escribe por la salida estandar, esta salida estandar 
// sera recogida por python con subprocess

const mm = require('@magenta/music/node/music_rnn');

// Guardar la referencia de la salida estándar original
const originalStdoutWrite = process.stdout.write;

// Suprimir la salida estándar
// Esto es necesario para evitar el mensaje de inicializacion de magenta en la salida estandar
process.stdout.write = function() {};

// Restaura la función write original después de la inicialización del modelo
music_rnn = new mm.MusicRNN("https://storage.googleapis.com/magentadata/js/checkpoints/music_rnn/basic_rnn");
music_rnn.initialize().then(() => {
    process.stdout.write = originalStdoutWrite;
    // generamos la secuencia de notas
    generate();
});

n_melodies = parseInt(process.argv[2]);
rnn_steps = parseInt(process.argv[3]);
temperature = parseInt(process.argv[4]);

function generate() {

    // melodia inicial para que el modelo la continue, por el momento es un Do y ya
    INI_MEL = {
        notes: [
            { pitch: 60, quantizedStartStep: 0, quantizedEndStep: 1 }
        ],
        quantizationInfo: { stepsPerQuarter: 4 },
        tempos: [{ time: 0, qpm: 120 }],
        totalQuantizedSteps: 1
    };

    music_rnn
        .continueSequence(INI_MEL, rnn_steps, temperature)
        .then(samples => {
            // Convertir NoteSequence a JSON y enviarlo a la salida estándar
            const jsonSequence = JSON.stringify(samples);
            process.stdout.write(jsonSequence + '\n');
        });
}