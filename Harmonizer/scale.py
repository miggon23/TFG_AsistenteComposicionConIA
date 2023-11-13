import Interval

class Scale:

    def __init__(self, intervals, checker = True):

        if type(intervals) == str:
            intervals = intervals.split()
   
        nextInterval = Interval.Interval(intervals[0])
        if checker and not nextInterval.is_tonic():
            raise Exception("Escala mal construida")
        
        self.scale = [nextInterval]
        idx = 0
        
        for i in intervals[1:]:
            nextInterval = Interval.Interval(i)
            if checker and nextInterval <= self.scale[idx]:
                raise Exception("Escala mal construida")
            self.scale.append(nextInterval)
            idx += 1

        self.degrees = []

    def create_degrees(self):

        if len(self.degrees) > 0:
            return

        lastScale = self.scale

        for n in range(len(self.scale) - 1):
         
            firstInterval = lastScale[1].semitones
            degree = []

            for i in lastScale[1:]:
                degree.append(i.semitones - firstInterval)
            degree.append(12 - firstInterval)

            s = Scale(degree)
            self.degrees.append(s)
            lastScale = s.scale

    def len(self):
        return len(self.scale)
    
    def copy_scale(self):
        
        semitones = []

        for interval in self.scale:
            semitones.append(interval.semitones)

        return Scale(semitones)      

    def print_scale(self):      
        for i in self.scale:
            print(i.get_interval() + " ", end='')
        print()

    def print_degrees(self):

        print(end="1: ")
        self.print_scale()

        idx = 1
        for s in self.degrees:
            print(self.scale[idx].get_interval(), end=": ")
            s.print_scale()
            idx += 1

    def contains(self, chord, degreeIdx = 0):
        
        if degreeIdx == 0:
            return self.__contains(chord)
        else:
            return self.degrees[degreeIdx - 1].__contains(chord)

    def __contains(self, chord):

        ids = 0
        idc = 0

        while ids < len(self.scale) and idc < len(chord.scale):

            if self.scale[ids] == chord.scale[idc]:
                idc += 1
            ids += 1

        return idc == len(chord.scale)
    
    




