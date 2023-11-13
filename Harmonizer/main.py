import MidiUtils
import Song
import Note
import Scale
import Harmony

if __name__ == "__main__":

    someChords = {
        "": Scale.Scale("1 3 5"),  # Mayor
        "-": Scale.Scale("1 b3 5"),  # Menor
        "-b5": Scale.Scale("1 b3 b5"),  # Disminuida
        "7": Scale.Scale("1 3 5 b7"),  # Dominante 
    }

    melody = MidiUtils.read_midi_song("midi/input_song.mid") 
    #Song.debug_song(melody, "files/notes_out.txt")
    song = Song.Song(melody)
    song.choose_scale_v2()
    harmony = song.armonize(ticksPerSlice = 4.0, possibleChords = someChords)
    MidiUtils.write_midi_song("midi/output_harmony.mid", harmony)
    MidiUtils.write_midi_song("midi/output_song.mid", song.melody + harmony)

    song.print_chord_analysis()
    print()
    song.print_best_chords()
    print()
    song.scale.print_degrees()
    print()
    song.harmony.print_chords()
    





