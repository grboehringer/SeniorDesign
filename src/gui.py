from functools import update_wrapper
import tkinter as tk
from tkinter import *
from tkinter.filedialog import askopenfilename
from turtle import left, right
from PIL import ImageTk
import PIL.Image

def start_window():
    intial_img = PIL.Image.open("images/Instructions.jpg")
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

    id.grid(row = 5, column = 2, padx=5, sticky = "s")
    patient_ID.grid(row = 6, column = 2, padx=5,sticky = "n")
    patient_ID.insert(0,"Enter Patient ID")

    gain_val.grid(row=7, column=2, padx=5, sticky = "s")
    gain_val_entry.grid(row=8, column=2, padx=5, sticky = "n")
    gain_val_entry.insert(0,"Enter Gain Value")

    threshold_intensity.grid(row=12, column=2, padx=5, sticky = "s")
    intensity_thresh_entry.grid(row=13, column=2, padx=5, sticky = "n")

    diff_threshold.grid(row=14, column=2, padx=5, sticky = "s")
    diff_thresh_entry.grid(row=15, column=2, padx=5, sticky = "n")

    perfusion_value.grid(row=16, column=2, padx=5, sticky = "s")
    per_val_entry.grid(row=17, column=2, padx=5, sticky = "n")

    change_Th.grid(row = 21, column = 2, padx=5)
    crop.grid(row = 23, column = 2, padx=5)
    compare.grid(row = 25, column = 2, padx=5)
    save.grid(row = 27, column = 2, padx=5)

#finding the filename
def select_file():

    # define allowed file types
    f_types = [('Jpg files', '*.jpg'), ('jpeg files', '*.jpeg'), ('PNG files','*.png')]

    # prompt dialog box
    filename = askopenfilename(filetypes = f_types)
    #dynamic column variable
    #image resizing before displaying
    return filename

def open_image():
    global filename
    filename = select_file()
    img = PIL.Image.open(filename)
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

    intensity_thresh_entry.delete(0, tk.END)
    diff_thresh_entry.delete(0, tk.END)
    per_val_entry.delete(0, tk.END)

    intensity_thresh_entry.insert(0,intensityThreshold)
    diff_thresh_entry.insert(0,differenceThreshold)
    per_val_entry.insert(0,perfusionVal)

def change_Thresholds():
    new_int_thresh = intensity_thresh_entry.get()
    new_diff_thresh = diff_thresh_entry.get()
    threshold_display(filename,int(new_int_thresh),int(new_diff_thresh))

def save_file():
    #to do: create file name as patient ID
    # one file = one patient
    # add header to file
    # user can choose which file to open
    # make it so user can choose where to save it
    # first save image as sepaerate file, then save them in same file
    pID = patient_ID.get()
    diff_thresh = diff_thresh_entry.get()
    int_thresh = intensity_thresh_entry.get()
    gain = gain_val_entry.get()
    per_index = per_val_entry.get()
    f = open('Ultrasound data', 'a+')
    f.write('%s\t%s\t%s\t%s\t%s\n'%(pID,diff_thresh,int_thresh,gain,per_index))
    f.close()

if __name__ == '__main__':
    from perfusion import *
    from crop import *
    perIndex = 55.5

    root = tk.Tk()
    root.geometry("706x534")
    root.title('Perfusion Index')
    root.configure(bg='#3A3B3C')

    id = tk.Label(root, text = 'Patient ID', bg ='#3A3B3C', fg = 'white')
    patient_ID = Entry(root)
    threshold_intensity = Label(root, text="Intensity Threshold", bg ='#3A3B3C', fg = 'white')
    intensity_thresh_entry = Entry(root)
    diff_threshold = Label(root, text="Difference Threshold",bg ='#3A3B3C', fg = 'white')
    diff_thresh_entry = Entry(root)
    gain_val = Label(root, text="Gain Value", bg ='#3A3B3C', fg = 'white')
    gain_val_entry = Entry(root)
    perfusion_value = Label(root, text="Perfusion Index Value",bg ='#3A3B3C', fg = 'white')
    per_val_entry = Entry(root)

    
    change_Th = tk.Button(root, text = "Change Threshold Values", width = 20, bg ='#3A3B3C', fg = 'white',command =lambda:change_Thresholds())
    crop = tk.Button(root, text = 'Crop Image', width = 20, bg ='#3A3B3C', fg = 'white') #doesn't do anything at the moment
    compare = tk.Button(root, text = 'Compare Images', width = 20, bg ='#3A3B3C', fg = 'white') #doesn't do anything at the moment
    save = tk.Button(root, text = 'Save Files', width = 20, bg ='#3A3B3C', fg = 'white',command =lambda:save_file()) #doesn't do anything at the moment

    start_window()

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
