import os
from PIL import Image
from PIL.ExifTags import TAGS
import pandas as pd
import json
import numpy as np
import math
from sklearn.cluster import KMeans
import matplotlib.image as img



with open("images/metadata/metadata.json", 'w+') as outfile:
    outfile.write(json.dumps(json_data))