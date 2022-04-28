import os
from PIL import Image
from PIL import ImageColor
from PIL.ExifTags import TAGS
from matplotlib import widgets
import pandas as pd
import json
import numpy as np
import math
from sklearn.cluster import KMeans
import webcolors
import multiprocessing as mp
cpu_count = mp.cpu_count()


def main_colors(imgfile):
    numarray = np.array(imgfile.getdata(), np.uint8)
    if len(numarray.shape) == 2:
        clusters = KMeans(n_clusters = 2)
        clusters.fit(numarray)
        colors = []
        for i in range(2):
            color = '#%02x%02x%02x' % (
                math.ceil(clusters.cluster_centers_[i][0]),
                    math.ceil(clusters.cluster_centers_[i][1]), 
                math.ceil(clusters.cluster_centers_[i][2]))
            colors.append(color)
        return colors
    else:
        return ''

def get_closest_color(rgb_triplet):
    min_colours = {}
    for key, name in webcolors.CSS21_HEX_TO_NAMES.items():
        r_c, g_c, b_c = webcolors.hex_to_rgb(key)
        rd = (r_c - rgb_triplet[0]) ** 2
        gd = (g_c - rgb_triplet[1]) ** 2
        bd = (b_c - rgb_triplet[2]) ** 2
        min_colours[(rd + gd + bd)] = name
    return min_colours[min(min_colours.keys())]

df = pd.read_csv('images/pokemon.csv', sep=',',header=None, skiprows=1)
df.replace(np.nan, "")
json_data = []
total = len([name for name in os.listdir("images/images/")])

def explore_image(filename,id):
        f = "images/images/" + filename
        image = Image.open(f)
        image = image.resize((120,120))
        metadata = df.loc[df[0] == filename.split(".")[0]]
    
        closest_name_list = []
        main_colors_value = main_colors(image)
        for i in range(len(main_colors_value)):
            rgb_color = ImageColor.getcolor(main_colors_value[i], "RGB")
            closest_name = get_closest_color(rgb_color)
            closest_name_list.append(closest_name)  

        
        json_metadata = {
            "id" : id,
            "properties" : {
                "name" : metadata[0].replace(np.nan, "None").values[0],
                "type1" : metadata[1].replace(np.nan, "None").values[0],
                "type2" : metadata[2].replace(np.nan, "None").values[0]
            },
            "size" : image.size,
            "colors" : main_colors_value,
            "closest_colors": closest_name_list,
            "tags" : [],
            "path" : f 
        }
        json_data.append(json_metadata)
        print(json_metadata)
        return json_metadata

filenames = os.listdir("images/images/")[:200]
with mp.Pool(processes=cpu_count) as pool:
    array = pool.starmap(explore_image, zip(filenames, range(1,len(filenames))))
    with open("images/metadata/metadata.json", 'w+') as outfile:
        outfile.write(json.dumps(array))

