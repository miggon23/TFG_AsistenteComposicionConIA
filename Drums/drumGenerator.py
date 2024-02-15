import Drums.oldMidiUtils as oldMidiUtils
from drumPattern import DrumPattern

class DrumGenerator:
    def generate(style):
        drumPatternA, drumPatternB, drumPatternC = DrumPattern.generatePatterns(style)

        oldMidiUtils.write_midi_song("midi/output_"+style.name+"_drumPatternA.mid", drumPatternA)
        oldMidiUtils.write_midi_song("midi/output_"+style.name+"_drumPatternB.mid", drumPatternB)
        oldMidiUtils.write_midi_song("midi/output_"+style.name+"_drumPatternC.mid", drumPatternC)