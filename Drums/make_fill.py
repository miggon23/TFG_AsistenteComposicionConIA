from enums import Style
from enums import Note
import random

class Make_fill:

    def make(style, lvl):
        list = [0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0]
        for i in range(lvl):
            list = Make_fill.fill(list, style)
        return list
        
    
    def fill(list, style):
        i1 = random.randint(0,15)
        i2 = random.randint(8,15)
        i3 = random.randint(12,15)

        if(style == Style.BASIC):
            list[i1] = Note.OpenHiHat.value
            list[i2] = Note.AcousticSnare.value
            list[i3] = Note.CrashCymbal.value

        if(style == Style.KICK):
            list[i1] = Note.BassDrum.value
            list[i2] = Note.BassDrum.value
            list[i3] = Note.BassDrum.value

        if(style == Style.CLAP):
            list[i1] = Note.AcousticClap.value
            list[i2] = Note.AcousticClap.value
            list[i3] = Note.AcousticClap.value

        if(style == Style.SHAKER):
            list[i1] = Note.ClosedHiHat.value
            list[i2] = Note.ClosedHiHat.value
            list[i3] = Note.ClosedHiHat.value

        if(style == Style.JAZZ):
            list[i1] = Note.OpenHiHat.value
            list[i2] = Note.ClosedHiHat.value
            list[i3] = Note.OpenHiHat.value

        if(style == Style.DISCO):
            list[i1] = Note.BassDrum.value
            list[i2] = Note.ElectricSnare.value
            list[i3] = Note.BassDrum.value

        if(style == Style.METAL):
            list[i1] = Note.AcousticSnare.value
            list[i2] = Note.AcousticSnare.value
            list[i3] = Note.AcousticSnare.value

        if(style == Style.LATIN):
            list[i1] = Note.HighTom.value
            list[i2] = Note.HiMidTom.value
            list[i3] = Note.HighTom.value

        if(style == Style.ROCK):
            list[i1] = Note.LowTom.value
            list[i2] = Note.HiMidTom.value
            list[i3] = Note.LowMidTom.value
    
        return list
    
