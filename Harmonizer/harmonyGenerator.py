import MidiUtils
import Song
import Note

class HarmonyGenerator:
    def generate(input):
        melody_ = MidiUtils.read_midi_song(input)
        song_ = Song.Song(melody_[:-1], Note.Note("A"))
        song_.choose_scale()
        harmony_ = song_.armonize(ticksPerSlice=1.0)
        song_.print_chord_analysis()

        output = "midi/output_harmony.mid"
        MidiUtils.write_midi_song(output, harmony_)

        return output