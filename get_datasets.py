import requests
import shutil
import os
import zipfile
from nets.globals import dataset_dir

data_urls = [
    'http://s3-us-west-1.amazonaws.com/udacity-aind/dog-project/dogImages.zip',
    'https://s3-us-west-1.amazonaws.com/udacity-aind/dog-project/lfw.zip'
]

os.makedirs(dataset_dir, exist_ok=True)

for url in data_urls:
    file_name = os.path.join(dataset_dir, os.path.basename(url))
    response = requests.get(url, stream=True)
    with open(file_name, "wb") as file:
        shutil.copyfileobj(response.raw, file)
    with zipfile.ZipFile(file_name, 'r') as zip_ref:
        zip_ref.extractall(dataset_dir)
    os.remove(file_name)
    print(f"Extracted {url} to {dataset_dir}")

delete = os.path.join(dataset_dir, "__MACOSX")
if os.path.exists(delete):
    shutil.rmtree(delete)
