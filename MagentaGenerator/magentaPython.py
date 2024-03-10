import subprocess
import json
import os
import note_seq

import sys
sys.path.append('./NoteSeqUtils/')

import noteseqConverter as nc

def generate_melodies(n_melodies, n_steps = 32):

    outputs = []

    process = subprocess.Popen(['node', os.getcwd() + '\MagentaGenerator\magentaGenerator.js', str(n_melodies), str(n_steps)], stdout=subprocess.PIPE)
        
    # Lee toda la salida del proceso a la vez
    output, _ = process.communicate()
    
    i = 0
    melodies = json.loads(output)

    for melody_json in melodies:
        out = "./midi/base_melody_" + str(i) + ".mid"
        nc.save_to_midi(nc.json_to_noteSeq(melody_json), out)
        outputs.append(out)
        i += 1
        print(f"Saved midi to {out}")

    return outputs

def continue_melody_noteseq(melody_noteseq, n_steps = 64, temperature = 1):

    json_noteseq = nc.noteseq_to_json(melody_noteseq)
    process = subprocess.Popen(['node', os.getcwd() + '\MagentaGenerator\magentaContinue.js', str(json_noteseq), str(n_steps), str(temperature)], stdout=subprocess.PIPE)

    # Lee toda la salida del proceso a la vez
    output, _ = process.communicate()

    melody = json.loads(output)

    out = "./midi/continued_melody.mid"
    nc.save_to_midi(nc.json_to_noteSeq(melody), out)

    print(f"Saved midi to {out}")

    return out

def continue_melody_midi(melody_midi, n_steps = 64, temperature = 1.5):

    noteseq = nc.load_from_midi(melody_midi)

    quantized_seq = note_seq.quantize_note_sequence(noteseq, steps_per_quarter=2)

    # out = "./midi/continued_melody.mid"
    # nc.save_to_midi(quantized_seq, out)

    # print(f"Saved midi to {out}")

    return continue_melody_noteseq(quantized_seq, n_steps, temperature)

# out = generate_melodies(1)

# continue_melody_midi(out[0], 64)
# continue_melody_midi("midi/base_melody_0.mid")