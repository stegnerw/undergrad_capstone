import os
import cv2
import numpy as np
import pickle
import tensorflow as tf
from tensorflow import keras
from tensorflow.keras import layers
from tensorflow.keras import models
from tensorflow.keras import losses

# Relevant directory and file definitions
proj_dir        = os.path.dirname(os.path.realpath(__file__))
train_pickle    = os.path.join(proj_dir, 'train_set.pickle')
test_pickle     = os.path.join(proj_dir, 'test_set.pickle')
out_dir         = os.path.join(proj_dir, 'networks/cnn_v1')

# Load train/test data
print('Loading train/test data...')
train       = pickle.load(open(train_pickle, 'rb'))
test        = pickle.load(open(test_pickle, 'rb'))
img_shape   = train['image'][0].shape
print(img_shape)

# Limit TF memory usage
physical_devices = tf.config.experimental.list_physical_devices('GPU')
assert len(physical_devices) > 0, "Not enough GPU hardware devices available"
config = tf.config.experimental.set_memory_growth(physical_devices[0], True)

# Define network model
print('Constructing network model...')
model = models.Sequential()
model.add(layers.Conv2D(50, (4, 4), padding='same', activation='tanh', input_shape=img_shape))
model.add(layers.MaxPool2D(pool_size=(3, 3)))
model.add(layers.Dropout(0.25))
model.add(layers.Conv2D(25, (3, 3), padding='same', activation='tanh'))
model.add(layers.MaxPool2D(pool_size=(3, 3)))
model.add(layers.Dropout(0.25))
model.add(layers.GlobalAvgPool2D())
model.add(layers.Dense(50, activation='tanh'))
model.add(layers.Dense(1, activation='sigmoid'))
model.compile(loss=losses.BinaryCrossentropy(), optimizer='Adam', metrics=['accuracy'])

model.fit(train['image'], train['class'], batch_size=32, verbose=1, validation_data=(test['image'], test['class']), epochs=1000, shuffle=True)

model.save(out_dir)

print(model.evaluate(test['image'], test['class'], verbose=2))

