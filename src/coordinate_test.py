from perfusion import *     # Connects Perfusion.py file
import tkinter as tk        # Imports tkinter library
from tkinter import *       # Imports tkinter functions
from PIL import Image, ImageTk  # Image Import
from tkinter.filedialog import askopenfilename  # Get filename

class Window(Frame):

    def __init__(self, master=None):
        """Set up class and top menu."""
        Frame.__init__(self, master)

        self.master = master
        self.pos = []
        self.master.title("GUI")
        self.pack(fill=BOTH, expand=1)

        self.counter = 0

        menu = Menu(self.master)
        self.master.config(menu=menu)

        """File drop down."""
        file = Menu(menu)
        menu.add_cascade(label="File", menu=file)
        file.add_command(label="Upload Image", command=self.upload_image)
        file.add_command(label="Save Image and Data", command=self.save_all)
        file.add_command(label="Settings", command=self.settings)
        file.add_command(label="Exit", command=self.client_exit)
        
        """Analyze drop down."""
        analyze = Menu(menu)
        menu.add_cascade(label="Analyze", menu=analyze)
        analyze.add_command(label="Region of Interest", command=self.regionOfInterest)
        analyze.add_command(label="Save Selection", command=self.save_selection)

        """Instructions image upload."""
        load = Image.open("images/Instructions.jpg")
        render = ImageTk.PhotoImage(load)
        img = Label(self, image=render)
        img.image = render
        img.place(x=0, y=0)

    """ MENU FUNCTIONS """
    
    def upload_image(self):
        """Open the selected image and resize."""
        global filename
        filename = select_file()
        load = Image.open(filename)
        render = ImageTk.PhotoImage(load)
        img = Label(self, image=render)
        img.image = render
        img.place(x=0, y=0)
        
        #threshold_display(filename,intensityThreshold,differenceThreshold)

    def save_all(self):
        """Save image and associated data to file"""
        print('Image and Data Function')
    
    def settings(self):
        """Allow thresholds and gain to be set manually"""
        print('Threshold and gain settings')

    def client_exit(self):
        """Exit program."""
        exit()
    
    def regionOfInterest(self):
        """Select ROI."""
        root.config(cursor="plus")
        canvas.bind("<Button-1>", self.imgClick)

    def save_selection(self):
        """Save selection coordinates and crop image for perfusion"""
        print('Coordinate Selection Function')

    """ SUBFUNCTIONS """

    def threshold_display(filename,intensityThreshold,differenceThreshold):
        """Update threshold values, perfusion value, and gain when changed by user."""
        perfusion = algorithm(filename,intensityThreshold,differenceThreshold)
        perfusionVal = finalVal(perfusion)

        #intensity_thresh_entry.insert(0,intensityThreshold)

        #diff_thresh_entry.insert(0,differenceThreshold)

        #gain_val_entry.insert(0,"Enter Gain Value")

        #per_val_entry.insert(0,perfusionVal)

    def select_file(self):
        """Finds the filename."""
        # define allowed file types
        f_types = [('Jpg files', '*.jpg'), ('jpeg files', '*.jpeg'), ('PNG files','*.png')]

        # prompt dialog box
        filename = askopenfilename(filetypes = f_types)

        return filename

    def imgClick(self, event):
        """Selection counter, displays rectangle, and stores selection values"""
        if self.counter < 2:
            x = canvas.canvasx(event.x)
            y = canvas.canvasy(event.y)
            self.pos.append((x, y))
            print(self.pos)
            canvas.create_line(x - 5, y, x + 5, y, fill="red", tags="crosshair")
            canvas.create_line(x, y - 5, x, y + 5, fill="red", tags="crosshair")
            self.counter += 1
        else:
            canvas.create_rectangle(self.pos[0][0], self.pos[0][1], self.pos[1][0], self.pos[1][1], outline="red")
            canvas.unbind("<Button 1>")
            root.config(cursor="arrow")
            self.counter = 0

if __name__ == '__main__':
    """Gets image size"""
    root = Tk()
    imgSize = Image.open("images/test.jpg")
    tkimage =  ImageTk.PhotoImage(imgSize)
    w, h = imgSize.size

    """Figure out what this does!!!"""
    canvas = Canvas(root, width=w, height=h)
    canvas.create_image((w/2,h/2),image=tkimage)
    canvas.pack()

    """Sets window???"""
    root.geometry("%dx%d"%(w,h))        # Why does the prefix "%dx%d"% need to be there?
    #root.geometry("%dx%d"%(512,512))
    app = Window(root)
    root.mainloop() 