import os
import sys
import numpy as np
from tensorflow.keras.applications.resnet50 import preprocess_input

from nets.globals import (
    in_jupyter,
    dog_names
)
from nets.loader import (
    load_model,
    load_bottling_model,
    load_detector_model
)
from nets.data_processing import path_to_tensor


if in_jupyter:
    from IPython.display import Image, display

printing = 0


def predict_breed(img_path, bottling_model, model):
    # extract bottleneck features
    input = preprocess_input(path_to_tensor(img_path))
    bottleneck_feature = bottling_model.predict(input, verbose=printing)
    # obtain predicted vector
    predicted_vector = model.predict(bottleneck_feature, verbose=printing)
    # return dog breed that is predicted by the model
    return dog_names[np.argmax(predicted_vector)]


def is_dog(img_path, detector_model):
    img = preprocess_input(path_to_tensor(img_path))
    shit = detector_model.predict(img, verbose=printing)
    prediction = np.argmax(shit)
    return ((prediction <= 268) & (prediction >= 151))


def detect_and_predict_breed_with_display(img_path, detector_model, bottling_model, model):
    if in_jupyter:
        display(Image(img_path, width=300))
    breed = detect_and_predict_breed(img_path, detector_model, bottling_model, model);
    if breed:
        print(f'The predicted breed of dog in this image is {breed}')
    else:
        print("no dog in the image")

def detect_and_predict_breed(img_path, detector_model, bottling_model, model):
    if is_dog(img_path, detector_model):
        breed = predict_breed(img_path, bottling_model, model).split('.')[-1]
        return breed;
    return None

if __name__ == "__main__":
    path = sys.argv[1]
    if not os.path.exists(path):
        print('Path given doesn\'t exist')
        exit(1)

    detector_model = load_detector_model()
    bottling_model = load_bottling_model()
    model = load_model(bottling_model,
                       name='20231024-best_weights_resnet50.hdf5')
    detect_and_predict_breed_with_display(path, detector_model, bottling_model, model)
