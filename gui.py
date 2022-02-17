from functools import update_wrapper
import tkinter as tk
from tkinter import *
from tkinter.filedialog import askopenfilename
from turtle import left, right
from PIL import ImageTk, Image
<<<<<<< HEAD
#from perfusion import *
=======
# from perfusion import *
>>>>>>> d6790ea83a084d493247036c5eddb16b112471a8

def start_window():
    intial_img = Image.open("Instructions.jpg")
    intial_img = intial_img.resize((512,512))
    intial_img = ImageTk.PhotoImage(intial_img)
    size = tk.Label(root)
    size.grid(row = 0, column = 0, columnspan=2, rowspan=40,padx=10,pady=10)
    size.image = intial_img
    size['image'] = intial_img

    intro = tk.Label(root, text = 'Upload Files and Display', bg ='#3A3B3C', fg = 'white')
    intro.grid(row = 0, column = 2, padx=5, sticky = "s")

    upload = tk.Button(root, text = 'Upload Files', width = 20, bg ='#3A3B3C', fg = 'white', command =lambda:open_image())
    upload.grid(row = 1, column = 2, padx=5, sticky = "n")

    threshold_intensity.grid(row=5, column=2, padx=5, sticky = "s")
    intensity_thresh_entry.grid(row=6, column=2, padx=5, sticky = "n")

    diff_threshold.grid(row=8, column=2, padx=5, sticky = "s")
    diff_thresh_entry.grid(row=9, column=2, padx=5, sticky = "n")

    perfusion_value.grid(row=11, column=2, padx=5, sticky = "s")
    per_val_entry.grid(row=12, column=2, padx=5, sticky = "n")

    save.grid(row = 15, column = 2, padx=5)

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

    perfusion = algorithm(filename,intensityThreshold,differenceThreshold)
    perfusionVal = finalVal(perfusion)

    intensity_thresh_entry.insert(0,intensityThreshold)

    diff_thresh_entry.insert(0,differenceThreshold)

    per_val_entry.insert(0,perfusionVal)

def threshold_display(filename,intensityThreshold,differenceThreshold):
    perfusion = algorithm(filename,intensityThreshold,differenceThreshold)
    perfusionVal = finalVal(perfusion)

    intensity_thresh_entry.insert(0,intensityThreshold)

    diff_thresh_entry.insert(0,differenceThreshold)

    per_val_entry.insert(0,perfusionVal)

if __name__ == '__main__':
    perIndex = 55.5

    root = tk.Tk()
    root.geometry("706x534")
    root.title('Testing GUI')
    root.configure(bg='#3A3B3C')

    threshold_intensity = Label(root, text="Intensity Threshold", bg ='#3A3B3C', fg = 'white')
    intensity_thresh_entry = Entry(root)

    diff_threshold = Label(root, text="Difference Threshold",bg ='#3A3B3C', fg = 'white')
    diff_thresh_entry = Entry(root)

    perfusion_value = Label(root, text="Perfusion value",bg ='#3A3B3C', fg = 'white')
    per_val_entry = Entry(root)

    save = tk.Button(root, text = 'Save Files', width = 20, bg ='#3A3B3C', fg = 'white') #doesn't do anything at the moment

    start_window()
    
    # Double window is occuring because the select_file() function was taken out of open_image() and called here. Need to fix.
    
    #threshold_display(filename,intensityThreshold,differenceThreshold)

    root.mainloop() #allows the window to stay open

""" 
To Do:
    i) Rectangular Image Select - John
    ii) Grid Layout understanding - Bradie
    iii) Save the GUI info
    1) Add adjustable threshold values with a default to start (DT & IT)
    2) Add the perfusion value
    3) Make image size larger
    4) Make GUI look appealing (buttons all on one side, items properly spaced, etc.)
    5) Work on zooming in on the image, showing the percentage the pixels take up of perfusion value
    """
