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
                    output1 = "./Media/midi/output_harmony.mid",
                    output2 = "./Media/midi/output_std_harmony.mid"):

        notes, ticksPerBeat = MidiUtils.read_midi_song(input)

        timeSignatures = [
            ts(4, 4).set_weights([1.4, 1.1, 1.2, 1.1]),
            ts(2, 4).set_weights([1.4, 1.2]),
            ts(1, 4).set_weights([1])
        ]

        song = Song.Song(notes, ticksPerBeat)

        invertedHarmony, harmony = song.find_chord_sequence(timeSignatures=timeSignatures[:2],
                                        loop=True)

        print(f"Tónica: {song.tonic.name}")
        song.print_best_chords()

        MidiUtils.write_midi_song(output1, invertedHarmony, ticksPerBeat)
        MidiUtils.write_midi_song(output2, harmony, ticksPerBeat)

        return output1, output2




    
