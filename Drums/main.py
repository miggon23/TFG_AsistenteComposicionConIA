import midiUtils
from enums import Style
from drumPattern import DrumPattern

if __name__ == "__main__":
    
    style = Style.BASIC
    drumPatternA, drumPatternB, drumPatternC = DrumPattern.generatePatterns(style)

    midiUtils.make_midi_song("midi/output_"+style.name+"_drumPatternA.mid", drumPatternA)
    midiUtils.make_midi_song("midi/output_"+style.name+"_drumPatternB.mid", drumPatternB)
    midiUtils.make_midi_song("midi/output_"+style.name+"_drumPatternC.mid", drumPatternC)