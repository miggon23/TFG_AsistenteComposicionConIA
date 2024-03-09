import midiUtils as MidiUtils
import song as Song
import scale as Scale
import os
from timeSignature import TimeSignature as ts
import note as Note
from models import ModalPerspective

class HarmonyGenerator:
    def generate(bassline, input = "midi/input_song.mid", outputDir = "midi/", outputHarmonyFile = "output_harmony", outputBasslineFile = "output_bass"):
        
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

        #si no existe el directorio de salida lo crea
        if not os.path.isdir(outputDir):
            os.mkdir(outputDir)
            
        #si no existe el archivo de salida lo crea
        if not os.path.isfile(outputHarmonyFile):
            with open(os.path.join(outputDir, outputHarmonyFile + ".mid"), 'w') as fp: 
                pass

        harmonyMidi = outputDir + outputHarmonyFile + ".mid"
        MidiUtils.write_midi_song(harmonyMidi, harmony, ticksPerBeat)

        return harmonyMidi, harmonyMidi
    
    def generateModal(inputMidi = "midi/input_song.mid", outputSongDir = ".midis/", outputHarmonyDir = ".midis/"):

        someChords = {
            "": Scale.Scale("1 3 5"),  # Mayor
            "-": Scale.Scale("1 b3 5"),  # Menor
        }

        for mode in ModalPerspective.modes:
            if mode is not None:
                
                modalModel = ModalPerspective(mode, chordWeights=[1, 1, 0.1], suggestedChords=someChords)
                modalModel.load_model()

                notes, ticksPerBeat = MidiUtils.read_midi_song(inputMidi)
                
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
                song.choose_sacle(modalModel.modalScale, tonic)
                song.fit_notes(notePenalties=notePenalties)

                harmony = song.armonize(type="win",
                                        timeSignatures = [
                                            ts(4, 4).set_weights([1.4, 1.1, 1.2, 1.1]),
                                            ts(2, 4).set_weights([1.4, 1.2])                      
                                        ],  
                                        possibleChords = modalModel.possibleChords,
                                        model=modalModel)
                
                MidiUtils.write_midi_song(outputHarmonyDir + mode  + ".mid", harmony, ticksPerBeat)
                MidiUtils.write_midi_song(outputSongDir + mode + ".mid", song.notes, ticksPerBeat)
    
