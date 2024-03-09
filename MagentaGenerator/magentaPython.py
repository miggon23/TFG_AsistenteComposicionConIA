import subprocess
import json
import os

import sys
sys.path.append('./NoteSeqUtils/')

import noteseqConverter as nc

def generate_melodies(n_melodies, n_steps = 28):

    outputs = []

    process = subprocess.Popen(['node', os.getcwd() + '\MagentaGenerator\magentaGenerator.js', str(n_melodies), str(n_steps)], stdout=subprocess.PIPE)
        
    # Lee toda la salida del proceso a la vez
    output, _ = process.communicate()
    
    # Dividir la salida en objetos JSON individuales
    melodies = output.decode('utf-8').split('\n')

    # Decodifica cada objeto JSON individualmente y realiza el procesamiento necesario
    i = 0
    for melody_data in melodies:
        if melody_data.strip():  # Ignorar líneas en blanco
            melody = json.loads(melody_data)
            out = "./midi/magenta_melody_" + str(i) + ".mid"
            nc.save_to_midi(nc.json_to_noteSeq(melody), out)
            outputs.append(out)
            i += 1
            print(f"Saved midi to {out}")

    return outputs

# generate_melodies(10)