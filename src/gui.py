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
        self.master.title("Perfusion Index")
        self.pack(fill=BOTH, expand=True)
        self.perfusion = Perfusion()

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
        analyze.add_command(label="Compare Images", command=self.compare_images)

        id = tk.Label(self, text = 'Patient ID:')
        id.pack(side = TOP, expand = True, fill = BOTH)

        """Instructions image upload."""

        load = Image.open("images/Instructions.jpg")
        render = ImageTk.PhotoImage(load)
        self.img = Label(self, image=render)
        self.img.image = render
        self.img.config(image = render)
        self.img.pack(side = TOP, expand = True, fill = BOTH)
        w, h = load.size

        """Figure out what this does!!!"""
        #self.canvas = Canvas(master, width=w, height=h)
        #self.canvas.create_image((w/2,h/2),image=render)
        #self.canvas.pack()

        # Try these for image thing
        # img = PhotoImage(file="python-tkinter-canvas-image-for-use.png")
        # canvas.create_image(370, 200, image=img)

        """Sets window???"""
        root.geometry("600x600")        # Why does the prefix "%dx%d"% need to be there?

    """ MENU FUNCTIONS """
    
    def upload_image(self):
        """Open the selected image and resize."""
        global filename
        w = 0
        h = 0
        self.img.config(image='')
        filename = self.select_file()
        load = Image.open(filename)
        render = ImageTk.PhotoImage(load)
        self.img.config(image = render)
        #self.img = Label(self, image=render)
        self.img.image = render
        self.img.pack(side = TOP, expand = True, fill = BOTH)
        w, h = load.size

        self.canvas = Canvas(root, width=w, height=h)
        self.canvas.create_image((w/2,h/2),image=render)
        self.canvas.pack()

        #self.threshold_display(filename,intensityThreshold,differenceThreshold)

    def save_all(self):
        """Save image and associated data to file"""
        print('Image and Data Function')
    
    def settings(self):
        """Allow thresholds and machine constants to be entered manually"""
        # Setup New Window
        root2 = tk.Tk()
        root2.title('Settings')
        root2.configure(bg='#3A3B3C')

        # Initialize User Entries
        id = tk.Label(root2, text = 'Patient ID:', bg ='#3A3B3C', fg = 'white')
        patient_ID = Entry(root2)
        
        threshold_intensity = Label(root2, text="Intensity Threshold:", bg ='#3A3B3C', fg = 'white')
        intensity_thresh_entry = Entry(root2)
        
        diff_threshold = Label(root2, text="Difference Threshold:",bg ='#3A3B3C', fg = 'white')
        diff_thresh_entry = Entry(root2)
        
        gain_val = Label(root2, text="Gain Value:", bg ='#3A3B3C', fg = 'white')
        gain_val_entry = Entry(root2)

        # Display and Organize User Entries (Label & Box)
        id.grid(row = 1, column = 1, padx=10, pady=5, sticky='e')
        patient_ID.grid(row = 1, column = 2, padx=5, pady=5)
        patient_ID.insert(0,"[Enter Patient ID]")

        gain_val.grid(row=2, column=1, padx=10, pady=5, sticky='e')
        gain_val_entry.grid(row=2, column=2, padx=5, pady=5)
        gain_val_entry.insert(0,"[Enter Gain Value]")

        threshold_intensity.grid(row=3, column=1, padx=10, pady=5, sticky='e')
        intensity_thresh_entry.grid(row=3, column=2, padx=5, pady=5)

        diff_threshold.grid(row=4, column=1, padx=10, pady=5, sticky='e')
        diff_thresh_entry.grid(row=4, column=2, padx=5, pady=5)

        # x = variable.get() can store entry

    def client_exit(self):
        """Exit program."""
        exit()
    
    def regionOfInterest(self):
        """Select ROI."""
        root.config(cursor="plus")
        self.canvas.bind("<Button-1>", self.imgClick)

    def compare_images(self):
        """Compare Images in new window"""
        print('Compare Images Function')

    """ SUBFUNCTIONS """

    def threshold_display(self, filename,intensityThreshold,differenceThreshold):
        """Update threshold values, perfusion value, and gain when changed by user."""
        perfusion = self.perfusion.algorithm(filename,intensityThreshold,differenceThreshold)
        perfusionVal = self.perfusion.finalVal(perfusion)


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
            x = self.canvas.canvasx(event.x)
            y = self.canvas.canvasy(event.y)
            self.pos.append((x, y))
            print(self.pos)
            self.canvas.create_line(x - 5, y, x + 5, y, fill="red", tags="crosshair")
            self.canvas.create_line(x, y - 5, x, y + 5, fill="red", tags="crosshair")
            self.counter += 1

        else:
            self.canvas.create_rectangle(self.pos[0][0], self.pos[0][1], self.pos[1][0], self.pos[1][1], outline="red", tags="crosshair")
            
            # Save Coordinates Window Setup
            self.save_coordinates = Tk()
            self.save_coordinates.title('Save Selection')
            self.save_coordinates.configure(bg='#3A3B3C')
            
            # Disable closing the window
            self.save_coordinates.protocol("WM_DELETE_WINDOW", self.disable_event)
            # ADD RESIZING LOCK
            
            coord_msg = tk.Label(self.save_coordinates, text = 'Would you like to save this selection?', bg ='#3A3B3C', fg = 'white')
            coord_msg.grid(row = 1, column = 1, columnspan = 2, padx=10, pady=5, ipady=5)
            
            save_sel = tk.Button(self.save_coordinates, text = "Save Selection", width = 15, bg ='#3A3B3C', fg = 'white',command =self.save_coord)
            save_sel.grid(row = 2, column = 1, padx=5, pady=5)
            
            del_sel = tk.Button(self.save_coordinates, text = "Delete Selection", width = 15, bg ='#3A3B3C', fg = 'white',command =self.delete_coord)
            del_sel.grid(row = 2, column = 2, padx=5, pady=5)

    def save_coord(self):
        """Save selection coordinates and crop image for perfusion"""
        print("save coord and crop")
        self.save_coordinates.destroy()
        # RERUN ALGORITHM HERE TO GET NEW PV WITH CROPPED IMAGE

    def delete_coord(self):
        """Delete selection coordinates"""
        self.canvas.delete("crosshair")
        self.pos = []
        self.counter = 0
        self.canvas.unbind("<Button 1>")
        root.config(cursor="arrow")
        self.save_coordinates.destroy()

    def disable_event(self):
        pass


if __name__ == '__main__':

    root = Tk()
    app = Window(root)
    root.mainloop() 