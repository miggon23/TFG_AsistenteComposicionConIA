from IPython.display import display
import pandas as pd

#lee el json line desde la url y lo convierte en dataframe de pandas
df = pd.read_json(path_or_buf="datasets/bach-doodle.jsonl-00001-of-00192.gz", lines=True)

display(df)