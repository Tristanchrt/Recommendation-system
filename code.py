# Download dataset on kaggle
import kaggle

kaggle.api.authenticate()
# assign directory
directory="./"
kaggle.api.dataset_download_files('vishalsubbiah/pokemon-images-and-types', path=directory, unzip=True)
