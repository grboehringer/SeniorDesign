from functools import update_wrapper
import tkinter as tk
from tkinter import *
from tkinter.filedialog import askopenfilename
from turtle import left, right
from PIL import ImageTk, Image
#from perfusion import *

def start_window():
    intial_img = Image.open("Instructions.jpg")
    intial_img = intial_img.resize((512,512))
    intial_img = ImageTk.PhotoImage(intial_img)
    size = tk.Label(root)
    size.grid(row = 0, column = 0, columnspan=2, rowspan=40,padx=10,pady=10)
    size.image = intial_img
    size['image'] = intial_img

    intro = tk.Label(root, text = ' ', bg ='#3A3B3C', fg = 'white')
    intro.grid(row = 0, column = 2, padx=5, sticky = "s")

    upload = tk.Button(root, text = 'Upload Files', width = 20, bg ='#3A3B3C', fg = 'white', command =lambda:open_image())
    upload.grid(row = 1, column = 2, padx=5, sticky = "n")

    threshold_intensity.grid(row=5, column=2, padx=5, sticky = "s")
    intensity_thresh_entry.grid(row=6, column=2, padx=5, sticky = "n")

    diff_threshold.grid(row=8, column=2, padx=5, sticky = "s")
    diff_thresh_entry.grid(row=9, column=2, padx=5, sticky = "n")

    gain_val.grid(row=11, column=2, padx=5, sticky = "s")
    gain_val_entry.grid(row=12, column=2, padx=5, sticky = "n")

    perfusion_value.grid(row=14, column=2, padx=5, sticky = "s")
    per_val_entry.grid(row=15, column=2, padx=5, sticky = "n")

    crop.grid(row = 21, column = 2, padx=5)
    compare.grid(row = 23, column = 2, padx=5)
    save.grid(row = 25, column = 2, padx=5)

#finding the filename
def select_file():

    # define allowed file types
    f_types = [('Jpg files', '*.jpg'), ('jpeg files', '*.jpeg'), ('PNG files','*.png')]

    # prompt dialog box
    filename = tk.filedialog.askopenfilename( filetypes = f_types)
    #dynamic column variable
    #image resizing before displaying
    return filename

def open_image():
    global filename
    filename = select_file()
    img = Image.open(filename)
    img = img.resize((512,512))
    #image display code
    # Use this code if no image resizing is wanted/needed: img = ImageTk.PhotoImage(file = filename)
    img = ImageTk.PhotoImage(img)
    size = tk.Label(root)
    size.grid(row = 0, column = 0, columnspan=2, rowspan=40,padx=10,pady=10)
    size.image = img
    size['image'] = img

    threshold_display(filename,intensityThreshold,differenceThreshold)

def threshold_display(filename,intensityThreshold,differenceThreshold):
    perfusion = algorithm(filename,intensityThreshold,differenceThreshold)
    perfusionVal = finalVal(perfusion)

    intensity_thresh_entry.insert(0,intensityThreshold)

    diff_thresh_entry.insert(0,differenceThreshold)

    gain_val_entry.insert(0,"Enter Gain Value")

    per_val_entry.insert(0,perfusionVal)

def crop_image():
    select_coordinates()
    threshold_display(filename,intensityThreshold,differenceThreshold)

if __name__ == '__main__':
    from perfusion import *
    from crop import *
    perIndex = 55.5

    root = tk.Tk()
    root.geometry("706x534")
    root.title('Testing GUI')
    root.configure(bg='#3A3B3C')

    threshold_intensity = Label(root, text="Intensity Threshold", bg ='#3A3B3C', fg = 'white')
    intensity_thresh_entry = Entry(root)

    diff_threshold = Label(root, text="Difference Threshold",bg ='#3A3B3C', fg = 'white')
    diff_thresh_entry = Entry(root)

    gain_val = Label(root, text="Gain Value", bg ='#3A3B3C', fg = 'white')
    gain_val_entry = Entry(root)

    perfusion_value = Label(root, text="Perfusion Index Value",bg ='#3A3B3C', fg = 'white')
    per_val_entry = Entry(root)

    crop = tk.Button(root, text = 'Crop Image', width = 20, bg ='#3A3B3C', fg = 'white', command =lambda:crop_image()) #doesn't do anything at the moment

    compare = tk.Button(root, text = 'Compare Images', width = 20, bg ='#3A3B3C', fg = 'white') #doesn't do anything at the moment

    save = tk.Button(root, text = 'Save Files', width = 20, bg ='#3A3B3C', fg = 'white') #doesn't do anything at the moment

    start_window()
    
    # Double window is occuring because the select_file() function was taken out of open_image() and called here. Need to fix.
    
    #threshold_display(filename,intensityThreshold,differenceThreshold)

    root.mainloop() #allows the window to stay open

""" 
To Do:

    1) Add adjustable threshold values with a default to start (DT & IT)
    2) Save GUI info and Image/Video
    3) Cropping Image and saving new image with GUI info
    4) Allow for PI comparison
    5) Import video and plot PIs
    6) Make GUI look appealing (buttons all on one side, items properly spaced, etc.)
    """
