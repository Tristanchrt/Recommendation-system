# Download dataset on kaggle
import kaggle
kaggle.api.authenticate()
# assign directory
directory = 'images'
kaggle.api.dataset_download_files('vishalsubbiah/pokemon-images-and-types', path=directory, unzip=True)



import os
from PIL import Image
from PIL.ExifTags import TAGS
for filename in os.listdir(directory + "/images/"):
    print(filename)
    f = directory + "/images/" + filename
    image = Image.open(f) 
    exif=dict(image.getexif().items())
    print(exif)