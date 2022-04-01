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
        self.file = Menu(menu, tearoff=False)
        menu.add_cascade(label="File", menu=self.file)
        self.file.add_command(label="Upload Image", command=self.upload_image)
        self.file.add_command(label="Save Image and Data", command=self.save_all)
        self.file.add_command(label="Settings", command=self.settings)
        self.file.add_command(label="Calibrate Machine", command=self.calibrate_machine)
        self.file.add_command(label="Exit", command=self.client_exit)

        self.file.entryconfig("Calibrate Machine", state="disabled")
        
        """Analyze drop down."""
        self.analyze = Menu(menu, tearoff=False)
        menu.add_cascade(label="Analyze", menu=self.analyze)
        self.analyze.add_command(label="Region of Interest", command=self.regionOfInterest)
        self.analyze.add_command(label="Compare Images", command=self.compare_images)

        self.analyze.entryconfig("Compare Images", state="disabled")

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
        txt ="P ID: [Enter Patient ID in Settings] \nPV:" + str(format(self.perfusion_value,'.2f'))
        self.txt_id = self.canvas.create_text(200, 50,fill="white",font="Times 20",text=txt,tag="txt")
        # Display Threshold

        # Enable menu functions
        self.analyze.entryconfig("Compare Images", state="normal")
        self.file.entryconfig("Calibrate Machine", state="normal")

    def save_all(self):
        """Save image and associated data to file"""
        image_data = {
            'value': self.perfusion_value,
            'threshold': self.perfusion.differenceThreshold,
            'pid': self.patient_ID,
            'gain': self.gain,
            'gain': self.zoom
        }
        try:
            with open('images.json') as file:
                data = json.load(file)
                data[self.filename] = image_data
        except:
            data = {
                self.filename: image_data
            }
        finally:
            with open('images.json', 'w') as file:
                json.dump(data, file)
            
        
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
        self.gain_val_entry = Entry(self.root2)

        zoom_val = Label(self.root2, text="Zoom Value:", bg ='#3A3B3C', fg = 'white')
        self.zoom_val_entry = Entry(self.root2)

        # Display and Organize User Entries (Label & Box)
        id.grid(row = 1, column = 1, padx=10, pady=5, sticky='e')
        self.patient_ID.grid(row = 1, column = 2, padx=5, pady=5)
        self.patient_ID.insert(0,"[Enter Patient ID]")

        gain_val.grid(row=2, column=1, padx=10, pady=5, sticky='e')
        self.gain_val_entry.grid(row=2, column=2, padx=5, pady=5)
        self.gain_val_entry.insert(0,"[Enter Gain Value]")

        zoom_val.grid(row=3, column=1, padx=10, pady=5, sticky='e')
        self.zoom_val_entry.grid(row=3, column=2, padx=5, pady=5)
        self.zoom_val_entry.insert(0,"[Enter Zoom Value]")

        threshold_intensity.grid(row=4, column=1, padx=10, pady=5, sticky='e')
        self.intensity_thresh_entry.grid(row=4, column=2, padx=5, pady=5)
        self.intensity_thresh_entry.insert(0,self.perfusion.intensityThreshold)

        diff_threshold.grid(row=5, column=1, padx=10, pady=5, sticky='e')
        self.diff_thresh_entry.grid(row=5, column=2, padx=5, pady=5)
        self.diff_thresh_entry.insert(0,self.perfusion.differenceThreshold)

        # x = variable.get() can store entry
        enter_sel = tk.Button(self.root2, text = "Enter", bg ='#3A3B3C', fg = 'white',command =self.enter_selections)
        enter_sel.grid(row = 5, column = 1, columnspan = 2, padx=5, pady=5, sticky='e')
            
    def enter_selections(self):
        """Save entered data and put into algorithm or display"""
        self.root2.bind('<Return>',self.perfusion.changeThreshold(int(self.intensity_thresh_entry.get()),int(self.diff_thresh_entry.get())))
        print(self.perfusion.intensityThreshold) 
        print(self.perfusion.differenceThreshold)
        self.new_perfusion_value = self.perfusion.image(self.filename)
        txt ="P ID:" + self.patient_ID.get() + "\nPV: " + str(format(self.new_perfusion_value,'.2f'))
        self.root2.destroy()
        self.canvas.delete('txt')
        self.canvas.create_text(200,50,fill="white",font="Times 20",text=txt,tag="txt")

    def calibrate_machine(self):
        """Calibrate Ultrasound Machine"""
        self.canvas.bind("<Button-1>", self.mouseRGB)        

    def client_exit(self):
        """Exit program."""
        exit()

    def regionOfInterest(self):
        """Select ROI."""
        root.config(cursor="plus")
        self.canvas.bind("<Button-1>", self.imgClick)

    def compare_images(self):
        """Compare Images in new window"""

        # Compare Images Instruction Window Setup
        self.compare_inst = Tk()
        self.compare_inst.title('Compare Images')
        self.compare_inst.configure(bg='#3A3B3C')
        
        # Disable closing the window
        self.compare_inst.protocol("WM_DELETE_WINDOW", self.disable_event)
        
        # Window Information
        info_msg = tk.Label(self.compare_inst, text = "The first perfusion value being compared is the current image's. Select a second image to compare it with.", bg ='#3A3B3C', fg = 'white')
        info_msg.grid(row = 1, column = 1, columnspan = 2, padx=10, pady=5, ipady=5)
        
        sel_img = tk.Button(self.compare_inst, text = "Select Image", width = 15, bg = '#3A3B3C', fg = 'white', command = self.calc_comp)
        sel_img.grid(row = 2, column = 1, columnspan = 2, padx=5, pady=5)

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
            
            # Window Information
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
        if self.counter < 1:
            x = int(self.canvas.canvasx(event.x))
            y = int(self.canvas.canvasy(event.y))

            self.pos.append((x, y))
            self.canvas.create_line(x - 5, y, x + 5, y, fill="red", tags="crosshair")
            self.canvas.create_line(x, y - 5, x, y + 5, fill="red", tags="crosshair")

            red, green, blue = self.perfusion.rgb(x,y)
            # calibrated_threshold = abs(int(red) - int(green))
            print(f"RGB Format: r: {int(red)} g: {int(green)} b: {int(blue)}")
            print("Coordinates of pixel: X: ",x,"Y: ",y)
            print(f'Calibrated Threshold: {blue}')

            """Display RGB at Bottom"""
            self.root3 = tk.Tk()
            bot_R = Label(self.root3, text =f'R: {red}', fg='red')
            bot_R.grid(row = 1, column = 1, padx=10, pady=1, sticky='e')
            bot_G = Label(self.root3, text =f'G: {green}', fg='green')
            bot_G.grid(row = 1, column = 2, padx=10, pady=1, sticky='e')
            bot_B = Label(self.root3, text =f'B: {blue}', fg='blue')
            bot_B.grid(row = 1, column = 3, padx=10, pady=1, sticky='e')
            bot_C_Threshold = Label(self.root3, text = f'Calibrated Threshold: {blue}', fg = 'black')
            bot_C_Threshold.grid(row = 1, column = 4, padx=10, pady=1, sticky='e')
            self.counter += 1

        else:
            self.canvas.delete("crosshair")
            self.pos = []
            self.counter = 0
            self.canvas.unbind("<Button 1>")
            self.root3.destroy()

    def calc_comp(self):
        self.compare_inst.destroy()

        # Store Current (First) Image Info
        pv_compare_1 = self.perfusion.image(self.filename)

        # Select File and Store Second Image Info
        self.filename_2 = self.select_file()
        pv_compare_2 = self.perfusion.image(self.filename_2)

        # Calculate Difference
        compare_PV = pv_compare_2 - pv_compare_1
        
        # Compare Images Display Window Setup
        self.compare_show = Tk()
        self.compare_show.title('Compare Images')
        self.compare_show.configure(bg='#3A3B3C')

        # Window Information
        title_msg = tk.Label(self.compare_show, text = "PV Image Comparison", bg ='#3A3B3C', fg = 'white', font=("Arial Bold", 14))
        title_msg.grid(row = 1, column = 1, columnspan = 2, padx=10, pady=5, ipady=5)
        
        img_1 = tk.Label(self.compare_show, text = "Image 1: " + self.filename, bg ='#3A3B3C', fg = 'white', font=("Arial", 10))
        img_1.grid(row = 2, column = 1, columnspan = 2, padx=10, pady=5, ipady=5)

        img_2 = tk.Label(self.compare_show, text = "Image 2: " + self.filename_2, bg ='#3A3B3C', fg = 'white', font=("Arial", 10))
        img_2.grid(row = 3, column = 1, columnspan = 2, padx=10, pady=5, ipady=5)

        pv1 = tk.Label(self.compare_show, text = "Perfusion Value 1: " + str(format(pv_compare_1,'.2f')), bg ='#3A3B3C', fg = 'white', font=("Arial", 10))
        pv1.grid(row = 4, column = 1, columnspan = 2, padx=10, pady=5, ipady=5)

        pv2 = tk.Label(self.compare_show, text = "Perfusion Value 2: " + str(format(pv_compare_2,'.2f')), bg ='#3A3B3C', fg = 'white', font=("Arial", 10))
        pv2.grid(row = 5, column = 1, columnspan = 2, padx=10, pady=5, ipady=5)

        comparison = tk.Label(self.compare_show, text = "Comparison (Image 2 - Image 1): " + str(format(compare_PV,'.2f')), bg ='#3A3B3C', fg = 'white', font=("Arial", 10))
        comparison.grid(row = 6, column = 1, columnspan = 2, padx=10, pady=5, ipady=5)

    def disable_event(self):
        pass


if __name__ == '__main__':

    root = Tk()
    app = Window(root)
    root.mainloop() 