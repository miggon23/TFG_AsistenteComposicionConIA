import mido
import song

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

    spread_song = song.note_seq(note_list)
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
            track.append(mido.Message('note_off', note=notes[1][y_init],channel=9, velocity=64, time=midi_events[idx]))
            y_init = 1
        elif (notes[0]):
            track.append(mido.Message('note_on', note=notes[0][x_init],channel=9, velocity=64, time=midi_events[idx]))
            x_init = 1
            
        for note in notes[1][y_init:]:
            track.append(mido.Message('note_off', note=note, channel=9, velocity=64, time=0))
        for note in notes[0][x_init:]:
            track.append(mido.Message('note_on', note=note,channel=9, velocity=64, time=0))
        
        idx += 1

    mid.save(midi_file_path)

def write_midi_song_drums(midi_file_path, note_list):

    # Crear un nuevo archivo MIDI
    mid = mido.MidiFile()

    # Crear una pista MIDI
    track = mido.MidiTrack()
    mid.tracks.append(track)

    # Configurar el tiempo en el archivo MIDI (puedes ajustar esto según tus necesidades)
    ticks_per_beat = 480
    track.append(mido.MetaMessage('time_signature', numerator=4, denominator=4, clocks_per_click=24, notated_32nd_notes_per_beat=8))
    track.append(mido.MetaMessage('set_tempo', tempo=500000))  # Tempo en microsegundos por negra (cambia según tus necesidades)

    spread_song = song.note_seq(note_list)
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
            vel = 45
            if (notes[1][y_init] == 36):
                vel = 120
            elif (notes[1][y_init] == 38 or notes[1][y_init] == 40):
                vel = 100
            track.append(mido.Message('note_off', note=notes[1][y_init],channel=9, velocity=vel, time=midi_events[idx]))
            y_init = 1
        elif (notes[0]):
            vel = 45
            if (notes[0][x_init] == 36):
                vel = 120
            elif (notes[0][x_init] == 38 or notes[0][x_init] == 40):
                vel = 100
            track.append(mido.Message('note_on', note=notes[0][x_init],channel=9, velocity=vel, time=midi_events[idx]))
            x_init = 1
            
        for note in notes[1][y_init:]:
            vel = 45
            if (note == 36):
                vel = 120
            elif (note == 38 or note == 40):
                vel = 100
            track.append(mido.Message('note_off', note=note, channel=9, velocity=vel, time=0))
        for note in notes[0][x_init:]:
            vel = 45
            if (note == 36):
                vel = 120
            elif (note == 38 or note == 40):
                vel = 100
            track.append(mido.Message('note_on', note=note,channel=9, velocity=vel, time=0))
        
        idx += 1

    mid.save(midi_file_path)