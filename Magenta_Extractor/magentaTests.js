const { core, midi, sequenceProtoToMidi, midiToSequenceProto } = require('@magenta/music/node/core');
const mm = require('@magenta/music/node/music_rnn');
const fs = require('fs');

// Initialize the model.
music_rnn = new mm.MusicRNN('https://storage.googleapis.com/magentadata/js/checkpoints/music_rnn/basic_rnn');
music_rnn.initialize();

rnn_steps = 20;
rnn_temperature = 1.5;

function generate() {

    INI_MEL = {
        notes: [
            { pitch: 60, quantizedStartStep: 0, quantizedEndStep: 1 }
        ],
        quantizationInfo: { stepsPerQuarter: 4 },
        tempos: [{ time: 0, qpm: 120 }],
        totalQuantizedSteps: 1
    };

    music_rnn
        .continueSequence(INI_MEL, rnn_steps, rnn_temperature)
        .then(samples => {

            //Conversión a MIDI
            const midiFile = sequenceProtoToMidi(samples);
            const midiBuffer = Buffer.from(midiFile);;
            const midiFileName = 'midi\\magenta_melody.mid';

            fs.writeFile(midiFileName, midiBuffer, 'binary', err => {
                if (err) {
                    console.error('Error al guardar el archivo MIDI:', err);
                } else {
                    console.log(`Archivo MIDI guardado como ${midiFileName}`);
                }
            });
        });
}

generate()