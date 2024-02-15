from note_seq import NoteSequence, midi_io

#QPM estandar para pasar a MIDI (1 negra por segundo)
QPM = 60

#Valor estandar de un step, para normalizar
STEP_VALUE = 1/4

MAX_SILENCE_STEPS = 8
MAX_SILENCE_SECONDS = 2

#Serializa una nota en formato "pitch_duracion" y devuelve la string serializada
def serialize_note(note):
    ser_note = str(note.pitch) + "_" +  str(note.quantized_end_step - note.quantized_start_step)

    return ser_note

#Deserializa una secuencia de notas en formato "pitch_duracion" y devuelve el NoteSequence correspondiente
def deserialize_noteseq(note_list):
    start_time = 0

    ns = NoteSequence()
    for ser_note in note_list:
        #deserializacion del pitch y duracion
        data = ser_note.split('_')
        pitch = int(data[0])
        duration = float(data[1])

        #cap de maxima duracion de silencios
        if  (pitch == 0):
            duration = min(duration, MAX_SILENCE_STEPS)
        
        #a partir de la duracion obtenemos el end_time
        end_time = start_time + duration

        if (pitch != 0):
            #añadimos la nota al NoteSequence
            note = NoteSequence.Note(pitch=pitch, velocity=100)
            
            note.quantized_start_step = int(start_time)
            note.quantized_end_step = int(end_time)

            note.start_time = (start_time * STEP_VALUE) * (60.0 / QPM)
            note.end_time = (end_time * STEP_VALUE) * (60.0 / QPM)

            ns.notes.append(note)
        
        #el start_time de la siguiente nota es el end_time de la anterior
        start_time = end_time

    return ns

def save_to_midi(noteseq, output):
    midi_io.sequence_proto_to_midi_file(noteseq, output)