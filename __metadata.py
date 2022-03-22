import os
from PIL import Image
from PIL.ExifTags import TAGS
import pandas as pd
import json
import numpy as np
import math
from sklearn.cluster import KMeans


def kmens_img(image, nb_color):
    numarray = np.array(image.getdata(), np.uint8)
    clusters = KMeans(n_clusters = nb_color)
    clusters.fit(numarray)
    npbins = np.arange(0, nb_color+1)
    histogram = np.histogram(clusters.labels_, bins=npbins)

    color_list = []

    for i in range(nb_color):
        colors = '#%02x%02x%02x' % ( math.ceil(clusters.cluster_centers_[i][0]), 
                    math.ceil(clusters.cluster_centers_[i][1]),
                    math.ceil(clusters.cluster_centers_[i][2]))
        color_list.append(colors)

    return sorted(histogram[0], reverse=True), color_list

df=pd.read_csv('images/pokemon.csv', sep=',',header=None, skiprows=1)
df.replace(np.nan, "")
# print(df.values)
json_data = []
id = 0
for filename in os.listdir("images/images/"):
    f = "images/images/" + filename
    image = Image.open(f)
    metadata = df.loc[df[0] == filename.split(".")[0]]
    # print(image.getdata())
    # histo, colors = kmens_img(image, 2)
    name = metadata[0].values[0]
    id+=1
    json_metadata = {
        "id" : id,
        "properties" : {
            "name" : metadata[0].replace(np.nan, "None").values[0],
            "type1" : metadata[1].replace(np.nan, "None").values[0],
            "type2" : metadata[2].replace(np.nan, "None").values[0]
        },
        "size" : image.size,
        "colors" : '',
        "tags" : [],
        "path" : f 
    }
    # json_metadata = json.dumps(json_metadata)
    json_data.append(json_metadata)
with open("images/metadata/metadata.json", 'w+') as outfile:
    outfile.write(json.dumps(json_data))