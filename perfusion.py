import cv2
import numpy as np
from gui import select_file

I = select_file()

img = cv2.imread(I)     # Import image

intensityThreshold = 5
differenceThreshold = 6

intensity = np.mean(img, axis=2)    # Find intensity

red = img[:,:,2]
green = img[:,:,1]
blue = img[:,:,0]

"""
if (abs(red - green) > dt):
    bool = 1
elif (abs(green - blue) > dt):
    bool = 1
elif (abs(red - blue) > dt):
    bool = 1
else:
    bool = 0
"""