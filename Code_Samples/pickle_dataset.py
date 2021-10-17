import os
import json
import pickle
import numpy as np
import cv2
from FileImage import FileImage

# Constant declarations
IMG_WIDTH   = 32
CLASSES     = ['benign', 'malicious']
NUM_CLASSES = 2

# Relevant directory and file definitions
proj_dir        = os.path.dirname(os.path.realpath(__file__))
train_json      = proj_dir + '/train_set.json'
test_json       = proj_dir + '/test_set.json'
train_pickle    = proj_dir + '/train_set.pickle'
test_pickle     = proj_dir + '/test_set.pickle'

def jsonToPickle(json_path, pickle_path, height, width):
    # Import json
    with open(json_path) as json_fd:
        json_contents = json.load(json_fd)

    # Create dictionaries to store values
    pickle_contents = {
            'file_name':    [],
            'image':        [],
            'class':        []
    }

    for f in json_contents:
        pickle_contents['file_name'].append(f['file_name'])
        img_obj = FileImage(f['file_name'], height, width)
        # cv2.imshow(f['file_name'], img_obj.getImage())
        # cv2.waitKey()
        # cv2.destroyAllWindows()
        pickle_contents['image'].append(img_obj.getImage())
        for i in range(NUM_CLASSES):
            if (f['class'] == CLASSES[i]):
                pickle_contents['class'].append(float(i))
    # Reshape input into np array to make tensorflow happy
    pickle_contents['image'] = np.array(pickle_contents['image']).reshape((-1, height, width, 1))
    # pickle_contents['image'] = np.array(pickle_contents['image']).reshape((-1, height, width))
    pickle_contents['class'] = np.array(pickle_contents['class']).reshape((-1, 1))

    # Save pickle file
    pickle.dump(pickle_contents, open(pickle_path, 'wb'))

# Calculate image height
max_size = 0
with open(train_json) as f:
    data = json.load(f)
    max_size = max(max_size, max([os.path.getsize(elem['file_name']) for elem in data]))
with open(test_json) as f:
    data = json.load(f)
    max_size = max(max_size, max([os.path.getsize(elem['file_name']) for elem in data]))
print(max_size)
IMG_HEIGHT = (max_size // IMG_WIDTH) + 1

print('Pickling train set...')
jsonToPickle(train_json, train_pickle, IMG_HEIGHT, IMG_WIDTH)
print('Pickling test set...')
jsonToPickle(test_json, test_pickle, IMG_HEIGHT, IMG_WIDTH)

print('Done')

