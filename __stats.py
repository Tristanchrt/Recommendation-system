import json
import pandas as pd
import matplotlib.pyplot as plt
with open('images/metadata/metadata.json','r') as f:
    data = json.loads(f.read())
# df = pd.read_json('images/metadata/metadata.json')

df = pd.json_normalize(
    data,  
    meta=[
        'class',
        ['properties', 'type1', 'types2'], 
    ]
)

grouped_df = df.groupby(['properties.type1'])['properties.type1']
print(grouped_df.describe())
x = []
y = []
for key, item in grouped_df:
    group = grouped_df.get_group(key)
    x.append(key)
    y.append(group.count())

plt.bar(x,y )
plt.show()
# print(stats)

