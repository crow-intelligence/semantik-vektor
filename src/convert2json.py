import pandas as pd

df = pd.read_csv('models/final.tsv', sep='\t', encoding='utf-8')
js = df.to_json(orient='records')

import json
j = json.loads(js)
with open('models/semantikvektors.json', 'w') as f:
    json.dump(j, f)
