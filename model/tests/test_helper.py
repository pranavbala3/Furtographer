import numpy as np
import os
import os.path
from sklearn.datasets import load_files
from tensorflow.keras.utils import to_categorical
from ..globals import (
    bottleneck_features_dir
    )


def load_dataset(path):
    data = load_files(path)
    dog_files = np.array(data['filenames'])
    dog_targets = to_categorical(np.array(data['target']), 133)
    return dog_files, dog_targets


def load_bottleneck_features():
    bottleneck_features = np.load(os.path.join(bottleneck_features_dir,
                                               'DogResnet50Data.npz'))
    train_Resnet50 = bottleneck_features['train']
    valid_Resnet50 = bottleneck_features['valid']
    test_Resnet50 = bottleneck_features['test']

    return train_Resnet50, valid_Resnet50, test_Resnet50
