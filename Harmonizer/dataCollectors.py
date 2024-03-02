import pandas as pd
import song
import interval as Interval
import harmony as Harmony

def seave_all(song, filePath):
        save_matrix(song, filePath + ".xlsx")
        save_raw(song, filePath + ".csv")

def save_raw(song, filePath):

    try:
        df = pd.read_csv(filePath)  
        data = {'chord': [], 'duration': []}       
    except FileNotFoundError:
        df = pd.DataFrame(columns=['chord', 'duration'])
        data = {'chord': ["start_end"], 'duration': [0]} 

    for chordInfo in song.bestChords:

        chord = chordInfo[0]
        if chord is not None:
            chord = chord[0] + "_" + chord[1]
            duration = chordInfo[1]

            data['chord'].append(chord)
            data['duration'].append(duration)

    data['chord'].append("start_end")
    data['duration'].append(0)       

    df = pd.concat([df, pd.DataFrame(data)], ignore_index=True)
    df.to_csv(filePath, index=False)

def save_matrix(song, filePath):

    lastChord = "start_end"

    try:
        df = pd.read_excel(filePath, index_col=0)
    except FileNotFoundError:
        initialData = {lastChord: [0]}
        df = pd.DataFrame(initialData, index=[lastChord])

    reorganize = False

    for chordInfo in song.bestChords:

        chord = chordInfo[0]
        if chord is not None:
            chord = chord[0] + "_" + chord[1]

            if chord not in df.index:
                df[chord] = 0
                df.loc[chord] = 0
                reorganize = True

            df.at[lastChord, chord] += 1

            lastChord = chord

    df.at[lastChord, "start_end"] += 1

    if reorganize:  

        def foo(chord):
            chord = str(chord)
            if chord == "start_end":
                return -1
            else:
                degree, chordName = chord.split("_")
                v1 = Interval.intervals.index(degree)
                v2 = list(Harmony.allChords.keys()).index(chordName)
                return v1 * len(Harmony.allChords) + v2

        indexes = sorted(df.index.tolist(), key=foo)
        df = df.reindex(index=indexes, columns=indexes)       

    df.to_excel(filePath)