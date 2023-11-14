from .model import Model
import os

model = Model()
current_dir = os.path.dirname(os.path.abspath(__file__))
images_path = os.path.join(current_dir, 'images')


# ensure the model ingests images of all sizes
def test_ingesting_different_sizes():
    for filename in os.listdir(images_path):
        if filename != '.DS_Store':
            full_path = os.path.join(images_path, filename)
            model.predict_path(full_path)
            img = model.form_image(full_path)
            model.is_dog(img)
            model.predict_breed(img)
