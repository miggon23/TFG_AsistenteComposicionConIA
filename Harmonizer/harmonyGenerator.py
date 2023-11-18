import midiUtils as MidiUtils
import song as Song
import scale as Scale
import os

class HarmonyGenerator:
    def generate(input = "midi/input_song.mid", outputDir = "midi/", outputFile = "output_harmony"):

        someChords = {
            "": Scale.Scale("1 3 5"),  # Mayor
            "-": Scale.Scale("1 b3 5"),  # Menor
            "-b5": Scale.Scale("1 b3 b5"),  # Disminuida
            "7": Scale.Scale("1 3 5 b7"),  # Dominante 
        }

        melody = MidiUtils.read_midi_song(input)
        song = Song.Song(melody)
        song.choose_scale()
        harmony = song.armonize(ticksPerSlice = 4.0, possibleChords = someChords)

        #si no existe el directorio de salida lo crea
        if not os.path.isdir(outputDir):
            os.mkdir(outputDir)
            
        #si no existe el archivo de salida lo crea
        if not os.path.isfile(outputFile):
            with open(os.path.join(outputDir, outputFile + ".mid"), 'w') as fp: 
                pass

        harmonyMidi = outputDir + outputFile + ".mid"

        MidiUtils.write_midi_song(harmonyMidi, harmony)

        return harmonyMidi