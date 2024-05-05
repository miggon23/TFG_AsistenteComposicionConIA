import midiUtils as MidiUtils
import song as Song
import scale as Scale
import os
from timeSignature import TimeSignature as ts
import note as Note
from models import ModalPerspective
import harmony as Harmony

class HarmonyGenerator:

    def treatMelody(input = "./Media/midi/input_song.mid", output = "./Media/midi/output_song.mid"):

        melody, ticksPerBeat = MidiUtils.read_midi_song(input)
        song = Song.Song(melody, ticksPerBeat)

        song.traspose(int((song.meanPitch - 72) / 12) * -12)

        MidiUtils.write_midi_song(output, song.notes, ticksPerBeat)

        return output
    
    def spreadSong(input = "./Media/midi/input_song.mid", 
                output1 = "./Media/midi/output_song1.mid", 
                output2 = "./Media/midi/output_song2.mid", 
                ticks = 4):

        melody, ticksPerBeat = MidiUtils.read_midi_song(input)
        song = Song.Song(melody, ticksPerBeat)
        song, cont = song.divide_song(int(ticks))

        MidiUtils.write_midi_song(output1, song.notes, ticksPerBeat)
        MidiUtils.write_midi_song(output2, cont.notes, ticksPerBeat)

        return output1, output2
    
    def combineSongs(input1, input2, output = "./Media/midi/combined_song.mid", ticks = 0):

        melody, ticksPerBeat = MidiUtils.read_midi_song(input1)
        song = Song.Song(melody, ticksPerBeat)

        melody2, ticksPerBeat2 = MidiUtils.read_midi_song(input2)

        if ticksPerBeat != ticksPerBeat2:
            raise Exception("Canciones incompatibles")
        
        song.add_song(Song.Song(melody2, ticksPerBeat2), ticks)

        MidiUtils.write_midi_song(output, song.notes, ticksPerBeat)

        return output

    
    def generate(input = "./Media/midi/input_song.mid", 
                output_melody = "./Media/midi/output_melody.mid",
                output_harmony = "./Media/midi/output_harmony.mid",
                output_std_harmony = "./Media/midi/output_std_harmony.mid"):

        output_melody_list = []
        output_harmony_list = []
        output_std_harmony_list = []

        notes, ticksPerBeat = MidiUtils.read_midi_song(input)

        timeSignatures = [
            ts(4, 4).set_weights([1.4, 1.1, 1.2, 1.1]),
            ts(2, 4).set_weights([1.4, 1.2]),
            ts(1, 4).set_weights([1])
        ]

        song = Song.Song(notes, ticksPerBeat)

        majorWeight = song.find_chord_sequence(chordProgressions=Harmony.majorProgressions,
                                        timeSignatures=timeSignatures[:2],
                                        loop=True)[-1]
        majorTonic = song.tonic
        
        minorWeight = song.find_chord_sequence(chordProgressions=Harmony.minorProgressions,
                                        timeSignatures=timeSignatures[:2],
                                        loop=True)[-1]
        minorTonic = song.tonic
        
        if majorWeight > minorWeight:
            harmony, harmony_std, _ = song.find_chord_sequence(chordProgressions=Harmony.majorProgressions,
                                        timeSignatures=timeSignatures[:2],
                                        loop=True,
                                        respectTonic=majorTonic)
            tonic = song.tonic
            scale = Scale.allScales["Major"]
        else:
            harmony, harmony_std, _ = song.find_chord_sequence(chordProgressions=Harmony.minorProgressions,
                                        timeSignatures=timeSignatures[:2],
                                        loop=True,
                                        respectTonic=minorTonic)
            tonic = song.tonic
            scale = Scale.allScales["minor"]

        song.choose_sacle(scale, tonic)
        song.fit_notes()    
        
        print(f"Tonica original: {tonic.name}")
        song.print_best_chords()

        MidiUtils.write_midi_song(output_melody, song.notes, ticksPerBeat)
        MidiUtils.write_midi_song(output_harmony, harmony, ticksPerBeat)
        MidiUtils.write_midi_song(output_std_harmony, harmony_std, ticksPerBeat)

        output_melody_list.append(output_melody)
        output_harmony_list.append(output_harmony)
        output_std_harmony_list.append(output_std_harmony)

        someChords = {
            "": Scale.Scale("1 3 5"),  # Mayor
            "-": Scale.Scale("1 b3 5"),  # Menor
            "-b5": Scale.Scale("1 b3 b5")
        }

        for mode in ModalPerspective.modes:
            if mode is not None:

                notes, ticksPerBeat = MidiUtils.read_midi_song(input)
                song = Song.Song(notes, ticksPerBeat)

                modalPerspective = ModalPerspective(mode, suggestedChords=someChords)

                notePenalties = [1] * 7
                for colorNote in modalPerspective.colorNotes:
                    for idx, interval in enumerate(modalPerspective.modalScale.scale):
                        if colorNote == interval:
                            notePenalties[idx] = 0
                            break
                notePenalties[0] = 0

                song.choose_sacle(modalPerspective.modalScale, tonic)
                song.fit_notes(notePenalties=notePenalties)

                harmony, harmony_std = song.find_chord_sequence(
                    chordProgressions=modalPerspective.chordProgressions,
                    timeSignatures=timeSignatures[:2], 
                    loop=True,
                    respectTonic=True)[:-1]
                
                print(f"Tonica {mode}: {song.tonic.name}")
                song.print_best_chords()
                
                output_melody_mode = output_melody[:-4] + "_" + mode + ".mid" 
                output_harmony_mode = output_harmony[:-4] + "_" + mode + ".mid"
                output_std_harmony_mode = output_std_harmony[:-4] + "_"  + mode + ".mid"
                MidiUtils.write_midi_song(output_melody_mode, song.notes, ticksPerBeat)
                MidiUtils.write_midi_song(output_harmony_mode, harmony, ticksPerBeat)
                MidiUtils.write_midi_song(output_std_harmony_mode, harmony_std, ticksPerBeat)
                output_melody_list.append(output_melody_mode)
                output_harmony_list.append(output_harmony_mode)
                output_std_harmony_list.append(output_std_harmony_mode)

        return output_melody_list, output_harmony_list, output_std_harmony_list
    
    def generate2(input = "./Media/midi/input_song.mid", 
                output_melody = "./Media/midi/output_melody.mid",
                output_harmony = "./Media/midi/output_harmony.mid",
                output_std_harmony = "./Media/midi/output_std_harmony.mid"):
        
        output_melody_list = []
        output_harmony_list = []
        output_std_harmony_list = []
        
        A, B = HarmonyGenerator.spreadSong(input, ticks=4*4)
        A_B = HarmonyGenerator.combineSongs(A, B)

        notes, ticksPerBeat = MidiUtils.read_midi_song(A_B)

        timeSignatures = [
            ts(4, 4).set_weights([1.4, 1.1, 1.2, 1.1]),
            ts(2, 4).set_weights([1.4, 1.2]),
            ts(1, 4).set_weights([1])
        ]

        song = Song.Song(notes, ticksPerBeat)

        majorWeight = song.find_chord_sequence(chordProgressions=Harmony.majorProgressions,
                                        timeSignatures=timeSignatures[:2],
                                        loop=True)[-1]
        majorTonic = song.tonic
        
        minorWeight = song.find_chord_sequence(chordProgressions=Harmony.minorProgressions,
                                        timeSignatures=timeSignatures[:2],
                                        loop=True)[-1]
        minorTonic = song.tonic
        
        if majorWeight > minorWeight:
            tonic = majorTonic
            scale = Scale.allScales["Major"]
            chordProgressions = Harmony.majorProgressions
        else:
            tonic = minorTonic
            scale = Scale.allScales["minor"]
            chordProgressions = Harmony.minorProgressions

        song.choose_sacle(scale, tonic)
        song.fit_notes()   

        harmony, harmony_std, _ = song.find_chord_sequence(
            chordProgressions=chordProgressions,
            timeSignatures=timeSignatures[:2], 
            loop=True,
            respectTonic=True) 
        
        print(f"Tonica original: {tonic.name}")
        song.print_best_chords()

        notes, ticksPerBeat = MidiUtils.read_midi_song(input)
        song = Song.Song(notes, ticksPerBeat)
        song.choose_sacle(scale, tonic)
        song.fit_notes()

        MidiUtils.write_midi_song(output_melody, song.notes, ticksPerBeat)
        MidiUtils.write_midi_song(output_harmony, harmony, ticksPerBeat)
        MidiUtils.write_midi_song(output_std_harmony, harmony_std, ticksPerBeat)

        output_melody_list.append(output_melody)
        output_harmony_list.append(output_harmony)
        output_std_harmony_list.append(output_std_harmony)

        notes, ticksPerBeat = MidiUtils.read_midi_song(A_B)
        song = Song.Song(notes, ticksPerBeat)
        song.choose_sacle(scale, tonic)
        song.fit_notes()
        MidiUtils.write_midi_song("./Media/midi/combined_song_debug.mid", song.notes, ticksPerBeat)

        someChords = {
            "": Scale.Scale("1 3 5"),  # Mayor
            "-": Scale.Scale("1 b3 5"),  # Menor
            "-b5": Scale.Scale("1 b3 b5")
        }

        for mode in ModalPerspective.modes:
            if mode is not None:

                notes, ticksPerBeat = MidiUtils.read_midi_song(A_B)
                song = Song.Song(notes, ticksPerBeat)

                modalPerspective = ModalPerspective(mode, suggestedChords=someChords)

                notePenalties = [1] * 7
                for colorNote in modalPerspective.colorNotes:
                    for idx, interval in enumerate(modalPerspective.modalScale.scale):
                        if colorNote == interval:
                            notePenalties[idx] = 0
                            break
                notePenalties[0] = 0

                song.choose_sacle(modalPerspective.modalScale, tonic)
                song.fit_notes(notePenalties=notePenalties)

                harmony, harmony_std = song.find_chord_sequence(
                    chordProgressions=modalPerspective.chordProgressions,
                    timeSignatures=timeSignatures[:2], 
                    loop=True,
                    respectTonic=True)[:-1]
                
                print(f"Tonica {mode}: {song.tonic.name}")
                song.print_best_chords()

                notes, ticksPerBeat = MidiUtils.read_midi_song(input)
                song = Song.Song(notes, ticksPerBeat)
                song.choose_sacle(modalPerspective.modalScale, tonic)
                song.fit_notes()
                
                output_melody_mode = output_melody[:-4] + "_" + mode + ".mid" 
                output_harmony_mode = output_harmony[:-4] + "_" + mode + ".mid"
                output_std_harmony_mode = output_std_harmony[:-4] + "_"  + mode + ".mid"
                MidiUtils.write_midi_song(output_melody_mode, song.notes, ticksPerBeat)
                MidiUtils.write_midi_song(output_harmony_mode, harmony, ticksPerBeat)
                MidiUtils.write_midi_song(output_std_harmony_mode, harmony_std, ticksPerBeat)
                output_melody_list.append(output_melody_mode)
                output_harmony_list.append(output_harmony_mode)
                output_std_harmony_list.append(output_std_harmony_mode)

        return output_melody_list, output_harmony_list, output_std_harmony_list






    
