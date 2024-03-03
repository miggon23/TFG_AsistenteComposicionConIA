import midiUtils as MidiUtils
import song as Song
import note as Note
import scale as Scale
import harmony as Harmony
import dataCollectors as Data
from models import Chain, ModalPerspective
from timeSignature import TimeSignature as ts

def modal(mode):

    someChords = {
        "": Scale.Scale("1 3 5"),  # Mayor
        "-": Scale.Scale("1 b3 5"),  # Menor
    }

    modalModel = ModalPerspective(mode, chordWeights=[1, 1, 0.1], suggestedChords=someChords)
    modalModel.load_model()

    notes, ticksPerBeat = MidiUtils.read_midi_song("midi/input_song.mid")
    
    song = Song.Song(notes, ticksPerBeat)

    tonicPen = 0.5
    possibleTonics = [0] * 12
    for idx, noteFrequency in enumerate(song.noteFrequencies):
        possibleTonics[idx] += noteFrequency * tonicPen
        for colorNote in modalModel.colorNotes:
            possibleTonics[idx] += song.noteFrequencies[(idx + colorNote.semitones) % 12]

    notePenalties = [1] * 7
    for colorNote in modalModel.colorNotes:
        for idx, interval in enumerate(modalModel.modalScale.scale):
            if colorNote == interval:
                notePenalties[idx] = 0
                break

    tonic = Note.Note(possibleTonics.index(max(possibleTonics)))
    print(f'{mode}: {tonic.name}')
    print(f'Color note(s):', end=' ')
    for colorNote in modalModel.colorNotes:
        print(f'{Note.Note(tonic.pitch + colorNote.semitones).name}', end=' ')
    print('\n')
    song.choose_sacle(modalModel.modalScale, tonic)
    song.fit_notes(notePenalties=notePenalties)

    harmony = song.armonize(type="win",
                            timeSignatures = [
                                ts(4, 4).set_weights([1.4, 1.1, 1.2, 1.1]),
                                ts(2, 4).set_weights([1.4, 1.2])                      
                            ],  
                            possibleChords = modalModel.possibleChords,
                            model=modalModel)
    
    # MidiUtils.write_midi_song("midi/" + mode  + "_output_harmony.mid", harmony, ticksPerBeat)
    # MidiUtils.write_midi_song("midi/" + mode  + "_output_song.mid", song.notes, ticksPerBeat)

    MidiUtils.write_midi_song("midi/" + mode + ".mid", song.notes + harmony, ticksPerBeat)


def standar():
    
    someChords = {
        "": Scale.Scale("1 3 5"),  # Mayor
        "-": Scale.Scale("1 b3 5"),  # Menor
        "-b5": Scale.Scale("1 b3 b5"),
        "7": Scale.Scale("1 3 5 b7"),  # Dominante 
        "º7": Scale.Scale("1 b3 b5 bb7"),  # Séptima disminuida (Disminuida)
    }

    notes, ticksPerBeat = MidiUtils.read_midi_song("midi/input_song.mid")
    # MidiUtils.debug_midi_file("midi/input_song.mid", "files/midi_out.txt") 
    # Song.debug_song(notes, "files/notes_out.txt")
    song = Song.Song(notes, ticksPerBeat)
    song.fill_scale()
    # song.set_harmony(someChords)
    harmony = song.armonize(type = "win",
                            timeSignatures = [
                                ts(4, 4).set_weights([1.4, 1.1, 1.2, 1.1]),
                                ts(2, 4).set_weights([1.4, 1.2])
                            ],  
                            possibleChords = someChords
                            )
    Data.seave_all(song, 'datasets/chords')
    MidiUtils.write_midi_song("midi/output_harmony.mid", harmony, ticksPerBeat)
    MidiUtils.write_midi_song("midi/output_song.mid", song.notes, ticksPerBeat)

    # print()
    # song.print_chord_analysis()
    # print()
    # song.print_best_chords()
    # print()
    # song.scale.print_degrees()
    # print()
    # song.harmony.print_chords()

if __name__ == "__main__":
    standar()
    for mode in ModalPerspective.modes:
        if mode is not None:
            modal(mode)

    

    





