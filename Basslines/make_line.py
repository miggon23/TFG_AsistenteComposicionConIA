import random

class Make_Line:

    def make():
        lineA = [0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0]
        lineB = [0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0]
        lineC = [0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0]
        lineD = [0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0]

        # Aleatorización
        division, replace1, replace2, replacefirst, rRithm = Make_Line.randomize()
        
        # Un compás
        lineA = Make_Line.line(lineA, division, replace1, replace2, replacefirst, rRithm)
        
        # Un compás ligeramente variado respecto del primero generado
        division, replace1, replace2, replacefirst, rRithm = Make_Line.variate(division, replace1, replace2, replacefirst, rRithm)
        lineB = Make_Line.line(lineB, division, replace1, replace2, replacefirst, rRithm)

        # Otro compás ligeramente variado respecto del primero generado
        division, replace1, replace2, replacefirst, rRithm = Make_Line.variate(division, replace1, replace2, replacefirst, rRithm)
        lineC = Make_Line.line(lineC, division, replace1, replace2, replacefirst, rRithm)
       
        # Otro compás ligeramente variado respecto del primero generado
        division, replace1, replace2, replacefirst, rRithm = Make_Line.variate(division, replace1, replace2, replacefirst, rRithm)
        lineD = Make_Line.line(lineD, division, replace1, replace2, replacefirst, rRithm)
       
        return lineA, lineB, lineC, lineD
        
    def randomize():
        division = random.randint(1,2)
        if(random.randint(1,4) <= 1):
            division = 4

        replace1 = (random.randint(1,10) <= 2)
        replace2 = (random.randint(1,10) <= 2)
        replacefirst = (random.randint(1,10) <= 4)

        rRithm = random.randint(1,10)

        return division, replace1, replace2, replacefirst, rRithm
    
    def variate(division, replace1, replace2, replacefirst, rRithm):
        variation = random.randint(1,5)
        if(variation == 1): 
            if(division != 1):
                division = 1
            else:
                division = random.randint(1,2) * 2
        elif(variation == 2): 
            replace1 = not replace1
        elif(variation == 3): 
            replace2 = not replace2
        elif(variation == 4): 
            replacefirst = not replacefirst
        elif(variation == 5): 
            rRithm = random.randint(1,10)
        return division, replace1, replace2, replacefirst, rRithm

    def line(list, division, replace1, replace2, replacefirst, rRithm):
        
        for j in range(16):
            list[j] = -1

        if(division == 1):
            list[0] = 1
        elif(division == 2):
            list[0] = 1
            list[8] = 1
        elif(division == 4):
            list[0] = 1
            list[4] = 1
            list[8] = 1
            list[12] = 1
        
        i = -1

        if(replace1):
            i = 4
        if(replace2):
            if(replacefirst):
                i = 8
            else:
                i = 12    

        if(i >= 0):
            if(rRithm == 1):
                list[i] = 3
                list[i+1] = 0
                list[i+2] = 0
                list[i+3] = 0
            if(rRithm == 2):
                list[i] = 5
                list[i+1] = 0
                list[i+2] = 0
                list[i+3] = 0
            if(rRithm == 3):
                list[i] = 3
                list[i+1] = 0
                list[i+2] = 3
                list[i+3] = 0
            if(rRithm == 4):
                list[i] = 3
                list[i+1] = 0
                list[i+2] = 5
                list[i+3] = 0
            if(rRithm == 5):
                list[i] = 1
                list[i+1] = 0
                list[i+2] = 3
                list[i+3] = 0
            if(rRithm == 6):
                list[i] = 5
                list[i+1] = 0
                list[i+2] = 3
                list[i+3] = 0
            if(rRithm == 7):
                list[i] = 4
                list[i+1] = 3
                list[i+2] = 2
                list[i+3] = 1
            if(rRithm == 8):
                list[i] = 3
                list[i+1] = 0
                list[i+2] = 1
                list[i+3] = 0
            if(rRithm == 9):
                list[i] = 1
                list[i+1] = 0
                list[i+2] = 5
                list[i+3] = 0
            if(rRithm == 10):
                list[i] = 1
                list[i+1] = 5
                list[i+2] = 1
                list[i+3] = 3


        return list