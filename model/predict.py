import sys
import os
from .model import (
    load_model,
    load_detector_model,
    load_bottling_model,
    detect_and_predict_breed_from_path,
    )

if __name__ == "__main__":
    path = sys.argv[1]
    if not os.path.exists(path):
        print('Path given doesn\'t exist')
        exit(1)

    detector_model = load_detector_model()
    bottling_model = load_bottling_model()
    model = load_model(bottling_model,
                       name='20231024-best_weights_resnet50.hdf5')
    breed = detect_and_predict_breed_from_path(path, detector_model,
                                               bottling_model, model)
    if breed:
        print(f"breed: {breed}")
    else:
        print("no dog")
