import os
import numpy as np
from glob import glob
from tensorflow.keras.applications.resnet50 import preprocess_input
from loader import (
    load_detector_model,
    load_dataset
)
from data_processing import (
    path_to_tensor,
)
from globals import (
    faces_data_dir,
    train_set_dir,
    in_jupyter
)


def is_dog(detector_model, img_path):
    img = preprocess_input(path_to_tensor(img_path))
    prediction = np.argmax(detector_model.predict(img, verbose=in_jupyter))
    return ((prediction <= 268) & (prediction >= 151))


if __name__ == "__main__":
    model = load_detector_model()

    dogs_in_human_files_short = []
    dogs_in_dog_files_short = []

    human_files = np.array(glob(os.path.join(faces_data_dir,
                                             '*', '*')))
    train_files, _ = load_dataset(train_set_dir)
    human_files = human_files[:100]
    train_files = train_files[:100]

    dogs_in_human_files = []
    dogs_in_dog_files = []
    for human in human_files:
        dog_in_human = is_dog(model, human)
        dogs_in_human_files.append(dog_in_human)
    for dog in train_files:
        dog_in_dog = is_dog(model, dog)
        dogs_in_dog_files.append(dog_in_dog)

    print('Proportion of dogs detected by dog_dector in human files: ',
          sum(dogs_in_human_files)/len(dogs_in_human_files))

    print('Proportion of dogs detected by dog_dector in dog_files_short: ',
          sum(dogs_in_dog_files)/len(dogs_in_dog_files))
