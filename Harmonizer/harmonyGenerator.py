import MidiUtils
import Song
import Scale

class HarmonyGenerator:
    def generate(input):

        someChords = {
            "": Scale.Scale("1 3 5"),  # Mayor
            "-": Scale.Scale("1 b3 5"),  # Menor
            "-b5": Scale.Scale("1 b3 b5"),  # Disminuida
            "7": Scale.Scale("1 3 5 b7"),  # Dominante 
        }

        melody = MidiUtils.read_midi_song("midi/input_song.mid")
        song = Song.Song(melody)
        song.choose_scale()
        harmony = song.armonize(ticksPerSlice = 4.0, possibleChords = someChords)
        harmonyMidi = "midi/output_harmony.mid"
        MidiUtils.write_midi_song(harmonyMidi, harmony)

        return harmonyMidi