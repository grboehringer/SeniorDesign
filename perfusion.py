import cv2
import numpy as np
from gui import select_file
import time
import matplotlib.pyplot as plt

def algorithm(img_filename):
    intensityThreshold = 5
    differenceThreshold = 200

    img = cv2.imread(img_filename) 

    intensity = np.mean(img, axis=2)    # Find intensity

    red = img[:,:,2]
    green = img[:,:,1]
    blue = img[:,:,0]

    dt = np.where(intensity > intensityThreshold, differenceThreshold / 3, differenceThreshold)

    boolean = np.abs(red - green) > dt
    boolean = boolean | np.abs(red - blue) > dt
    boolean = boolean | np.abs(green - blue) > dt

    perfusion = intensity * boolean

    return perfusion

if __name__ == '__main__':
    img_filename = select_file()

    perfusion = algorithm(img_filename)

    plt.imshow(perfusion, 'gray')
    plt.show()

