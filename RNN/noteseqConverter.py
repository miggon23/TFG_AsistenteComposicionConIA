from note_seq import NoteSequence, midi_io

#Serializa una nota en formato "pitch_duracion" y devuelve la string serializada
def serialize_note(self, note):
    ser_note = ""

    if (self.step_mode):
        ser_note = str(note.pitch) + "_" +  str(note.quantized_end_step - note.quantized_start_step)
    else:
        ser_note = str(note.pitch) + "_" +  str(round(note.end_time - note.start_time, 2))

    return ser_note

#Deserializa una secuencia de notas en formato "pitch_duracion" y devuelve el NoteSequence correspondiente
def deserialize_noteseq(self, note_list):
    start_time = 0

    ns = NoteSequence()
    for ser_note in note_list:
        #deserializacion del pitch y duracion
        data = ser_note.split('_')
        pitch = int(data[0])
        duration = float(data[1])

        #cap de maxima duracion de silencios
        if  (pitch == 0):
            if (self.step_mode):
                duration = min(duration, MAX_SILENCE_STEPS)
            else:
                duration = min(duration, MAX_SILENCE_SECONDS)
        
        #a partir de la duracion obtenemos el end_time
        end_time = start_time + duration

        if (pitch != 0):
            #añadimos la nota al NoteSequence
            note = NoteSequence.Note(pitch=pitch, velocity=100)
            
            if (self.step_mode):
                note.quantized_start_step = int(start_time)
                note.quantized_end_step = int(end_time)

                note.start_time = (start_time * STEP_VALUE) * (60.0 / QPM)
                note.end_time = (end_time * STEP_VALUE) * (60.0 / QPM)
            else:
                note.start_time = start_time
                note.end_time = end_time

            ns.notes.append(note)
        
        #el start_time de la siguiente nota es el end_time de la anterior
        start_time = end_time

    return ns

def save_to_midi(noteseq, output):
    midi_io.sequence_proto_to_midi_file(noteseq, output)