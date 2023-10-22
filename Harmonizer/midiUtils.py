import mido

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

def read_midi_song(midi_file_path, output_file):
    song = []  # Lista para almacenar las notas (tono, duración, tiempo de inicio)

    try:
        midi_file = mido.MidiFile(midi_file_path)
        
        current_time = 0  # Variable para rastrear el tiempo actual
        for track in midi_file.tracks:
            for msg in track:
                current_time += msg.time

                if msg.type == 'note_on':
                    note = {
                        'pitch': msg.note,        # Tono de la nota
                        'start_time': current_time,  # Tiempo de inicio
                        'duration': 0           # Duración inicial (se actualizará en 'note_off')                        
                    }
                    song.append(note)

                elif msg.type == 'note_off':
                    # Buscar la nota correspondiente en la lista y actualizar su duración
                    for note in reversed(song):
                        if note['pitch'] == msg.note:
                            note['duration'] = current_time - note['start_time']
                            break

        # Imprimir las notas extraídas
        with open(output_file, 'w') as f:           
            for note in song:
                f.write(f"Pitch: {note['pitch']}, Start Time: {note['start_time']}, Duration: {note['duration']}\n")

        return song

    except Exception as e:
        print(f"Error: {e}")
        return []
    

    
def make_midi_song(midi_file_path, song):

    # Crear un nuevo archivo MIDI
    mid = mido.MidiFile()

    # Crear una pista MIDI
    track = mido.MidiTrack()
    mid.tracks.append(track)

    # Configurar el tiempo en el archivo MIDI (puedes ajustar esto según tus necesidades)
    ticks_per_beat = 480
    track.append(mido.MetaMessage('time_signature', numerator=4, denominator=4, clocks_per_click=24, notated_32nd_notes_per_beat=8))
    track.append(mido.MetaMessage('set_tempo', tempo=500000))  # Tempo en microsegundos por negra (cambia según tus necesidades)

    song = [
        {"pitch": 1, "start_time": 0.25, "duration": 8.0},
        {"pitch": 60, "start_time": 0.75, "duration": 1.0},
        {"pitch": 62, "start_time": 1.5, "duration": 0.5},
        {"pitch": 65, "start_time": 1.5, "duration": 0.5},
        {"pitch": 66, "start_time": 1.5, "duration": 0.5},
        {"pitch": 67, "start_time": 1.75, "duration": 0.5},
        {"pitch": 59, "start_time": 1.5, "duration": 34.5},
        {"pitch": 64, "start_time": 2, "duration": 0.5},
        {"pitch": 61, "start_time": 0.5, "duration": 4},
    ]

    spread_song = {}
    first_note_tick = song[0]["start_time"]

    for item in song:

        key = item['start_time']
        first_note_tick = min(first_note_tick, key)

        if key in spread_song:
            spread_song[key].append(item['pitch'])
        else:
            spread_song[key] = [item['pitch']]

        key += item['duration']

        if key in spread_song:
            spread_song[key].append(-item['pitch'])
        else:
            spread_song[key] = [-item['pitch']]


    spread_song = dict(sorted(spread_song.items()))

    midi_events = [int(first_note_tick * ticks_per_beat)]
    last_tick = first_note_tick

    for tick in list(spread_song.keys())[1:]:
        midi_events.append(int((tick - last_tick) * ticks_per_beat))
        last_tick = tick

    print(midi_events) 
    print(spread_song)  

    idx = 0
    for tick, notes in spread_song.items():

        if (notes[0] > 0):
            track.append(mido.Message('note_on', note=notes[0], velocity=64, time=midi_events[idx]))
        elif (notes[0] < 0):
            track.append(mido.Message('note_off', note=-notes[0], velocity=64, time=midi_events[idx]))
        idx += 1

        for note in notes[1:]:

            if (note > 0):
                track.append(mido.Message('note_on', note=note, velocity=64, time=0))
            elif (note < 0):
                track.append(mido.Message('note_off', note=-note, velocity=64, time=0))

    # Guardar el archivo MIDI
    mid.save(midi_file_path)