import Drums.oldMidiUtils as oldMidiUtils
from drumPattern import DrumPattern
from Drums import enums

class DrumGenerator:
    def generate(style):
        drumPatternA, drumPatternB, drumPatternC = DrumPattern.generatePatterns(style)

        oldMidiUtils.write_midi_song("midi/output_"+style.name+"_drumPatternA.mid", drumPatternA)
        oldMidiUtils.write_midi_song("midi/output_"+style.name+"_drumPatternB.mid", drumPatternB)
        oldMidiUtils.write_midi_song("midi/output_"+style.name+"_drumPatternC.mid", drumPatternC)

    def generateAllStyles():
        DrumGenerator.generate(enums.Style.BASIC)
        DrumGenerator.generate(enums.Style.KICK)
        DrumGenerator.generate(enums.Style.CLAP)
        DrumGenerator.generate(enums.Style.SHAKER)
        DrumGenerator.generate(enums.Style.JAZZ)
        DrumGenerator.generate(enums.Style.DISCO)
        DrumGenerator.generate(enums.Style.METAL)
        DrumGenerator.generate(enums.Style.LATIN)
        DrumGenerator.generate(enums.Style.ROCK)        