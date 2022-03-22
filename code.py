import os
from PIL import Image
from PIL.ExifTags import TAGS
import pandas as pd
import json
import numpy as np
import numpy
import math
from sklearn.cluster import KMeans
import matplotlib.image as img


def main_colors(imgfile):
    numarray = numpy.array(imgfile.getdata(), numpy.uint8)
    if len(numarray.shape) == 2:
        clusters = KMeans(n_clusters = 5)
        clusters.fit(numarray)
        colors = []
        for i in range(0,2):
            color = '#%02x%02x%02x' % (
                math.ceil(clusters.cluster_centers_[i][0]),
                    math.ceil(clusters.cluster_centers_[i][1]), 
                math.ceil(clusters.cluster_centers_[i][2]))
            colors.append(color)
        return colors
    else:
        return ''


df=pd.read_csv('images/pokemon.csv', sep=',',header=None, skiprows=1)
df.replace(np.nan, "")

json_data = []
for filename in os.listdir("images/images/"):
    f = "images/images/" + filename
    image = Image.open(f)
    metadata = df.loc[df[0] == filename.split(".")[0]]
    # print(image.getdata())
    # histo, colors = kmens_img(image, 2)

    name = metadata[0].values[0]
    json_metadata = {
        "properties" : {
            "name" : metadata[0].replace(np.nan, "None").values[0],
            "type1" : metadata[1].replace(np.nan, "None").values[0],
            "type2" : metadata[2].replace(np.nan, "None").values[0]
        },
        "size" : image.size,
        "main_colors" : main_colors(image),
        "path" : f 
    }
    # json_metadata = json.dumps(json_metadata)
    json_data.append(json_metadata)
with open("images/metadata/metadata.json", 'w+') as outfile:
    outfile.write(json.dumps(json_data))