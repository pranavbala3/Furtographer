import os
import numpy as np
from tensorflow.keras.models import Sequential
from tensorflow.keras.layers import GlobalAveragePooling2D, Dense
from tensorflow.keras.applications.resnet50 import ResNet50
from tensorflow.keras.applications.resnet50 import preprocess_input
from tensorflow.keras.preprocessing import image
import ssl
ssl._create_default_https_context = ssl._create_unverified_context
from .globals import (
    dog_names,
    num_dog_breeds,
    saved_models_dir,
    default_saved_model_name
)


class Model():
    def __init__(self, name=None):
        self.detector_model = load_detector_model()
        self.bottler = load_bottling_model()
        if name is None:
            name = default_saved_model_name
        self.classifier = load_classifier(self.bottler, name)

    def predict_path(self, path):
        img = preprocess_input(path_to_tensor(path))
        if self.is_dog(img):
            breed = self.predict_breed(img).split('.')[-1]
            return breed
        return None

    def is_dog(self, img):
        out = self.detector_model.predict(img, verbose=0)
        prediction = np.argmax(out)
        return ((prediction <= 268) & (prediction >= 151))

    def predict_breed(self, img):
        # extract bottleneck features
        bottleneck_feature = self.bottler.predict(img, verbose=0)
        # obtain predicted vector
        predicted_vector = self.classifier.predict(bottleneck_feature,
                                                   verbose=0)
        # return dog breed that is predicted by the model
        return dog_names[np.argmax(predicted_vector)]


def load_bottling_model():
    return ResNet50(weights='imagenet', include_top=False)


def load_detector_model():
    return ResNet50(weights='imagenet')


def load_classifier(bottling_model, name=None):
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


def path_to_tensor(img_path):
    # loads RGB image as PIL.Image.Image type
    img = image.load_img(img_path, target_size=(224, 224))
    # convert PIL.Image.Image type to 3D tensor with shape (224, 224, 3)
    x = image.img_to_array(img)
    # convert 3D tensor to 4D tensor with shape (1, 224, 224, 3)
    # and return 4D tensor
    return np.expand_dims(x, axis=0)
