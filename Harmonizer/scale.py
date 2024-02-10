import interval as Interval
import note as Note

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

    def create_degrees(self):

        self.degrees = []

        lastScale = self.scale

        for _ in range(len(self.scale) - 1):
         
            firstInterval = lastScale[1].semitones
            degree = []

            for i in lastScale[1:]:
                degree.append(i.semitones - firstInterval)
            degree.append(12 - firstInterval)

            scale = Scale(degree)
            self.degrees.append(scale)
            lastScale = scale.scale

    def absolutize_scale(self, tonic):
        
        self.absolutizedScale = []

        allNotes = ['A', 'B', 'C', 'D', 'E', 'F', 'G']
        allSounds = ['A', ' ', 'B', 'C', ' ', 'D', ' ', 'E', 'F', ' ', 'G', ' ']

        noteIdx = allNotes.index(tonic.name[0])

        extraSemitones = len(tonic.name) - 1
        if extraSemitones > 0 and tonic.name[-1] == 'b':
                extraSemitones *= - 1

        soundIdx = (allSounds.index(tonic.name[0]) + extraSemitones + 12) % 12


        for interval in self.scale:

            noteName = allNotes[(int(interval.get_name()[-1]) - 1 + noteIdx) % 7]


            srcIdx = (soundIdx + interval.semitones) % 12
            dstIdx = allSounds.index(noteName)

            if srcIdx != dstIdx:
                flatDist = (dstIdx - srcIdx + 12) % 12
                sharpDist = (srcIdx - dstIdx + 12) % 12               

                if flatDist <= sharpDist:
                    noteName += flatDist * "b"
                else:
                    noteName += sharpDist * "#"            

            self.absolutizedScale.append(Note.Note(noteName))

    
    def copy(self):
        
        semitones = []

        for interval in self.scale:
            semitones.append(interval.semitones)

        return Scale(semitones)      

    def print_scale(self):      

        for i in self.scale:
            print(i.get_name() + " ", end='')
        print()

    def print_degrees(self):

        print(end="1: ")
        self.print_scale()

        idx = 1
        for s in self.degrees:
            print(self.scale[idx].get_name(), end=": ")
            s.print_scale()
            idx += 1

    def print_absolutized_scale(self):

        for note in self.absolutizedScale:
            print(f"{note.name} ", end="")
        print()
    
    def len(self):
        return len(self.scale)

    def contains(self, scale, degreeIdx = 0):
        
        if degreeIdx == 0:
            return self.__contains(scale)
        else:
            return self.degrees[degreeIdx - 1].__contains(scale)

    def __contains(self, scale):

        ids = 0
        idc = 0

        while ids < len(self.scale) and idc < len(scale.scale):

            if self.scale[ids] == scale.scale[idc]:
                idc += 1
            ids += 1

        return idc == len(scale.scale)
    
    




