import mido
import song

def read_midi_file(midi_file_path, output_file):
    try:
        midi_file = mido.MidiFile(midi_file_path)
        with open(output_file, 'w') as f:
            for i, track in enumerate(midi_file.tracks):
                f.write(f"Track {i}:\n")
                for msg in track:
                    f.write(str(msg) + '\n')
    except Exception as e:
        print(f"Error: {e}")

def read_midi_song(midi_file_path, output_file = None):
    song = []  # Lista para almacenar las notas (tono, duración, tiempo de inicio)

    try:
        midi_file = mido.MidiFile(midi_file_path)
        
        current_time = 0  # Variable para rastrear el tiempo actual
        for track in midi_file.tracks:
            for msg in track:
                current_time += (msg.time / 96.0)

                if msg.type == 'note_on':
                    note = {
                        'note': msg.note,        # Tono de la nota
                        'start_time': current_time,  # Tiempo de inicio
                        'duration': 0           # Duración inicial (se actualizará en 'note_off')                        
                    }
                    song.append(note)

                elif msg.type == 'note_off':
                    # Buscar la nota correspondiente en la lista y actualizar su duración
                    for note in reversed(song):
                        if note['note'] == msg.note:
                            note['duration'] = current_time - note['start_time']
                            break

        if output_file != None:
            # Imprimir las notas extraídas
            with open(output_file, 'w') as f:           
                for note in song:
                    f.write(f"note: {note['note']}, Start Time: {note['start_time']}, Duration: {note['duration']}\n")

        return song

    except Exception as e:
        print(f"Error: {e}")
        return []
    

def make_midi_song(midi_file_path, note_list):

    # Crear un nuevo archivo MIDI
    mid = mido.MidiFile()

    # Crear una pista MIDI
    track = mido.MidiTrack()
    mid.tracks.append(track)

    # Configurar el tiempo en el archivo MIDI (puedes ajustar esto según tus necesidades)
    ticks_per_beat = 480
    track.append(mido.MetaMessage('time_signature', numerator=4, denominator=4, clocks_per_click=24, notated_32nd_notes_per_beat=8))
    track.append(mido.MetaMessage('set_tempo', tempo=500000))  # Tempo en microsegundos por negra (cambia según tus necesidades)

    spread_song = song.spread_song(note_list)
    first_note_tick = next(iter(spread_song))

    midi_events = [int(first_note_tick * ticks_per_beat)]
    last_tick = first_note_tick

    for tick in list(spread_song.keys())[1:]:
        midi_events.append(int((tick - last_tick) * ticks_per_beat))
        last_tick = tick

    idx = 0
    for tick, notes in spread_song.items():

        x_init = 0
        y_init = 0

        if (notes[1]):
            track.append(mido.Message('note_off', note=notes[1][y_init], velocity=64, time=midi_events[idx]))
            y_init = 1
        elif (notes[0]):
            track.append(mido.Message('note_on', note=notes[0][x_init], velocity=64, time=midi_events[idx]))
            x_init = 1
            
        for note in notes[1][y_init:]:
            track.append(mido.Message('note_off', note=note, velocity=64, time=0))
        for note in notes[0][x_init:]:
            track.append(mido.Message('note_on', note=note, velocity=64, time=0))
        
        idx += 1

    mid.save(midi_file_path)