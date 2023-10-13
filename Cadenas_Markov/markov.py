from IPython.display import display
import pandas as pd
from note_seq import NoteSequence

#lee el json line desde la url y lo convierte en dataframe de pandas
df = pd.read_json(path_or_buf="datasets/bach-doodle.jsonl-00001-of-00192.gz", lines=True)

notes_to_train = []

inputs = df["input_sequence"]
for i in range(len(inputs)):
    #
    for j in range(len(inputs[i])):
        #solo nos interesan las notas si el feedback es positivo ("2")
        if (df["feedback"][i][j] == "2"):
            notes = inputs[i][j]
            
            # Create a NoteSequence
            ns = NoteSequence()
            for note_data in notes["notes"]:
                note = NoteSequence.Note(pitch=note_data["pitch"], start_time=note_data.get("startTime", 0), end_time=note_data["endTime"], velocity=note_data["velocity"])
                ns.notes.append(note)

            notes_to_train.append(ns)

exit
# import json

# data = []
# with open('datasets/tmpcFDwkB') as f:
#     for line in f:
#         data.append(json.loads(line))

# for i in range(len(data)):
#     #
#     for j in range(len(data[i]["input_sequence"])):
#         #solo nos interesan las notas si el feedback es positivo ("2")
#         if (data[i]["feedback"][j] == "2"):
#             notes = data[i]["input_sequence"][j]
#             print(notes["notes"])
#             print("----------------------------------------------------------")
