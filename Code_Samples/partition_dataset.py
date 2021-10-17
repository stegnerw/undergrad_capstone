import os
import random
import json

# Constant Definitions
TRAIN_PERCENT    = 80

# Relevant directory and file definitions
proj_dir        = os.path.dirname(os.path.realpath(__file__))
benign_dir      = proj_dir + '/Dataset_Generation/benign_files/'
infected_dir    = proj_dir + '/Dataset_Generation/infected_files/'
train_json      = proj_dir + '/train_set.json'
test_json       = proj_dir + '/test_set.json'

# Get list of files
max_file_size = 100000
file_names = []
benign_files = os.listdir(benign_dir)
for f in benign_files:
    file_names.append(os.path.join(benign_dir, f))
infected_files = os.listdir(infected_dir)
for f in infected_files:
    file_names.append(os.path.join(infected_dir, f))
file_names = [f for f in file_names if os.path.getsize(f) <= max_file_size]
random.shuffle(file_names)

# Partition files
train_files = []
test_files  = []
first_test  = (len(file_names) * TRAIN_PERCENT) // 100
for fn in file_names[:first_test]:
    if os.path.splitext(fn)[1] == '.benign':
        fclass = 'benign'
    else:
        fclass = 'malicious'
    train_files.append({
        'file_name':    fn,
        'class':        fclass
    })

for fn in file_names[first_test:]:
    if os.path.splitext(fn)[1] == '.benign':
        fclass = 'benign'
    else:
        fclass = 'malicious'
    test_files.append({
        'file_name':    fn,
        'class':        fclass
    })

# Shuffle partitions
random.shuffle(train_files)
random.shuffle(test_files)

# Export json
with open(train_json, 'w') as trainf:
    json.dump(train_files, trainf)

with open(test_json, 'w') as testf:
    json.dump(test_files, testf)

print('Done')

