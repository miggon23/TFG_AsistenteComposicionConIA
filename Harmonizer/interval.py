
intervals = ["1", "b2", "2", "b3", "3", "4", "b5", "5", "b6", "6", "b7", "7"]

class Interval:
    # Constructor de la clase
    def __init__(self, interval):

        if type(interval) == int:
            self.semitones = interval
            self.__check_interval()
            return

        semitones = int(interval[-1])

        if semitones < 1:
            raise Exception("Intervalo incorrecto")
        if semitones == 1:
            semitones = 0
        elif semitones == 2:
            semitones = 2
        elif semitones < 5:
            semitones += 1
        elif semitones < 8:
            semitones += semitones - 3
        else:
            raise Exception("Intervalo incorrecto")

        for accidental in interval[:-1]:
            if accidental == 'b':
                semitones -= 1
            elif accidental == '#':
                semitones += 1
            else:
                raise Exception("Alteraciones mal escritas")      

        self.semitones = semitones
        self.__check_interval()      
        
    def __check_interval(self):
        if self.semitones < 0 or self.semitones > 11:
            raise Exception("Intervalo incorrecto")
    
    def get_name(self):
        return intervals[self.semitones]
    
    def is_tonic(self):
        return self.semitones == 0
    
    def __le__(self, otro):
        if isinstance(otro, Interval):
            return self.semitones <= otro.semitones
    def __eq__(self, otro):
        if isinstance(otro, Interval):
            return self.semitones == otro.semitones



