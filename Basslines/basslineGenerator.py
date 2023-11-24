import midiUtils
from basslinePattern import BasslinePattern

class BasslineGenerator:
    def generate():
        line = BasslinePattern.generatePatterns()

        # midiUtils.write_midi_song("midi/output_"+style.name+"_drumPatternA.mid", drumPatternA)