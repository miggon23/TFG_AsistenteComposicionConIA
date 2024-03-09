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

def json_to_serialized(noteSeq_json):
    serialized_notes = []

    last_end = 0

    for note in noteSeq_json['notes']:
        # hay un silencio lo codificamos como pitch 0
        if (note['quantizedStartStep'] != last_end):
            silence_dur = note['quantizedStartStep'] - last_end
            silence = "0_" + str(silence_dur)
            serialized_notes.append(silence)

        # serializamos la nota en formato pitch_dur
        note_dur = note['quantizedEndStep'] - note['quantizedStartStep']
        note_ser = str(note['pitch']) + "_" + str(note_dur)
        serialized_notes.append(note_ser)

    return serialized_notes

def json_to_noteSeq(noteSeq_json):
    ns = NoteSequence()
    
    for json_note in noteSeq_json['notes']:
        pitch = json_note['pitch']
        if (pitch != 0):
            #añadimos la nota al NoteSequence
            note = NoteSequence.Note(pitch=pitch, velocity=100)

            note.quantized_start_step = int(json_note['quantizedStartStep'])
            note.quantized_end_step = int(json_note['quantizedEndStep'])

            note.start_time = (int(json_note['quantizedStartStep']) * STEP_VALUE) * (60.0 / QPM)
            note.end_time = (int(json_note['quantizedEndStep']) * STEP_VALUE) * (60.0 / QPM)

            ns.notes.append(note)

    return ns

def save_to_midi(noteseq, output):
    midi_io.sequence_proto_to_midi_file(noteseq, output)