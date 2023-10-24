import os
from tensorflow.keras.models import Sequential
from tensorflow.keras.layers import GlobalAveragePooling2D, Dense
from tensorflow.keras.applications.resnet50 import ResNet50
from globals import (
    num_dog_breeds,
    saved_models_dir,
)


def load_detector_model():
    return ResNet50(weights='imagenet')


def load_model(bottling_model, name=None):
    model = Sequential()
    model.add(GlobalAveragePooling2D(input_shape=(bottling_model.layers[-1].
                                                  output_shape[1:])))
    model.add(Dense(num_dog_breeds, activation='softmax'))

    model.compile(loss='categorical_crossentropy',
                  optimizer='rmsprop', metrics=['accuracy'])

    if name:
        model_path = os.path.join(saved_models_dir, name)
        model.load_weights(model_path)

    return model


def load_bottling_model():
    return ResNet50(weights='imagenet', include_top=False)
