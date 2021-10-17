import os
import numpy as np
import math
import cv2

class FileImage:
    def __init__(self, file_path, height=100, width=25):
        # Check if file exists
        if not os.path.isfile(file_path):
            raise FileNotFoundError('Could not load binary because file does not exist')
        self.file_path = file_path
        self.file_size = os.path.getsize(file_path)
        self.setImageSize(height, width)

        # Load binary file
        self.file_contents = np.empty(self.file_size, dtype='uint8')
        if not os.path.isfile(self.file_path):
            raise FileNotFoundError('Could not load binary because file does not exist')
        with open(self.file_path, 'rb') as f:
            idx = 0
            new_byte = f.read(1)
            while new_byte:
                self.file_contents[idx] = int.from_bytes(new_byte, byteorder='big')
                idx += 1
                new_byte = f.read(1)

    def setImageSize(self, height, width):
        if (width > 0):
            self.img_width = width
        if (height > 0):
            self.img_height = height

    def getImage(self):
        img = np.zeros(self.img_width * self.img_height, dtype='uint8')
        for i in range(min(self.file_size, img.size)):
            img[i] = self.file_contents[i]
        img = img.reshape((self.img_height, self.img_width))
        return img


    def showImage(self):
        img = self.getImage()
        cv2.imshow(self.file_path, img)
        cv2.waitKey()
        cv2.destroyAllWindows()

if __name__ == '__main__':
    f = FileImage('Dataset_Generation/benign_files/ls.benign', 512, 256)
    f.showImage()

