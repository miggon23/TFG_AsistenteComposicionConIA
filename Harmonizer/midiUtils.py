import mido
import song as Song

import mido
import song as Song

def debug_midi_file(midiFilePath, outputFile):
    
    midiFile = mido.MidiFile(midiFilePath)
    with open(outputFile, 'w') as f:
        for i, track in enumerate(midiFile.tracks):
            f.write(f"Track {i}:\n")
            for msg in track:
                f.write(str(msg) + '\n')

def read_midi_song(midiFilePath):

    midiFile = mido.MidiFile(midiFilePath)  

    notes = []     

    current_time = 0

    for track in midiFile.tracks:
        for msg in track:

            msgType = msg.type 
            if msgType == 'note_on' or msgType == 'note_off':

                if msgType == 'note_on' and msg.velocity == 0:
                    msgType = 'note_off'

                current_time += msg.time

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

    return song, midiFile.ticks_per_beat

def write_midi_song(midiFilePath, song, ticksPerBeat):

    # Crear un nuevo archivo MIDI
    mid = mido.MidiFile()
    mid.ticks_per_beat = ticksPerBeat

    # Crear una pista MIDI
    track = mido.MidiTrack()
    mid.tracks.append(track)

    # Configurar el tiempo en el archivo MIDI (puedes ajustar esto según tus necesidades)
    track.append(mido.MetaMessage('set_tempo', tempo = 500000))  # Tempo en microsegundos por negra (cambia según tus necesidades)
    track.append(mido.MetaMessage('time_signature', numerator= 4, denominator=4, clocks_per_click=24, notated_32nd_notes_per_beat=8))

    spread_song = Song.spread_song(song)
    firstNoteTick = next(iter(spread_song))

    midi_events = [firstNoteTick]
    lastTick = firstNoteTick

    for tick in list(spread_song.keys())[1:]:
        midi_events.append(tick - lastTick)
        lastTick = tick

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

    mid.save(midiFilePath)