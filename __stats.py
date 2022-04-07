import json
import pandas as pd
import matplotlib.pyplot as plt
import squarify
with open('images/metadata/metadata.json','r') as f:
    data = json.loads(f.read())
    dataFrame = pd.DataFrame(data)

df = pd.read_json('images/metadata/metadata.json')

df = pd.json_normalize(
    data,  
    meta=[
        'class',
        ['properties', 'type1', 'types2'],
        'colors' 
    ]
)

## Count by type
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

### Colors bar 
count_by_colors = {}

for el in data:
    colors = el["closest_colors"]
    for color in colors:
        if color in count_by_colors.keys():
            count_by_colors[color] += 1
        else: 
            count_by_colors[color] = 1

plt.bar(range(len(count_by_colors)), list(count_by_colors.values()), align='center', color=count_by_colors.keys())
plt.xticks(range(len(count_by_colors)), list(count_by_colors.keys()))
plt.show()


df = pd.DataFrame({'presence':count_by_colors.values(), 'color':count_by_colors.keys() })

# plot it
squarify.plot(sizes=df['presence'], label=df['color'], alpha=.8 ,color=count_by_colors.keys())
plt.axis('off')
plt.show()
import matplotlib.image as mpimg

_, axs = plt.subplots(2, 5, figsize=(8, 8))
axs = axs.flatten()
for ax in axs:
    image = list(dataFrame.sample()['path'].items())[0][1]
    img = mpimg.imread(image)
    ax.imshow(img)
plt.show()


