import midiUtils
from drumPattern import DrumPattern

class DrumGenerator:
    def generate(style):
        drumPatternA, drumPatternB, drumPatternC = DrumPattern.generatePatterns(style)

        midiUtils.make_midi_song("midi/output_"+style.name+"_drumPatternA.mid", drumPatternA)
        midiUtils.make_midi_song("midi/output_"+style.name+"_drumPatternB.mid", drumPatternB)
        midiUtils.make_midi_song("midi/output_"+style.name+"_drumPatternC.mid", drumPatternC)