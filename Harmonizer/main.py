import midiUtils as MidiUtils
import song as Song
import note as Note
import scale as Scale
import harmony as Harmony
from timeSignature import TimeSignature as ts

if __name__ == "__main__":

    # MidiUtils.debug_midi_file("midi/input_song.mid", "files/midi_out.txt") 
    # melody, ticksPerBeat = MidiUtils.read_midi_song("midi/input_song.mid")
    # MidiUtils.write_midi_song("midi/output_song.mid", melody, ticksPerBeat)

    someChords = {
        "": Scale.Scale("1 3 5"),  # Mayor
        "-": Scale.Scale("1 b3 5"),  # Menor
        "-b5": Scale.Scale("1 b3 b5"),
        "7": Scale.Scale("1 3 5 b7"),  # Dominante 
    }

    melody, ticksPerBeat = MidiUtils.read_midi_song("midi/input_song.mid")
    MidiUtils.debug_midi_file("midi/input_song.mid", "files/midi_out.txt") 
    Song.debug_song(melody, "files/notes_out.txt")
    song = Song.Song(melody, ticksPerBeat)
    song.choose_scale()
    harmony = song.armonize(type = "win",
                            timeSignatures = [
                                ts(4, 4).set_weights([1.4, 1.1, 1.2, 1.1]),
                                ts(2, 4).set_weights([1.4, 1.2]),
                                ts(1, 4).set_weights([1])
                            ],  
                            possibleChords = someChords)
    song.save_data('datasets/matrix.xlsx')
    MidiUtils.write_midi_song("midi/output_harmony.mid", harmony, ticksPerBeat)
    MidiUtils.write_midi_song("midi/output_song.mid", melody, ticksPerBeat)
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

    





