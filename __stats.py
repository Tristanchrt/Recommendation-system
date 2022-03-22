import json
import pandas as pd
with open('images/metadata/metadata.json','r') as f:
    data = json.loads(f.read())
# df = pd.read_json('images/metadata/metadata.json')

df = pd.json_normalize(
    data, 
    record_path =['students'], 
    meta=[
        'class',
        ['properties', 'type1', 'types2'], 
        # ['info', 'contacts', 'tel']
    ]
)

df.values()


