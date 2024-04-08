import midiUtils as MidiUtils
import song as Song
import scale as Scale
import os
from timeSignature import TimeSignature as ts
import note as Note
from models import ModalPerspective

class HarmonyGenerator:

    def treatMelody(input = "./Media/midi/input_song.mid", output = "./Media/midi/output_song.mid"):

        melody, ticksPerBeat = MidiUtils.read_midi_song(input)
        song = Song.Song(melody, ticksPerBeat)

        song.traspose(int((song.meanPitch - 60) / 12) * -12)

        MidiUtils.write_midi_song(output, song.notes, ticksPerBeat)

        return output


    def generate(input = "./Media/midi/input_song.mid", output = "./Media/midi/output_harmony.mid"):
        
        someChords = {
            "": Scale.Scale("1 3 5"),  # Mayor
            "-": Scale.Scale("1 b3 5"),  # Menor
            "-b5": Scale.Scale("1 b3 b5"),  # Disminuida
            "7": Scale.Scale("1 3 5 b7"),  # Dominante  
            "º7": Scale.Scale("1 b3 b5 bb7"),  # Séptima disminuida (Disminuida)
        }

        melody, ticksPerBeat = MidiUtils.read_midi_song(input)
        song = Song.Song(melody, ticksPerBeat)
        song.fill_scale()
        harmony = song.armonize(type = "win",
                                timeSignatures = [
                                    ts(4, 4).set_weights([1.4, 1.1, 1.2, 1.1]),
                                    ts(2, 4).set_weights([1.4, 1.2]),
                                    ts(1, 4).set_weights([1])
                            ],  
                            possibleChords = someChords)

        MidiUtils.write_midi_song(output, harmony, ticksPerBeat)

        return output
    
    def generateModalMelodies(input = "./Media/midi/input_song.mid", 
                              outputDirectory = "./Media/midi/", 
                              outputFile = "_output_song.mid"):
        
        someChords = {
            "": Scale.Scale("1 3 5"),  
            "-": Scale.Scale("1 b3 5")
        }

        outputs = []
        tonics = []
        models = []

        for mode in ModalPerspective.modes:
            if mode is not None:
                
                modalModel = ModalPerspective(mode, chordWeights=[1, 1, 0.1], suggestedChords=someChords)
                modalModel.load_model()
                models.append(modalModel)

                notes, ticksPerBeat = MidiUtils.read_midi_song(input)             
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
                tonics.append(tonic)
                song.choose_sacle(modalModel.modalScale, tonic)
                song.fit_notes(notePenalties=notePenalties)

                output = outputDirectory + mode + outputFile
                MidiUtils.write_midi_song(output, song.notes, ticksPerBeat)  
                outputs.append(output) 

        return outputs, tonics, models
    
    def generateModalHarmony(tonics, models,
                        inputDirectory = "./Media/midi/", 
                        inputFile = "_input_song.mid", 
                        outputDirectory = "./Media/midi/", 
                        outputFile = "_output_harmony.mid"):
        
        outputs = []

        idx = 0
        for mode in ModalPerspective.modes:
            if mode is not None:

                notes, ticksPerBeat = MidiUtils.read_midi_song(inputDirectory + mode + inputFile) 
                song = Song.Song(notes, ticksPerBeat) 
                song.choose_sacle(models[idx].modalScale, tonics[idx])

                harmony = song.armonize(type="win",
                                        timeSignatures = [
                                            ts(4, 4).set_weights([1.4, 1.1, 1.2, 1.1]),
                                            ts(2, 4).set_weights([1.4, 1.2])                      
                                        ],  
                                        possibleChords = models[idx].possibleChords,
                                        model=models[idx])
                
                output = outputDirectory + mode + outputFile
                MidiUtils.write_midi_song(output, harmony, song.ticksPerBeat)
                outputs.append(output) 

                idx += 1

        return outputs

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
    
    def combineSongs(input, input2, output = "./Media/midi/combined_song.mid"):

        melody, ticksPerBeat = MidiUtils.read_midi_song(input)
        song = Song.Song(melody, ticksPerBeat)

        melody2, ticksPerBeat2 = MidiUtils.read_midi_song(input2)

        if ticksPerBeat != ticksPerBeat2:
            raise Exception("Canciones incompatibles")
        
        song += Song.Song(melody2, ticksPerBeat2)

        MidiUtils.write_midi_song(output, song.notes, ticksPerBeat)

        return output

    
