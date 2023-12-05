from .model import Model
from .globals import dog_names
import pytest
import os


current_dir = os.path.dirname(os.path.abspath(__file__))


@pytest.fixture
def model():
    return Model()


def images_path():
    return os.path.join(current_dir, 'images')


@pytest.fixture
def multi_size_path():
    return os.path.join(images_path(), 'many_size')


@pytest.fixture
def example_path():
    return os.path.join(images_path(), 'examples')


# ensure the model ingests images of all sizes
def test_ingesting_different_sizes(model, multi_size_path):
    for filename in os.listdir(multi_size_path):
        if filename != '.DS_Store':
            path = os.path.join(multi_size_path, filename)
            model.predict_path(path)
            img = model.form_image(path)
            model.is_dog(img)
            model.predict_breed(img)


def assert_prediction(path, target, model):
    if target is None:
        assert model.predict_path(path) is None
    else:
        assert model.predict_path(path) == target
    # assert model.predict_path(path) == target


# ensure the model ingests images of all sizes
def test_example_classifications(model, example_path):
    for filename in os.listdir(example_path):
        if filename != '.DS_Store':
            name = os.path.splitext(filename)[0]
            if name in dog_names:
                assert_prediction(os.path.join(example_path, filename), name,
                                  model)
            else:
                assert_prediction(os.path.join(example_path, filename), None,
                                  model)
