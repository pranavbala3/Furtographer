import os
import numpy as np
from tensorflow.keras.models import Sequential
from tensorflow.keras.layers import GlobalAveragePooling2D, Dense
from tensorflow.keras.applications.resnet50 import ResNet50
from sklearn.datasets import load_files
from tensorflow.keras.utils import to_categorical
from globals import (
    num_dog_breeds,
    saved_models_dir,
    bottleneck_features_dir,
)


def load_dataset(path):
    data = load_files(path)
    dog_files = np.array(data['filenames'])
    dog_targets = to_categorical(np.array(data['target']), 133)
    return dog_files, dog_targets


def load_detector_model():
    return ResNet50(weights='imagenet')


def load_bottleneck_features():
    bottleneck_features = np.load(os.path.join(bottleneck_features_dir,
                                               'DogResnet50Data.npz'))
    train_Resnet50 = bottleneck_features['train']
    valid_Resnet50 = bottleneck_features['valid']
    test_Resnet50 = bottleneck_features['test']

    return train_Resnet50, valid_Resnet50, test_Resnet50


def load_model(bottling_model, name=None):
    model = Sequential()
    model.add(GlobalAveragePooling2D(input_shape=(bottling_model.layers[-1].
                                                  output_shape[1:])))
    model.add(Dense(num_dog_breeds, activation='softmax'))

    model.compile(loss='categorical_crossentropy',
                  optimizer='rmsprop', metrics=['accuracy'])

    if name:
        model_path = os.path.join(saved_models_dir, name)
        assert os.path.exists(model_path)
        model.load_weights(model_path)

    return model


def load_bottling_model():
    return ResNet50(weights='imagenet', include_top=False)
