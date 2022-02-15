import cv2
import numpy as np
from gui import select_file
import time
import matplotlib.pyplot as plt

intensityThreshold = 20
differenceThreshold = 10

def algorithm(img_filename, intensityThreshold, differenceThreshold):
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

    return perfusion, dt 

def finalVal(perfusion):
    perfusionVal = np.mean(perfusion)
    
    return perfusionVal

if __name__ == '__main__':
    img_filename = select_file()
    
    perfusion, dt = algorithm(img_filename, intensityThreshold, differenceThreshold)
    perfusionVal = finalVal(perfusion)

    print(perfusionVal)
    plt.imshow(perfusion, 'gray')
    plt.show()
