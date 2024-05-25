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
        song = Song.Song(notes, ticksPerBeat)

        timeSignatures = [
            ts(4, 4).set_weights([1.4, 1.1, 1.2, 1.1]),
            ts(2, 4).set_weights([1.4, 1.2]),
            ts(1, 4).set_weights([1])
        ]  

        someChords = {
            "": Scale.Scale("1 3 5"), 
            "-": Scale.Scale("1 b3 5"), 
        }   

        majorWeight = song.find_chord_sequence(chordProgressions=Harmony.majorProgressions,
                                        timeSignatures=timeSignatures[:2],
                                        loop=True)[-1]
        majorTonic = song.tonic
        
        minorWeight = song.find_chord_sequence(chordProgressions=Harmony.minorProgressions,
                                        timeSignatures=timeSignatures[:2],
                                        loop=True)[-1]
        minorTonic = song.tonic

        if majorWeight == 0 and minorWeight == 0:
            print('No hay ninguna solución Mayor o menor')  
            print('Se procede a armonizar con el algoritmo anterior')
            song.choose_sacle(Scale.allScales["Major"], song.most_frequent_note())
            song.fit_notes() 
            harmony, harmony_std = song.armonize(type = "win", 
                possibleChords = someChords, 
                timeSignatures = timeSignatures[:2])  
        else:   
            if majorWeight > minorWeight:
                print('Escala original: Mayor')
                song.choose_sacle(Scale.allScales["Major"], majorTonic)
                chordProgressions = Harmony.majorProgressions
            else:
                print('Escala original: menor')
                song.choose_sacle(Scale.allScales["minor"], minorTonic)
                chordProgressions = Harmony.minorProgressions

            song.fit_notes()   
            harmony, harmony_std = song.find_chord_sequence(chordProgressions=chordProgressions,
                                timeSignatures=timeSignatures[:2],
                                loop=True,
                                respectTonic=True)[:-1] 
        
        tonic = song.tonic
        print(f"Tonica original: {tonic.name}")
        song.print_best_chords()

        MidiUtils.write_midi_song(output_melody, song.notes, ticksPerBeat)
        MidiUtils.write_midi_song(output_harmony, harmony, ticksPerBeat)
        MidiUtils.write_midi_song(output_std_harmony, harmony_std, ticksPerBeat)

        output_melody_list.append(output_melody)
        output_harmony_list.append(output_harmony)
        output_std_harmony_list.append(output_std_harmony)

        someChords["-b5"] = Scale.Scale("1 b3 b5")

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

                harmony, harmony_std, weight = song.find_chord_sequence(
                    chordProgressions=modalPerspective.chordProgressions,
                    timeSignatures=timeSignatures[:2], 
                    loop=True,
                    respectTonic=True)
                
                if weight == 0:
                    print(f'La busqueda de progresiones ha fallado para el modo {mode},') 
                    print('se procede a armonizar con el algoritmo anterior')
                    song.choose_sacle(modalPerspective.modalScale, tonic)
                    harmony, harmony_std = song.armonize(type = "win", 
                        possibleChords = modalPerspective.possibleChords, 
                        timeSignatures = timeSignatures[:2])
                
                output_melody_mode = output_melody[:-4] + mode + ".mid" 
                output_harmony_mode = output_harmony[:-4] + mode + ".mid"
                output_std_harmony_mode = output_std_harmony[:-4] + mode + ".mid"
                MidiUtils.write_midi_song(output_melody_mode, song.notes, ticksPerBeat)
                MidiUtils.write_midi_song(output_harmony_mode, harmony, ticksPerBeat)
                MidiUtils.write_midi_song(output_std_harmony_mode, harmony_std, ticksPerBeat)
                output_melody_list.append(output_melody_mode)
                output_harmony_list.append(output_harmony_mode)
                output_std_harmony_list.append(output_std_harmony_mode)

        return output_melody_list, output_harmony_list, output_std_harmony_list

    
    def super_repetitiva(input = "./Media/midi/input_song.mid", 
                output_melody = "./Media/midi/output_melody.mid",
                output_harmony = "./Media/midi/output_harmony.mid",
                output_std_harmony = "./Media/midi/output_std_harmony.mid"):
        
        return HarmonyGenerator.generate(input,
                                         output_melody,
                                         output_harmony,
                                         output_std_harmony)

        
    
    def repetitiva(input = "./Media/midi/input_song.mid", 
                output_melody = "./Media/midi/output_melody.mid",
                output_harmony = "./Media/midi/output_harmony.mid",
                output_std_harmony = "./Media/midi/output_std_harmony.mid"):
        
        output_melody_list = []
        output_harmony_list = []
        output_std_harmony_list = []
        
        A, B = HarmonyGenerator.spreadSong(input, ticks=4*4)
        A_B = HarmonyGenerator.combineSongs(A, B)

        notes, ticksPerBeat = MidiUtils.read_midi_song(A_B)
        song = Song.Song(notes, ticksPerBeat)

        timeSignatures = [
            ts(4, 4).set_weights([1.4, 1.1, 1.2, 1.1]),
            ts(2, 4).set_weights([1.4, 1.2]),
            ts(1, 4).set_weights([1])
        ] 

        someChords = {
            "": Scale.Scale("1 3 5"),  # Mayor
            "-": Scale.Scale("1 b3 5")  # Menor
        }    

        majorWeight = song.find_chord_sequence(chordProgressions=Harmony.majorProgressions,
                                        timeSignatures=timeSignatures[:2],
                                        loop=True)[-1]
        majorTonic = song.tonic
        
        minorWeight = song.find_chord_sequence(chordProgressions=Harmony.minorProgressions,
                                        timeSignatures=timeSignatures[:2],
                                        loop=True)[-1]
        minorTonic = song.tonic

        if majorWeight == 0 and minorWeight == 0:
            print('No hay ninguna solución Mayor o menor')  
            print('Se procede a armonizar con el algoritmo anterior')
            song.choose_sacle(Scale.allScales["Major"], song.most_frequent_note())
            song.fit_notes() 
            harmony, harmony_std = song.armonize(type = "win", 
                possibleChords = someChords, 
                timeSignatures = timeSignatures[:2])    
        else:
            if majorWeight > minorWeight:
                print('Escala original: Mayor')
                song.choose_sacle(Scale.allScales["Major"], majorTonic)
                chordProgressions = Harmony.majorProgressions
            else:
                print('Escala original: menor')
                song.choose_sacle(Scale.allScales["minor"], minorTonic)
                chordProgressions = Harmony.minorProgressions

            song.fit_notes()   
            harmony, harmony_std = song.find_chord_sequence(chordProgressions=chordProgressions,
                                timeSignatures=timeSignatures[:2],
                                loop=True,
                                respectTonic=True)[:-1] 
        
        scale = song.scale
        tonic = song.tonic 
        print(f"Tonica original: {song.tonic.name}")
        song.print_best_chords() 

        # Se vuelve a abrir el archivo original  
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

        someChords["-b5"] = Scale.Scale("1 b3 b5")

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

                harmony, harmony_std, weight = song.find_chord_sequence(
                    chordProgressions=modalPerspective.chordProgressions,
                    timeSignatures=timeSignatures[:2], 
                    loop=True,
                    respectTonic=True)
                
                if weight == 0:
                    print(f'La busqueda de progresiones ha fallado para el modo {mode},') 
                    print('se procede a armonizar con el algoritmo anterior')
                    song.choose_sacle(modalPerspective.modalScale, tonic)
                    harmony, harmony_std = song.armonize(type = "win", 
                        possibleChords = modalPerspective.possibleChords, 
                        timeSignatures = timeSignatures[:2])

                notes, ticksPerBeat = MidiUtils.read_midi_song(input)
                song = Song.Song(notes, ticksPerBeat)
                song.choose_sacle(modalPerspective.modalScale, tonic)
                song.fit_notes()
                
                output_melody_mode = output_melody[:-4] + mode + ".mid" 
                output_harmony_mode = output_harmony[:-4] + mode + ".mid"
                output_std_harmony_mode = output_std_harmony[:-4] + mode + ".mid"
                MidiUtils.write_midi_song(output_melody_mode, song.notes, ticksPerBeat)
                MidiUtils.write_midi_song(output_harmony_mode, harmony, ticksPerBeat)
                MidiUtils.write_midi_song(output_std_harmony_mode, harmony_std, ticksPerBeat)
                output_melody_list.append(output_melody_mode)
                output_harmony_list.append(output_harmony_mode)
                output_std_harmony_list.append(output_std_harmony_mode)

        return output_melody_list, output_harmony_list, output_std_harmony_list
    
    def estandar(input = "./Media/midi/input_song.mid", 
                output_melody = "./Media/midi/output_melody.mid",
                output_harmony = "./Media/midi/output_harmony.mid",
                output_std_harmony = "./Media/midi/output_std_harmony.mid"):
        
        return HarmonyGenerator.generate(input,
                                    output_melody,
                                    output_harmony,
                                    output_std_harmony)






    
