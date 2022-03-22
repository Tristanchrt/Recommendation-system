import json
import pandas as pd
with open('images/metadata/metadata.json','r') as f:
    data = json.loads(f.read())
# df = pd.read_json('images/metadata/metadata.json')

df = pd.json_normalize(
    data, 
    meta=[
        ['properties', 'type1', 'types2'], 
    ]
)

df.info()


