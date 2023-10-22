import midiUtils
import song
import note
import scale
import harmony

if __name__ == "__main__":
    midiUtils.make_midi_song("midi/midi.mid", [])
    midiUtils.read_midi_file("midi/midi.mid", "files/midi_out.txt")
    extracted_notes = midiUtils.read_midi_song("midi/midi.mid", "files/notes_out.txt")  
    # scale = scale.Scale("1 2 3 4 5 6 7")
    # scale.create_degrees()
    # scale.print_degrees()
    # print()
    # harmony = harmony.Harmony(scale)
    # harmony.print_chords()
    # print()
    # harmony.relativize_chords()
    # harmony.print_relativized_chords()
    # print()
    # s = midiUtils.read_midi_song("midi/input_song.mid", "files/notes_out.txt")  
    # song = song.Song(s, note.Note("F#"))
    # song.choose_scale()






