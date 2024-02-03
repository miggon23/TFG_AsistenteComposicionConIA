import midiUtils as MidiUtils
import song as Song
import note as Note
import scale as Scale
import harmony as Harmony
from timeSignature import TimeSignature as ts

if __name__ == "__main__":

    someChords = {
        "": Scale.Scale("1 3 5"),  # Mayor
        "-": Scale.Scale("1 b3 5"),  # Menor
        "-b5": Scale.Scale("1 b3 b5"),  # Disminuida
        "7": Scale.Scale("1 3 5 b7"),  # Dominante 
    }

    melody, ticksPerBeat = MidiUtils.read_midi_song("midi/input_song.mid")
    MidiUtils.debug_midi_file("midi/input_song.mid", "files/midi_out.txt") 
    Song.debug_song(melody, "files/notes_out.txt")
    song = Song.Song(melody, ticksPerBeat)
    song.choose_scale()
    harmony = song.armonize(type = "win", 
                            possibleChords = someChords)
    song.save_data()
    MidiUtils.write_midi_song("midi/output_harmony.mid", harmony, ticksPerBeat)
    MidiUtils.write_midi_song("midi/output_song.mid", song.melody + harmony, ticksPerBeat)
    # bassline = song.process_bassline_4x4_v2(None, harmony)
    # MidiUtils.write_midi_song("midi/output_bassline.mid", bassline)

    print()
    song.print_chord_analysis()
    print()
    song.print_best_chords()
    print()
    song.scale.print_degrees()
    print()
    song.harmony.print_chords()

    





