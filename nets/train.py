import numpy as np
import os
from datetime import datetime
from tensorflow.keras.callbacks import ModelCheckpoint

from globals import (
    train_set_dir,
    valid_set_dir,
    test_set_dir,
    saved_models_dir,
    dog_names,
    bottleneck_features_dir,
)
from loader import (
    load_model,
    load_bottling_model,
)
from data_processing import load_dataset


# load train, test, and validation datasets
train_files, train_targets = load_dataset(train_set_dir)
valid_files, valid_targets = load_dataset(valid_set_dir)
test_files, test_targets = load_dataset(test_set_dir)

# print statistics about the dataset
print('There are %d total dog categories.' % len(dog_names))
print('There are %s total dog images.\n' %
      len(np.hstack([train_files, valid_files, test_files])))
print('There are %d training dog images.' % len(train_files))
print('There are %d validation dog images.' % len(valid_files))
print('There are %d test dog images.' % len(test_files))

bottleneck_features = np.load(os.path.join(bottleneck_features_dir,
                                           'DogResnet50Data.npz'))
train_Resnet50 = bottleneck_features['train']
valid_Resnet50 = bottleneck_features['valid']
test_Resnet50 = bottleneck_features['test']

bottling_model = load_bottling_model()
model = load_model(bottling_model)
model.summary()

model.compile(loss='categorical_crossentropy',
              optimizer='rmsprop',
              metrics=['accuracy'])
model_path = os.path.join(saved_models_dir, datetime.today().
                          strftime('%Y%m%d-') + 'best_weights_resnet50.hdf5')

checkpointer = ModelCheckpoint(filepath=model_path, verbose=1,
                               save_best_only=True)
model.fit(train_Resnet50, train_targets,
          validation_data=(valid_Resnet50, valid_targets),
          epochs=20, batch_size=20, callbacks=[checkpointer], verbose=1)

model_predictions = [np.argmax(model.predict(np.expand_dims(feature, axis=0),
                                             verbose=0))
                     for feature in test_Resnet50]

# report test accuracy
correct_predictions = np.sum(np.array(model_predictions) ==
                             np.argmax(test_targets, axis=1))
test_accuracy = 100*correct_predictions/len(model_predictions)
print('Test accuracy: %.4f%%' % test_accuracy)
