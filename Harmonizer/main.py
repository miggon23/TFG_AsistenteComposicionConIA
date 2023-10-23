import midiUtils
import song
import note
import scale
import harmony

if __name__ == "__main__":
    # midiUtils.make_midi_song("midi/midi.mid", [])
    # midiUtils.read_midi_file("midi/midi.mid", "files/midi_out.txt")
    # extracted_notes = midiUtils.read_midi_song("midi/midi.mid", "files/notes_out.txt") 
     
    # scale = scale.Scale("1 2 3 4 5 b6 7")
    # scale.create_degrees()
    # scale.print_degrees()
    # print()
    # harmony = harmony.Harmony(scale)
    # harmony.print_chords()
    # print()
    # harmony.relativize_chords()
    # harmony.print_relativized_chords()
    # print()

    #read midi funciona del orto (me lo hizo chatGPT 😡)
    #hay que poner una nota random al principio si no, peta
    #te desplaza toda la canción varios compases a la derecha por la polla
    #lo cambiaré en el futuro
    s = midiUtils.read_midi_song("midi/input_song.mid", "files/notes_out.txt")  
    song = song.Song(s[:-1], note.Note("C"))
    song.choose_scale()
    s = song.armonize(ticksPerSlice=2.0)
    midiUtils.make_midi_song("midi/temita.mid", s)





