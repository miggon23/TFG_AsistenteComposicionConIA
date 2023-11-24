from make_line import Make_Line
class BasslinePattern:
    
    def generatePatterns():

        lineA, lineB, lineC, lineD = Make_Line.make()

        return [lineA, lineB, lineC, lineD]

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