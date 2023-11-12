import os
from glob import glob

current_dir = os.path.dirname(os.path.abspath(__file__))
default_saved_model_name = '20231024-best_weights_resnet50.hdf5'
dataset_dir = os.path.join(current_dir, "datasets")
dog_data_dir = os.path.join(dataset_dir, "dogImages")
faces_data_dir = os.path.join(dataset_dir, "lfw")
bottleneck_features_dir = os.path.join(current_dir, "bottleneck_features")
saved_models_dir = os.path.join(current_dir, "saved_models")
train_set_dir = os.path.join(dog_data_dir, 'train')
valid_set_dir = os.path.join(dog_data_dir, 'valid')
test_set_dir = os.path.join(dog_data_dir, 'test')
dog_names = [item[5:] for item in sorted(glob(os.path.join(train_set_dir,
                                                           '*')))]
num_dog_breeds = len(dog_names)
printing = 0
