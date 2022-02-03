import tkinter as tk
from tkinter import *
from tkinter.filedialog import askopenfilename
from PIL import ImageTk, Image

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
    size.grid(row = 0, column = 0, columnspan=2, rowspan=35,padx=10,pady=10)
    size.image = img
    size['image'] = img

    threshold_intensity = Label(root, text="Intensity Threshold", bg ='#3A3B3C', fg = 'white')
    threshold_intensity.grid(row=3, column=2, padx=5)
    intensity_thresh_entry = Entry(root)
    intensity_thresh_entry.insert(0,'Intensity Threshold') #need to bring over intensity threshold from perfusion.py
    intensity_thresh_entry.grid(row=4, column=2, padx=5)

    diff_threshold = Label(root, text="Difference Threshold",bg ='#3A3B3C', fg = 'white')
    diff_threshold.grid(row=6, column=2, padx=5)
    diff_thresh_entry = Entry(root)
    diff_thresh_entry.insert(0,'Difference Threshold') #need to bring over difference threshold from perfusion.py
    diff_thresh_entry.grid(row=7, column=2, padx=5)

    perfusion_value = Label(root, text="Perfusion value",bg ='#3A3B3C', fg = 'white')
    perfusion_value.grid(row=9, column=2, padx=5)
    per_val_entry = Entry(root)
    per_val_entry.insert(0,'Perfusion value') #need to bring over perfusion value from perfusion.py
    per_val_entry.grid(row=10, column=2, padx=5)
    
if __name__ == '__main__':
    perIndex = 55.5

    root = tk.Tk()
    root.geometry("706x534")
    root.title('Testing GUI')
    root.configure(bg='#3A3B3C')

    intro = tk.Label(root, text = 'Upload Files and Display', bg ='#3A3B3C', fg = 'white')
    intro.grid(row = 0, column = 2, padx=5)

    upload = tk.Button(root, text = 'Upload Files', width = 20, bg ='#3A3B3C', fg = 'white', command =lambda:open_image())
    upload.grid(row = 1, column = 2, padx=5)
    
    root.mainloop() #allows the window to stay open

""" 
To Do:
    i) Rectangular Image Select - John
    ii) Grid Layout understanding - Brady
    iii) Save the GUI info
    1) Add adjustable threshold values with a default to start (DT & IT)
    2) Add the perfusion value
    3) Make image size larger
    4) Make GUI look appealing (buttons all on one side, items properly spaced, etc.)
    5) Work on zooming in on the image, showing the percentage the pixels take up of perfusion value
    """
