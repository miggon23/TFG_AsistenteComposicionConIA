from make_beat import Make_Beat
from make_engine import Make_Engine
from make_constant import Make_Constant
class DrumPattern:
    
    def generatePatterns(style):

        beatA, beatB, beatC = Make_Beat.make(style)
        engineA, engineB, engineC = Make_Engine.make(style)
        constantA, constantB, constantC = Make_Constant.make(style)

        drumPatternA = DrumPattern.joinPattern(beatA, engineA, constantA)
        drumPatternB = DrumPattern.joinPattern(beatA, engineB, constantB)
        drumPatternC = DrumPattern.joinPattern(beatB, engineC, constantA)

        return drumPatternA, drumPatternB, drumPatternC

    def joinPattern(b, e, a):
        pattern = []
        for i in range(len(b)):
            if b[i] != 0:
                pattern.append({"note": b[i], "start_time": 0.25 * i, "duration": 0.25})
        for i in range(len(e)):
            if e[i] != 0:
                pattern.append({"note": e[i], "start_time": 0.25 * i, "duration": 0.25})
        for i in range(len(a)):
            if a[i] != 0:
                pattern.append({"note": a[i], "start_time": 0.25 * i, "duration": 0.25})
        
        return pattern