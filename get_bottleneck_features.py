import requests
import shutil
import os
from nets.globals import bottleneck_features_dir

urls = [
    'https://s3-us-west-1.amazonaws.com/udacity-aind/dog-project/' +
    'DogResnet50Data.npz'
]

os.makedirs(bottleneck_features_dir, exist_ok=True)

for url in urls:
    file_name = os.path.join(bottleneck_features_dir, os.path.basename(url))
    response = requests.get(url, stream=True)
    with open(file_name, "wb") as file:
        shutil.copyfileobj(response.raw, file)
