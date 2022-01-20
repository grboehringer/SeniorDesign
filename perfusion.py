import cv2
import numpy as np

# import image
I = select_file()
Img = cv2.imread(I)                         # import image

# image conversion and adjustments
gsImg = cv2.cvtColor(Img, cv2.COLOR_BGR2GRAY)   # Convert to grayscale

# I don't believe contrast adjustment is needed since we are only
# creating a perfusion index and there is some abiguity in that function,
# but we can always add it.

""" 
Workflow:
    1) Adjust contrast
    2) Average filtering
    3) Binarize
    4) Remove Background:
        a) Create Structuring Element
        b) Close Image
        c) Subtract background from image
        d) Invert if needed
"""