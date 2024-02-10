import midiUtils as MidiUtils
import song as Song
import scale as Scale
import os

class HarmonyGenerator:
    def generate(bassline, input = "midi/input_song.mid", outputDir = "midi/", outputHarmonyFile = "output_harmony", outputBasslineFile = "output_bass"):
        
        someChords = {
            "": Scale.Scale("1 3 5"),  # Mayor
            "-": Scale.Scale("1 b3 5"),  # Menor
            "-b5": Scale.Scale("1 b3 b5"),  # Disminuida
            "7": Scale.Scale("1 3 5 b7"),  # Dominante 
        }

        melody = MidiUtils.read_midi_song(input)
        song = Song.Song(melody)
        song.choose_scale()
        harmony = song.armonize(timeSignature = 4.0, possibleChords = someChords)

        #si no existe el directorio de salida lo crea
        if not os.path.isdir(outputDir):
            os.mkdir(outputDir)
            
        #si no existe el archivo de salida lo crea
        if not os.path.isfile(outputHarmonyFile):
            with open(os.path.join(outputDir, outputHarmonyFile + ".mid"), 'w') as fp: 
                pass

        harmonyMidi = outputDir + outputHarmonyFile + ".mid"
        MidiUtils.write_midi_song(harmonyMidi, harmony)

        basslineMidi = outputDir + outputBasslineFile + ".mid"
        bassline = song.process_bassline_4x4_v2(bassline, harmony)
        MidiUtils.write_midi_song(basslineMidi, bassline)

        return harmonyMidi, basslineMidi
    
    