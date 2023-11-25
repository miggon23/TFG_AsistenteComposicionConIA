name_pitch = {
    "C": 0,
    "C#": 1,
    "Db": 1,  
    "D": 2,
    "D#": 3,
    "Eb": 3,
    "E": 4,
    "F": 5,
    "F#": 6,
    "Gb": 6,
    "G": 7,
    "G#": 8,
    "Ab": 8,
    "A": 9,
    "A#": 10,
    "Bb": 10,
    "B": 11,
}

def get_pitch(interval, tonic, octave):
        return tonic.pitch + interval.semitones + 12 * octave

def get_nearest_pitch(interval, tonic, meanPitch):
    
    pitch = (tonic.pitch + interval.semitones) % 12

    octave = int(meanPitch / 12)

    if pitch + octave * 12 > meanPitch:
        octave -= 1

    lowerPitch = pitch + octave * 12
    higherPitch = pitch + (octave + 1) * 12

    if meanPitch - lowerPitch < higherPitch - meanPitch:
        return lowerPitch
    else:
        return higherPitch


class Note:

    def __init__(self, note):
        
        if type(note) == int:

            self.pitch = note

            for name, pitch in reversed(name_pitch.items()):
                if pitch == self.pitch % 12:
                    self.name = name
                
        else:

            extraSemitones = 0
            for alteration in note[1:]:
                if alteration == 'b':
                    extraSemitones -= 1
                elif alteration == '#':
                    extraSemitones += 1
                else:
                    raise Exception("La nota tiene un nombre incorrecto")
                 
            self.pitch = (name_pitch[note[0]] + extraSemitones + 12) % 12
            self.name = note[0]

            if extraSemitones > 0:
                self.name += extraSemitones * '#'
            elif extraSemitones < 0:
                self.name += (extraSemitones * -1) * 'b'


        
            

    