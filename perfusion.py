import cv2
import numpy as np

import tkinter as tk
from tkinter import ttk
from tkinter import filedialog as fd

# create the root window
root = tk.Tk()                          # creates box
root.title('Image Selection')           # name of box
root.resizable(False, False)            # user can't change size
root.geometry('300x150')                # size of box

# file selection function (Should this be in its own file?)
def select_file():
    
    # define allowed file types
    filetypes = (
        ('Image files', '*.jpg'),
        ('All files', '*.*')
    )

    # prompt dialog box
    filename = fd.askopenfilename(
        title='Open an image',
        initialdir='/',
        filetypes=filetypes)

# open button
open_button = ttk.Button(
    root,
    text='Open an Image',
    command=select_file
)

open_button.pack(expand=True)

#root.mainloop()

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