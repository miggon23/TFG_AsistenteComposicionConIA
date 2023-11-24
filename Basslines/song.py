'''
Reformatea la representación de la canción para que sea más fácil de operar para los diferentes algoritmos:
    song[tick] = (note_on[], note_off[])
'''
def spread_song(song):
    spreadSong = {}

    for note in song:

        key = note['start_time']

        for i in range(2):
            if key not in spreadSong:
                spreadSong[key] = ([],[])
            spreadSong[key][i].append(note['note'])

            key += note['duration']

    return dict(sorted(spreadSong.items()))


