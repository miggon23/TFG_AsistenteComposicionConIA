
const mvae = require('@magenta/music/node/music_vae');
const {core, midi, sequenceProtoToMidi, midiToSequenceProto} = require('@magenta/music/node/core');
const checkpoints = require('./checkpoints.json');
const fs = require('fs');
//const { sequences } = require('@magenta/music/node');

const checkpointID = 'mel_4bar_med_q2'

//Buscamos el modelo preentrenado en nuestra lista de modelos
const checkpointEspecifico = checkpoints.find(checkpoint => checkpoint.id === checkpointID)

//Lo buscamos por URL
const model = new mvae.MusicVAE(checkpointEspecifico.url);
model
  .initialize()
  .then(() => model.sample(1))
  .then(samples => {

    console.log(samples[0]);
    //Conversión a MIDI
    const midiFile = sequenceProtoToMidi(samples[0]);
    const midiBuffer = Buffer.from(midiFile);;
    const midiFileName = `midi\\output_${checkpointID}.mid`;

    fs.writeFile(midiFileName, midiBuffer, 'binary', err => {
        if (err) {
            console.error('Error al guardar el archivo MIDI:', err);
        } else {
            console.log(`Archivo MIDI guardado como ${midiFileName}`);
        }
    });
  });

  //Leer MIDI generado:
  //midiToSequenceProto()
