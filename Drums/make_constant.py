from enums import Style
from enums import Note
import random

class Make_Constant:

    def make(style):
        constant1 = [0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0]
        constant2 = [0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0]
        constant3 = [0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0]

        # Aleatorización
        sixteenth, skipped1, skipped2, skipped3, skipped1N, skipped2N, skipped3N = Make_Constant.randomize()
        
        # Un compás
        constant1 = Make_Constant.constant(constant1, style, sixteenth, skipped1, skipped2, skipped3, skipped1N, skipped2N, skipped3N)
        
        # Un compás ligeramente variado respecto del primero generado
        skipped1, skipped2,skipped3 = Make_Constant.variate(skipped1, skipped2, skipped3)
        constant2 = Make_Constant.constant(constant2, style, sixteenth, skipped1, skipped2, skipped3, skipped1N, skipped2N, skipped3N)

        # Otro compás ligeramente variado respecto del primero generado
        skipped1, skipped2,skipped3 = Make_Constant.variate(skipped1, skipped2, skipped3)
        constant3 = Make_Constant.constant(constant3, style, sixteenth, skipped1, skipped2, skipped3, skipped1N, skipped2N, skipped3N)
       
        return constant1, constant2, constant3
        
    def randomize():
        sixteenth = (random.randint(1,3) <= 1)
        skipped1 = (random.randint(1,10) <= 3)
        skipped2 = (random.randint(1,10) <= 2)
        skipped3 = (random.randint(1,10) <= 1)
        skipped1N = random.randint(0,15)
        skipped2N = random.randint(0,15)
        skipped3N = random.randint(0,15)
        return sixteenth, skipped1, skipped2, skipped3, skipped1N, skipped2N, skipped3N
    
    def variate(skipped1, skipped2,skipped3):
        variation = random.randint(1,3)
        if(variation == 1): skipped1 = not skipped1
        elif(variation == 2): skipped2 = not skipped2
        elif(variation == 3): skipped3 = not skipped3

        return skipped1, skipped2, skipped3

    def constant(list, style, sixteenth, skipped1, skipped2, skipped3, skipped1N, skipped2N, skipped3N):
        if(style.value == Style.BASIC.value or style.value == Style.CLAP.value or style.value == Style.SHAKER.value or style.value == Style.DISCO.value or style.value == Style.LATIN.value or style.value == Style.ROCK.value):
            for i in range(16):
                if(sixteenth or (i%2 == 0)):
                    if not((i == skipped1N and skipped1) or (i == skipped2N and skipped2) or (i == skipped3N and skipped3)):
                        list[i] = Note.ClosedHiHat.value
        
        # En Style.KICK no hay constant
        
        elif(style.value == Style.JAZZ.value):                 
            list[4] = Note.OpenHiHat.value
            list[7] = Note.OpenHiHat.value
            list[12] = Note.OpenHiHat.value
            list[15] = Note.OpenHiHat.value

        elif(style.value == Style.METAL.value):
            for i in range(16):
                if not((i == skipped1N and skipped1) or (i == skipped2N and skipped2) or (i == skipped3N and skipped3)):
                    list[i] = Note.BassDrum.value

        return list
    
