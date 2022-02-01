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

boolean = np.abs(red - green) > differenceThreshold
boolean = boolean | np.abs(red - blue) > differenceThreshold
boolean = boolean | np.abs(green - blue) > differenceThreshold

perfusion = intensity * boolean
print('boolean:\n')
print(boolean)
print('perfusion:\n')
print(perfusion)