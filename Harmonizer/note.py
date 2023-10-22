notes_pitch = {
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


class Note:

    def __init__(self, note, octave = 0):
        self.pitch = notes_pitch[note] + 12 * octave