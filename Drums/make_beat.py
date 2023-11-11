from enums import Style
from enums import Note
import random

class Make_Beat:

    def make(style):
        beat1 = [0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0]
        beat2 = [0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0]
        beat3 = [0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0]

        # Aleatorización
        skipped, delayed, delayedN, rushed, rushedN, double1, double1N, double2, double2N = Make_Beat.randomize()
        
        # Un compás
        beat1 = Make_Beat.beat(beat1, style, skipped, delayed, delayedN, rushed, rushedN, double1, double1N, double2, double2N)
        
        # Un compás ligeramente variado respecto del primero generado
        skippedVar, delayedVar, delayedNVar, rushedVar, double1Var, double2Var = Make_Beat.variate(skipped, delayed, delayedN, rushed, double1, double2)
        beat2 = Make_Beat.beat(beat2, style, skippedVar, delayedVar, delayedNVar, rushedVar, rushedN, double1Var, double1N, double2Var, double2N)

        # Otro compás ligeramente variado respecto del primero generado
        skippedVar, delayedVar, delayedNVar, rushedVar, double1Var, double2Var = Make_Beat.variate(skipped, delayed, delayedN, rushed, double1, double2)
        beat3 = Make_Beat.beat(beat3, style, skippedVar, delayedVar, delayedNVar, rushedVar, rushedN, double1Var, double1N, double2Var, double2N)
       
        return beat1, beat2, beat3
        
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

    def beat(list, style, skipped, delayed, delayedN, rushed, rushedN, double1, double1N, double2, double2N):
        if(style == Style.BASIC or style == Style.KICK or style == Style.CLAP):
            i = 0
            list[i] = Note.BassDrum.value
            if double1: list[i + double1N] = Note.BassDrum.value
            i = 8
            if not skipped:
                if delayed: i += delayedN
                elif rushed: i -= rushedN
                list[i] = Note.BassDrum.value
                if double2: list[i + double2N] = Note.BassDrum.value

        elif(style == Style.SHAKER):
            for i in range(2):
                j = (i-1)*4
                list[j] = Note.ClosedHiHat.value
                if double1: 
                    list[j + double1N] = Note.ClosedHiHat.value
                j = (i-1)*4 + 8
                if not skipped:
                    if delayed: j += delayedN
                    elif rushed: j -= rushedN
                    list[j] = Note.BassDrum.value
                    if double2: list[j + double2N] = Note.BassDrum.value

        elif(style == Style.JAZZ):
            i = 0
            list[i] = Note.OpenHiHat.value
            if double1: list[i + double1N] = Note.OpenHiHat.value
            i = 8
            if not skipped:
                if delayed: i += delayedN
                elif rushed: i -= rushedN
                list[i] = Note.OpenHiHat.value
                if double2: list[i + double2N] = Note.OpenHiHat.value

        elif(style == Style.DISCO):
            for i in range(4):
                j = (i-1)*4
                list[j] = Note.BassDrum.value

        elif(style == Style.METAL):
            for i in range(2):
                j = (i-1)*4
                list[j] = Note.ClosedHiHat.value
                if double1: 
                    list[j + double1N] = Note.ClosedHiHat.value
                j = (i-1)*4 + 8
                if not skipped:
                    if delayed: j += delayedN
                    elif rushed: j -= rushedN
                    list[j] = Note.ClosedHiHat.value
                    if double2: list[j + double2N] = Note.ClosedHiHat.value

        elif(style == Style.LATIN):
            i = 0
            list[i] = Note.BassDrum.value
            if double1: list[i + double1N] = Note.BassDrum.value
            i = 6
            if not skipped:
                if delayed: i += delayedN
                elif rushed: i -= rushedN
                list[i] = Note.BassDrum.value
            i = 8
            list[i] = Note.BassDrum.value
            if double2: list[i + double1N] = Note.BassDrum.value
            i = 14
            list[i] = Note.BassDrum.value

        elif(style == Style.ROCK):
            for i in range(2):
                j = (i-1)*4
                list[j] = Note.AcousticSnare.value
                if double1: 
                    list[j + double1N] = Note.AcousticSnare.value
                j = (i-1)*4 + 8
                if not skipped:
                    if delayed: j += delayedN
                    elif rushed: j -= rushedN
                    list[j] = Note.AcousticSnare.value
                    if double2: list[j + double2N] = Note.AcousticSnare.value
                    
        return list
    
