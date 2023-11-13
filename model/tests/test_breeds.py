import numpy as np
import sys
from ..model import (
    load_model,
    load_bottling_model,
)
from .test_helper import (
    load_dataset,
    load_bottleneck_features,
)
from ..globals import (
    default_saved_model_name,
    train_set_dir,
    valid_set_dir,
    test_set_dir,
    printing,
)


def print_accuracy(model, features, targets, name):
    predictions = [np.argmax(model.predict(np.expand_dims(feature,
                   axis=0), verbose=printing))
                   for feature in features]
    correct_predictions = np.sum(np.array(predictions) ==
                                 np.argmax(targets, axis=1))
    accuracy = 100 * correct_predictions / len(predictions)
    print(f'{name} accuracy: %.4f%%' % accuracy)


if __name__ == "__main__":
    bottler = load_bottling_model()
    saved_path = sys.argv[1] if len(sys.argv) > 1 else default_saved_model_name
    model = load_model(bottler, saved_path)

    train_files, train_targets = load_dataset(train_set_dir)
    valid_files, valid_targets = load_dataset(valid_set_dir)
    test_files, test_targets = load_dataset(test_set_dir)

    train_features, valid_features, test_features = load_bottleneck_features()

    # print_accuracy(model, train_features, train_targets, "Train")
    # print_accuracy(model, valid_features, valid_targets, "Valid")
    print_accuracy(model, test_features, test_targets, "Test")
