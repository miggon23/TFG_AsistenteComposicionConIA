from make_beat import Make_Beat
from make_engine import Make_Engine
from make_constant import Make_Constant
from enums import Style
class DrumPattern:
    
    def generatePatterns(style):

        beatA, beatB, beatC = Make_Beat.make(style)
        engineA, engineB, engineC = Make_Engine.make(style)
        constantA, constantB, constantC = Make_Constant.make(style)

        drumPatternA = []
        #drumPatternA.append(beatA)
        #drumPatternA.append(engineA)
        drumPatternA.append(constantA)
        
        drumPatternB = []
        
        drumPatternC = []

        return drumPatternA, drumPatternB, drumPatternC

        