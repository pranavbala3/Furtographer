from .model import Model
import pytest
import os


@pytest.fixture
def model():
    return Model()


# Fixture to get the path to the 'images' directory
@pytest.fixture
def images_path():
    current_dir = os.path.dirname(os.path.abspath(__file__))
    return os.path.join(current_dir, 'images')


# ensure the model ingests images of all sizes
def test_ingesting_different_sizes(model, images_path):
    for filename in os.listdir(images_path):
        if filename != '.DS_Store':
            path = os.path.join(images_path, filename)
            model.predict_path(path)
            img = model.form_image(path)
            model.is_dog(img)
            model.predict_breed(img)
