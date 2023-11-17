import mido
import Song

def debug_midi_file(midi_file_path, output_file):
    
    midi_file = mido.MidiFile(midi_file_path)
    with open(output_file, 'w') as f:
        for i, track in enumerate(midi_file.tracks):
            f.write(f"Track {i}:\n")
            for msg in track:
                f.write(str(msg) + '\n')

def read_midi_song(midi_file_path):

    midi_file = mido.MidiFile(midi_file_path)  

    notes = []     

    current_time = 0

    for track in midi_file.tracks:
        for msg in track:

            msgType = msg.type 
            if msgType == 'note_on' or msgType == 'note_off':

                if msgType == 'note_on' and msg.velocity == 0:
                    msgType = 'note_off'

                current_time += msg.time / midi_file.ticks_per_beat

                notes.append({
                    'type': msgType, 
                    'note': msg.note, 
                    'time': current_time
                })

    song = []

    for note in notes:

        if note['type'] == 'note_on':

            song.append({
                'note': note['note'], 
                'start_time': note['time'], 
                'duration': -1
            })

        elif note['type'] == 'note_off':

            for previousNote in reversed(song):
                if previousNote['note'] == note['note'] and previousNote['duration'] == -1:
                    previousNote['duration'] = note['time'] - previousNote['start_time']
                    break 

    return song

def write_midi_song(midi_file_path, note_list):

    # Crear un nuevo archivo MIDI
    mid = mido.MidiFile()

    # Crear una pista MIDI
    track = mido.MidiTrack()
    mid.tracks.append(track)

    # Configurar el tiempo en el archivo MIDI (puedes ajustar esto según tus necesidades)
    ticks_per_beat = 480
    track.append(mido.MetaMessage('time_signature', numerator=4, denominator=4, clocks_per_click=24, notated_32nd_notes_per_beat=8))
    track.append(mido.MetaMessage('set_tempo', tempo=500000))  # Tempo en microsegundos por negra (cambia según tus necesidades)

    spread_song = Song.spread_song(note_list)
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