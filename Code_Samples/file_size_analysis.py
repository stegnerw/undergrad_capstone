import os
import matplotlib.pyplot as plt

# Relevant directory and file definitions
proj_dir        = os.path.dirname(os.path.realpath(__file__))
benign_dir      = proj_dir + '/Dataset_Generation/benign_files/'
infected_dir    = proj_dir + '/Dataset_Generation/infected_files/'

# Get list of files
file_names = []
benign_files = os.listdir(benign_dir)
for f in benign_files:
    file_names.append(os.path.join(benign_dir, f))
infected_files = os.listdir(infected_dir)
for f in infected_files:
    file_names.append(os.path.join(infected_dir, f))

file_sizes = [os.path.getsize(f) for f in file_names]

num_files = []
file_thresh = []
#max_size = max(file_sizes) + 1
max_size = 100000
size_step = 10
for size in range(0, max_size, size_step):
    if size % (size_step*500) == 0:
        print('size: ', size, '/', max_size, ' - ', size/max_size * 100, '%')
    num_files.append(len([s for s in file_sizes if s <= size]))
    file_thresh.append(size)

plt.plot(file_thresh, num_files)
plt.xlabel('Max File Size, bytes')
plt.ylabel('Number of Files')
plt.title('File Count vs Cutoff Size')
plt.show()

file_sizes = [s for s in file_sizes if s <= max_size]
print('Remaining files:', len(file_sizes))

n, bins, patches = plt.hist(x=file_sizes, bins=20, color='#0504aa', alpha=0.7, rwidth=0.85)
plt.grid(axis='y', alpha=0.75)
plt.xlabel('File Size, bytes')
plt.ylabel('Number of Files')
plt.title('Distribution of File Sizes')
plt.show()

