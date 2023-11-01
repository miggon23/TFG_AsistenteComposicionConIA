from mido import MidiFile, MidiTrack, Message, MetaMessage

def make_midi_drum_song(midi_file_path, drumPattern):
    # Crea un nuevo archivo MIDI
    mid = MidiFile()
    track = MidiTrack()
    mid.tracks.append(track)

    # Configura los parámetros del archivo MIDI
    ticks_per_beat = 480  # Número de ticks por tiempo (puedes ajustar esto según tus necesidades)
    subdivisiones_por_beat = 4  # Para semicorcheas, usa 4 subdivisiones por beat (una subdivisión es una semicorchea)

    # Calcula la duración de una semicorchea en ticks
    ticks_por_subdivision = ticks_per_beat / subdivisiones_por_beat

    # Crea un nuevo archivo MIDI
    mid = MidiFile()
    track = MidiTrack()
    mid.tracks.append(track)

    # Convierte las notas de percusión en mensajes de nota en el archivo MIDI
    for fila in drumPattern:
        print(fila)
        for i, nota in enumerate(fila):
            # Calcula el tiempo en ticks para colocar la nota en la posición de la n semicorchea
            tiempo_en_ticks = int(i * ticks_por_subdivision)
            print(tiempo_en_ticks, i, nota)
            if nota!=0:
                # Convierte el tiempo_en_ticks a entero y crea un mensaje de nota en el canal de percusión (canal 9)
                track.append(Message('note_on', note=nota, velocity=64, channel=9, time=int(tiempo_en_ticks)))
                track.append(Message('note_off', note=nota, velocity=64, channel=9, time=int(tiempo_en_ticks+ticks_por_subdivision)))  # Duración de la semicorchea

    mid.save(midi_file_path)