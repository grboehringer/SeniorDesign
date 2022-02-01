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
    img = img.resize((300,300))
    #image display code
    # Use this code if no image resizing is wanted/needed: img = ImageTk.PhotoImage(file = filename)
    img = ImageTk.PhotoImage(img)
    size = tk.Label(root)
    size.grid(row = 3, column = 1)
    size.image = img
    size['image'] = img

if __name__ == '__main__':
    perIndex = 55.5

    root = tk.Tk()
    root.geometry("410x300")
    root.title('Testing GUI')

    intro = tk.Label(root, text = 'Upload Files and Display')
    upload = tk.Button(root, text = 'Upload Files', width = 20, command =lambda:open_image())


    # Grid layout for GUI
    intro.grid(row = 1, column = 1, columnspan = 4)
    upload.grid(row = 2, column = 1, columnspan = 4)


    root.mainloop() #allows the window to stay open

""" 
To Do:
    1) Add adjustable threshold values with a default to start (DT & IT)
    2) Add the perfusion value
    3) Make image size larger
    4) Make GUI look appealing (buttons all on one side, items properly spaced, etc.)
    5) Work on zooming in on the image, showing the percentage the pixels take up of perfusion value
    """
