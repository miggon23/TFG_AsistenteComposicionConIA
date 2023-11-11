import midiUtils
import song
import note

class HarmonyGenerator:
    def generate(input):
        melody_ = midiUtils.read_midi_song(input)
        song_ = song.Song(melody_[:-1], note.Note("A"))
        song_.choose_scale()
        harmony_ = song_.armonize(ticksPerSlice=1.0)
        song_.print_chord_analysis()

        output = "midi/output_harmony.mid"
        midiUtils.make_midi_song(output, harmony_)

        return output