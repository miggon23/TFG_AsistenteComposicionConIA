from enums import Style
from enums import Note
import random

class Make_Engine:

    def make(style):
        engine1 = [0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0]
        engine2 = [0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0]
        engine3 = [0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0]

        # Aleatorización
        skipped, delayed, delayedN, rushed, rushedN, double1, double1N, double2, double2N = Make_Engine.randomize()
        
        # Un compás
        engine1 = Make_Engine.engine(engine1, style, skipped, delayed, delayedN, rushed, rushedN, double1, double1N, double2, double2N)
        
        # Un compás ligeramente variado respecto del primero generado
        skippedVar, delayedVar, delayedNVar, rushedVar, double1Var, double2Var = Make_Engine.variate(skipped, delayed, delayedN, rushed, double1, double2)
        engine2 = Make_Engine.engine(engine2, style, skippedVar, delayedVar, delayedNVar, rushedVar, rushedN, double1Var, double1N, double2Var, double2N)

        # Otro compás ligeramente variado respecto del primero generado
        skippedVar, delayedVar, delayedNVar, rushedVar, double1Var, double2Var = Make_Engine.variate(skipped, delayed, delayedN, rushed, double1, double2)
        engine3 = Make_Engine.engine(engine3, style, skippedVar, delayedVar, delayedNVar, rushedVar, rushedN, double1Var, double1N, double2Var, double2N)
       
        return engine1, engine2, engine3
        
    def randomize():
        skipped = (random.randint(1,10) <= 1)
        delayed = (random.randint(1,10) <= 3)
        delayedN = random.randint(1,3)
        rushed = False
        if not delayed:
            rushed = (random.randint(1,10) <= 2)
        rushedN = random.randint(1,3)
        double1 = (random.randint(1,10) <= 2)
        double1N = random.randint(1,2)
        double2 = (random.randint(1,10) <= 4)
        double2N = random.randint(1,2)
        return skipped, delayed, delayedN, rushed, rushedN, double1, double1N, double2, double2N
    
    def variate(skipped, delayed, delayedN, rushed, double1, double2):
        variation = random.randint(1,5)
        if(variation == 1): skipped = not skipped
        elif(variation == 2): 
            delayed = not delayed
            rushed = not rushed 
        elif(variation == 3): 
            rushed = not rushed 
            delayedN += 1
        elif(variation == 4): double1 = not double1
        elif(variation == 5): double2 = not double2
        return skipped, delayed, delayedN, rushed, double1, double2

    def engine(list, style, skipped, delayed, delayedN, rushed, rushedN, double1, double1N, double2, double2N):
        if(style == Style.BASIC or style == Style.CLAP or style == Style.METAL):
            i = 4
            list[i] = Note.AcousticSnare.value
            if double1: list[i + double1N] = Note.AcousticSnare.value
            i = 12
            if not skipped:
                if delayed: i += 1
                elif rushed: i -= rushedN
                list[i] = Note.AcousticSnare.value
                if double2: list[i + double2N] = Note.AcousticSnare.value

        # En Style.KICK y en Style.SHAKER no hay engine

        elif(style == Style.JAZZ):
            i = 4
            list[i] = Note.PedalHiHat.value
            if double1: list[i + double1N] = Note.PedalHiHat.value
            i = 12
            if not skipped:
                if delayed: i += delayedN
                elif rushed: i -= rushedN
                list[i] = Note.PedalHiHat.value
                if double2: list[i + double2N] = Note.PedalHiHat.value

        elif(style == Style.DISCO):
            for i in range(4):
                j = (i-1)*4 + 2
                list[j] = Note.ElectricSnare.value

        elif(style == Style.LATIN):
            i = 0
            if(random.randint(1,2)==1):
                list[i] = Note.OpenHiHat.value

            i = 6
            if delayed: i += delayedN
            elif rushed: i -= rushedN
            list[i] = Note.OpenHiHat.value
            if double1: list[i + double1N] = Note.OpenHiHat.value

            i = 12
            if delayed: i += delayedN
            elif rushed: i -= rushedN
            list[i] = Note.OpenHiHat.value
            if double2: list[i + double2N] = Note.OpenHiHat.value

        elif(style == Style.ROCK):
            i = 0
            list[i] = Note.BassDrum.value
            i = 10
            if not skipped:
                if delayed: i += delayedN
                elif rushed: i -= rushedN
                list[i] = Note.BassDrum.value
                if double1: list[i + double1N] = Note.BassDrum.value
            i = 14
            if not skipped:
                if rushed: i -= rushedN
                list[i] = Note.BassDrum.value
                if double2: list[i - double2N] = Note.BassDrum.value
                    
        return list