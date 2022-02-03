import cv2
import numpy as np
from gui import select_file
import time
import matplotlib.pyplot as plt

def algorithm(img):
    intensityThreshold = 5
    differenceThreshold = 6

    intensity = np.mean(img, axis=2)    # Find intensity

    red = img[:,:,2]
    green = img[:,:,1]
    blue = img[:,:,0]

    boolean = np.abs(red - green) > differenceThreshold
    boolean = boolean | np.abs(red - blue) > differenceThreshold
    boolean = boolean | np.abs(green - blue) > differenceThreshold

    perfusion = intensity * boolean

    return perfusion

if __name__ == '__main__':
    I = select_file()

    img = cv2.imread(I)     # Import image

    perfusion = algorithm(img)

    plt.imshow(perfusion, 'gray')
    plt.show()

