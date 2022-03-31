from perfusion import *     # Connects Perfusion.py file
import tkinter as tk        # Imports tkinter library
from tkinter import *       # Imports tkinter functions
from PIL import Image, ImageTk  # Image Import
from tkinter.filedialog import askopenfilename  # Get filename
import json

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
        file.add_command(label="Calibrate Machine", command=self.calibrate_machine)
        file.add_command(label="Exit", command=self.client_exit)
        
        """Analyze drop down."""
        analyze = Menu(menu)
        menu.add_cascade(label="Analyze", menu=analyze)
        analyze.add_command(label="Region of Interest", command=self.regionOfInterest)
        analyze.add_command(label="Compare Images", command=self.compare_images)

        """Instructions image upload."""
        load = Image.open("images/Instructions.jpg")
        self.render = ImageTk.PhotoImage(load)
        #h = self.render.height()
        #w = self.render.width()
        #self.canvas = Canvas(master, width=w, height=h)
        self.canvas = Canvas(master, width=512, height=512)
        self.canvas.pack()
        #self.img_id = self.canvas.create_image((w/2,w/2),image=self.render)
        self.img_id = self.canvas.create_image((512/2,512/2),image=self.render)
        """Sets window size"""
        #root.geometry(f'{w}x{h}')
        root.geometry("512x512")

    """ MENU FUNCTIONS """
    
    def upload_image(self):
        """Open the selected image and resize."""
        #self.canvas.delete('txt')
        #self.canvas.delete('img')
        self.filename = self.select_file()
        load = Image.open(self.filename)
        self.render = ImageTk.PhotoImage(load)
        self.canvas.itemconfig(self.img_id, image=self.render)
        #h = self.render.height()
        #w = self.render.width()
        #self.canvas = Canvas(self, width=w, height=h)
        #self.canvas.pack()
        #self.img_id=self.canvas.create_image((w/2,h/2), image=self.render,tag="img")
        #root.geometry(f'{w}x{h}')

        print(self.filename)
        self.perfusion_value = self.perfusion.image(self.filename)
        print(self.perfusion_value)
        txt ="P ID: [Enter Patient ID in Settings] \nPV:" + str(self.perfusion_value)
        self.txt_id = self.canvas.create_text(200, 50,fill="white",font="Times 20",text=txt,tag="txt")
        # Display Threshold

    def save_all(self):
        """Save image and associated data to file"""
        if (self.filename and self.perfusion_value):
            dictionary = {
                'filename': self.filename,
                'perfusion': self.perfusion_value
                }
            string = json.dumps(dictionary)
            with open('stuff.json', 'a') as file:
                file.write(string)
        
    def settings(self):
        """Allow thresholds and machine constants to be entered manually"""
        # Setup New Window
        self.root2 = tk.Tk()
        self.root2.title('Settings')
        self.root2.configure(bg='#3A3B3C')

        # Initialize User Entries
        id = tk.Label(self.root2, text = 'Patient ID:', bg ='#3A3B3C', fg = 'white')
        self.patient_ID = Entry(self.root2)
        
        threshold_intensity = Label(self.root2, text="Intensity Threshold:", bg ='#3A3B3C', fg = 'white')
        self.intensity_thresh_entry = Entry(self.root2)
        
        diff_threshold = Label(self.root2, text="Difference Threshold:",bg ='#3A3B3C', fg = 'white')
        self.diff_thresh_entry = Entry(self.root2)
        
        gain_val = Label(self.root2, text="Gain Value:", bg ='#3A3B3C', fg = 'white')
        gain_val_entry = Entry(self.root2)

        # Display and Organize User Entries (Label & Box)
        id.grid(row = 1, column = 1, padx=10, pady=5, sticky='e')
        self.patient_ID.grid(row = 1, column = 2, padx=5, pady=5)
        self.patient_ID.insert(0,"[Enter Patient ID]")

        gain_val.grid(row=2, column=1, padx=10, pady=5, sticky='e')
        gain_val_entry.grid(row=2, column=2, padx=5, pady=5)
        gain_val_entry.insert(0,"[Enter Gain Value]")

        threshold_intensity.grid(row=3, column=1, padx=10, pady=5, sticky='e')
        self.intensity_thresh_entry.grid(row=3, column=2, padx=5, pady=5)
        self.intensity_thresh_entry.insert(0,self.perfusion.intensityThreshold)

        diff_threshold.grid(row=4, column=1, padx=10, pady=5, sticky='e')
        self.diff_thresh_entry.grid(row=4, column=2, padx=5, pady=5)
        self.diff_thresh_entry.insert(0,self.perfusion.differenceThreshold)

        # x = variable.get() can store entry
        enter_sel = tk.Button(self.root2, text = "Enter", bg ='#3A3B3C', fg = 'white',command =self.enter_selections)
        enter_sel.grid(row = 5, column = 1, columnspan = 2, padx=5, pady=5, sticky='e')
            
    def calibrate_machine(self):
        """Calibrate Ultrasound Machine"""
        self.canvas.bind("<Button-1>", self.mouseRGB)

    def enter_selections(self):
        """Save entered data and put into algorithm or display"""
        self.root2.bind('<Return>',self.perfusion.changeThreshold(int(self.intensity_thresh_entry.get()),int(self.diff_thresh_entry.get())))
        print(self.perfusion.intensityThreshold) 
        print(self.perfusion.differenceThreshold)
        self.new_perfusion_value = self.perfusion.image(self.filename)
        txt ="P ID:" + self.patient_ID.get() + "\nPV: " + str(self.new_perfusion_value)
        self.root2.destroy()
        self.canvas.delete('txt')
        self.canvas.create_text(200,50,fill="white",font="Times 20",text=txt,tag="txt")
        

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

    def mouseRGB(self, event):
        """Calibrate Machine Sub Function"""
        # if event == cv2.EVENT_LBUTTONDOWN: #checks mouse left button down condition
        if self.counter < 1:
            x = self.canvas.canvasx(event.x)
            y = self.canvas.canvasy(event.y)

            self.pos.append((x, y))
            print(self.pos)
            self.canvas.create_line(x - 5, y, x + 5, y, fill="red", tags="crosshair")
            self.canvas.create_line(x, y - 5, x, y + 5, fill="red", tags="crosshair")

            colors = self.perfusion.rgb(x,y)
            # colorsR = self.canvas[y,x,0]
            # colorsG = self.canvas[y,x,1]
            # colorsB = self.canvas[y,x,2]
            # colors = self.canvas[y,x]
            # reverse = colors[::-1] #reverses BGR array
            # print("Red: ",colorsR)
            # print("Green: ",colorsG)
            # print("Blue: ",colorsB)
            print("RGB Format: ",colors)
            print("Coordinates of pixel: X: ",x,"Y: ",y)
            # """Display RGB at Bottom"""
            # bottom_status = Label(self.master,text= 'R: '+ colorsR + ' G: ' + colorsG + ' B: ' + colorsB)
            # bottom_status.grid(row=2, column=0, columnspan=3)

        else:
            self.canvas.delete("crosshair")
            self.pos = []
            self.counter = 0
            self.canvas.unbind("<Button 1>")

    def disable_event(self):
        pass


if __name__ == '__main__':

    root = Tk()
    app = Window(root)
    root.mainloop() 