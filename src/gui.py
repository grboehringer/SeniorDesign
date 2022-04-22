from perfusion import *     # Connects Perfusion.py file
import tkinter as tk        # Imports tkinter library
from tkinter import *       # Imports tkinter functions
from PIL import Image, ImageTk  # Image Import
from tkinter.filedialog import askopenfilename  # Get filename
import json
import os

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

        # Settings Window Defaults
        d_pid = "[Enter Patient ID]"
        self.new_pid = d_pid
        d_gain = "[Enter Gain Value]"
        self.new_gain = d_gain
        d_zoom = "[Enter Zoom Value]"
        self.new_zoom = d_zoom
        d_frameavg = "[Enter Frame Average Value]"
        self.new_frameavg = d_frameavg
        d_thresh = "[Enter Threshold Percentage Value]"
        self.new_thresh = d_thresh
        d_samplevol = "[Enter Sample Volume Value]"
        self.new_samplevol = d_samplevol
        d_wallfilt = "[Enter Wall Filter Value]"
        self.new_wallfilt = d_wallfilt
        d_freq = "[Enter Frequency Value]"
        self.new_freq = d_freq
        

        # JSON Variables
        self.patient_ID = None
        self.gain = None
        self.zoom = None
        
        # Main menu
        menu = Menu(self.master)
        self.master.config(menu=menu)

        """File drop down."""
        self.file = Menu(menu, tearoff=False)
        menu.add_cascade(label="File", menu=self.file)
        self.file.add_command(label="Upload Image", command=self.upload_image)
        self.file.add_command(label="Save Image Data", command=self.save_all)

        # Settings Sub Menu
        self.sub_menu = Menu(menu, tearoff=False)
        self.sub_menu.add_command(label = 'Edit Settings', command=self.settings)
        self.sub_menu.add_command(label = 'Preset 1', command = self.preset_1)
        self.sub_menu.add_command(label = 'Preset 2', command = self.preset_2)
        self.sub_menu.add_command(label = 'Preset 3', command = self.preset_3)
        self.file.add_cascade(label="Settings", menu=self.sub_menu)

        self.file.add_command(label="Exit", command=self.client_exit)
        
        self.file.entryconfig("Save Image Data", state="disabled")
        self.file.entryconfig("Settings", state="disabled")
                
        """Analyze drop down."""
        self.analyze = Menu(menu, tearoff=False)
        menu.add_cascade(label="Analyze", menu=self.analyze)
        self.analyze.add_command(label="Region of Interest", command=self.regionOfInterest)
        self.analyze.add_command(label="Compare Images", command=self.compare_images)
        self.analyze.add_command(label="Calibrate Machine", command=self.calibrate_machine)
        
        self.analyze.entryconfig("Region of Interest", state="disabled")
        self.analyze.entryconfig("Compare Images", state="disabled")
        self.analyze.entryconfig("Calibrate Machine", state="disabled")
        
        self.initial_image()

    def initial_image(self):
        self.grid()
        self.canvas = Canvas(self,width=600, height=600)
        self.canvas.grid(row = 2,column = 0,columnspan=20)

        """Instructions image upload."""
        load = Image.open("images/Instructions.jpg")
        (w,h) = load.size
        self.canvas.config(width=w,height=h)
        self.render = ImageTk.PhotoImage(load)
        self.canvas.create_image(int(w/2),int(h/2),image=self.render)
        """Sets window size"""

        self.pid = tk.Label(self, text = '')
        self.pv = tk.Label(self, text = '')

    """ MENU FUNCTIONS """
    
    def upload_image(self):
        """Open the selected image and resize."""
        self.filename = self.select_file()
        self.load = Image.open(self.filename)
        (w,h) = self.load.size
        self.canvas.config(width=w,height=h)
        self.render = ImageTk.PhotoImage(self.load)
        self.canvas.create_image(int(w/2),int(h/2),image=self.render)

        self.pid.destroy()
        self.pv.destroy()
        self.perfusion_value = self.perfusion.image(self.filename)
        print(self.perfusion_value)
        self.pid = tk.Label(self, text = 'Patient ID: [Enter Patient ID in Settings]')
        self.pid.grid(row = 0, column = 0, pady=5)
        self.pv = tk.Label(self, text = 'PV:' + str(format(self.perfusion_value,'.2f')))
        self.pv.grid(row = 0, column = 1, pady=5)
        self.new_pid = "[Enter Patient ID]"

        # Enable menu functions
        self.analyze.entryconfig("Region of Interest", state="normal")
        self.analyze.entryconfig("Compare Images", state="normal")
        self.analyze.entryconfig("Calibrate Machine", state="normal")
        self.file.entryconfig("Save Image Data", state="normal")
        self.file.entryconfig("Settings", state="normal")

    def save_all(self):
        """Save image and associated data to file"""
        image_data = {
            'value': self.perfusion_value,
            'threshold': self.perfusion.differenceThreshold,
            'pid': self.patient_ID,
            'gain': self.gain,
            'zoom': self.zoom
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
        alg_set = tk.Label(self.root2, text = "Patient Algorithm Settings", bg ='#3A3B3C', fg = 'white', font=("Arial Bold", 10))

        id = tk.Label(self.root2, text = 'Patient ID:', bg ='#3A3B3C', fg = 'white', font=("Arial", 9))
        self.patient_ID = Entry(self.root2)
        
        diff_threshold = Label(self.root2, text="Difference Threshold:",bg ='#3A3B3C', fg = 'white', font=("Arial", 9))
        self.diff_thresh_entry = Entry(self.root2)

        mach_set = tk.Label(self.root2, text = "Patient Machine Settings", bg ='#3A3B3C', fg = 'white', font=("Arial Bold", 10))

        gain_val = Label(self.root2, text="Gain Value:", bg ='#3A3B3C', fg = 'white', font=("Arial", 9))
        self.gain_val_entry = Entry(self.root2)

        zoom_val = Label(self.root2, text="Zoom Value:", bg ='#3A3B3C', fg = 'white', font=("Arial", 9))
        self.zoom_val_entry = Entry(self.root2)

        frame_avg_val = Label(self.root2, text="Frame Average:", bg ='#3A3B3C', fg = 'white', font=("Arial", 9))
        self.frame_avg_val_entry = Entry(self.root2)

        thresh_val = Label(self.root2, text="Threshold (%):", bg ='#3A3B3C', fg = 'white', font=("Arial", 9))
        self.thresh_val_entry = Entry(self.root2)

        sample_vol_val = Label(self.root2, text="Sample Volume:", bg ='#3A3B3C', fg = 'white', font=("Arial", 9))
        self.sample_vol_val_entry = Entry(self.root2)

        wall_filter_val = Label(self.root2, text="Wall Filter:", bg ='#3A3B3C', fg = 'white', font=("Arial", 9))
        self.wall_filter_val_entry = Entry(self.root2)

        frequency_val = Label(self.root2, text="Frequency:", bg ='#3A3B3C', fg = 'white', font=("Arial", 9))
        self.frequency_val_entry = Entry(self.root2)

        # Display and Organize User Entries (Label & Box)
        alg_set.grid(row = 1, column = 1, columnspan=2, padx=10, pady=5)
        
        id.grid(row = 2, column = 1, padx=10, pady=5, sticky='w')
        self.patient_ID.grid(row = 2, column = 2, padx=5, pady=5)
        self.patient_ID.insert(0,self.new_pid)

        diff_threshold.grid(row=3, column=1, padx=10, pady=5, sticky='w')
        self.diff_thresh_entry.grid(row=3, column=2, padx=5, pady=5)
        self.diff_thresh_entry.insert(0,self.perfusion.differenceThreshold)

        mach_set.grid(row = 4, column = 1, columnspan=2, padx=10, pady=5)

        gain_val.grid(row=5, column=1, padx=10, pady=5, sticky='w')
        self.gain_val_entry.grid(row=5, column=2, padx=5, pady=5)
        self.gain_val_entry.insert(0,self.new_gain)

        zoom_val.grid(row=6, column=1, padx=10, pady=5, sticky='w')
        self.zoom_val_entry.grid(row=6, column=2, padx=5, pady=5)
        self.zoom_val_entry.insert(0,self.new_zoom)

        frame_avg_val.grid(row=7, column=1, padx=10, pady=5, sticky='w')
        self.frame_avg_val_entry.grid(row=7, column=2, padx=5, pady=5)
        self.frame_avg_val_entry.insert(0,self.new_frameavg)

        thresh_val.grid(row=8, column=1, padx=10, pady=5, sticky='w')
        self.thresh_val_entry.grid(row=8, column=2, padx=5, pady=5)
        self.thresh_val_entry.insert(0,self.new_thresh)

        sample_vol_val.grid(row=9, column=1, padx=10, pady=5, sticky='w')
        self.sample_vol_val_entry.grid(row=9, column=2, padx=5, pady=5)
        self.sample_vol_val_entry.insert(0,self.new_samplevol)

        wall_filter_val.grid(row=10, column=1, padx=10, pady=5, sticky='w')
        self.wall_filter_val_entry.grid(row=10, column=2, padx=5, pady=5)
        self.wall_filter_val_entry.insert(0,self.new_wallfilt)

        frequency_val.grid(row=11, column=1, padx=10, pady=5, sticky='w')
        self.frequency_val_entry.grid(row=11, column=2, padx=5, pady=5)
        self.frequency_val_entry.insert(0,self.new_freq)

        # x = variable.get() can store entry
        enter_sel = tk.Button(self.root2, text = "Enter", bg ='#3A3B3C', fg = 'white', font=("Arial Bold", 9), command =self.enter_selections)
        enter_sel.grid(row = 12, column = 1, columnspan = 2, padx=5, pady=5, ipadx=100)

        # Adding presets to the settings
            
    def preset_1(self): 
        print("Add preset 1")   
    def preset_2(self):        
        print("Add preset 3")
    def preset_3(self):
        print("Add preset 3")

    def enter_selections(self):
        """Save entered data and put into algorithm or display"""
        self.root2.bind('<Return>',self.perfusion.changeThreshold(int(self.diff_thresh_entry.get())))
        print(self.perfusion.differenceThreshold)
        self.new_perfusion_value = self.perfusion.image(self.filename)

        # Update PID and PV values
        self.new_pid = self.patient_ID.get()
        self.pid['text'] = 'Patient ID: ' + str(format(self.new_pid))
        self.pv['text'] = 'PV: ' + str(format(self.new_perfusion_value,'.2f'))
        
        # Update Settings Values
        self.new_gain = self.gain_val_entry.get()
        self.new_zoom = self.zoom_val_entry.get()
        self.new_frameavg = self.frame_avg_val_entry.get()
        self.new_thresh = self.thresh_val_entry.get()
        self.new_samplevol = self.sample_vol_val_entry.get()
        self.new_wallfilt = self.wall_filter_val_entry.get()
        self.new_freq = self.frequency_val_entry.get()

        # Removed because this caused the overlay issue
        # self.root2.destroy()
    
    def cal_selections(self):
        """Save entered data and put into algorithm or display"""
        self.root3.bind('<Return>',self.perfusion.changeThreshold(int(self.perfusion.differenceThreshold)))
        print(self.perfusion.differenceThreshold)
        self.new_perfusion_value = self.perfusion.image(self.filename)
        self.pv['text'] = 'PV: ' + str(format(self.new_perfusion_value,'.2f'))

    def calibrate_machine(self):
        """Instructions Window Creation"""
        self.info = Tk()
        self.info.title('Calibration Instructions')
        self.info.configure(bg='#3A3B3C')

        # Window Information
        info_msg = tk.Label(self.info, text = "To calibrate correctly select the color that represents the slowest motion first.\n Then select the fastest motion.", bg ='#3A3B3C', fg = 'white', font=("Arial Bold", 10))
        info_msg.grid(row = 1, column = 1, columnspan = 2, padx=10, pady=5, ipady=5)

        sel_img = tk.Button(self.info, text = "Continue", width = 15, bg = '#3A3B3C', fg = 'white', command = self.destroy_window)
        sel_img.grid(row = 2, column = 1, columnspan = 2, padx=5, pady=5)

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
        info_msg = tk.Label(self.compare_inst, text = "The first perfusion value being compared is the current image's. Select a second image to compare it with.", bg ='#3A3B3C', fg = 'white', font=("Arial", 10))
        info_msg.grid(row = 1, column = 1, columnspan = 2, padx=10, pady=5, ipady=5)
        
        info_msg = tk.Label(self.compare_inst, text = "IMPORTANT: Make sure image PIDs and ultrasound machine settings are the same!", bg ='#3A3B3C', fg = 'white', font=("Arial Bold", 10))
        info_msg.grid(row = 2, column = 1, columnspan = 2, padx=10, pady=5, ipady=5)

        sel_img = tk.Button(self.compare_inst, text = "Select Image", width = 15, bg = '#3A3B3C', fg = 'white', command = self.calc_comp)
        sel_img.grid(row = 3, column = 1, columnspan = 2, padx=5, pady=5)

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
            #self.cropped_image(self.pos[0][0], self.pos[0][1], self.pos[1][0], self.pos[1][1])
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
        self.save_coordinates.destroy()

        #crop image and display to window
        self.cropped_img = self.load.crop((int(self.pos[0][0]), int(self.pos[0][1]), int(self.pos[1][0]), int(self.pos[1][1])))
        (w,h) = self.cropped_img.size
        self.canvas.config(width=w,height=h)
        self.render = ImageTk.PhotoImage(self.cropped_img)
        self.canvas.create_image(int(w/2),int(h/2),image=self.render)

        # send to image to perfusion.py to get new perfusion value
        filename, extension = os.path.splitext(self.filename)
        self.cropped_img.save(filename + "_cropped" + extension)
        self.filename = filename + "_cropped" + extension
        self.cper_val = self.perfusion.image(self.filename)
        self.pv['text'] = 'PV:' + str(format(self.cper_val,'.2f'))

        # Reset ROI variables to default
        self.canvas.delete("crosshair")
        self.pos = []
        self.counter = 0
        self.canvas.unbind("<Button 1>")
        root.config(cursor="arrow")

    def delete_coord(self):
        """Delete selection coordinates"""
        self.canvas.delete("crosshair")
        self.pos = []
        self.counter = 0
        self.canvas.unbind("<Button 1>")
        root.config(cursor="arrow")
        self.save_coordinates.destroy()

    """Calibrate Machine Sub Function"""
    def mouseRGB(self, event):

        if self.counter < 1:
            x = int(self.canvas.canvasx(event.x))
            y = int(self.canvas.canvasy(event.y))

            self.pos.append((x, y))
            self.canvas.create_line(x - 5, y, x + 5, y, fill="red", tags="crosshair")
            self.canvas.create_line(x, y - 5, x, y + 5, fill="red", tags="crosshair")
            self.counter += 1
            # print(self.counter)
            # print(x)
            # print(y)

            redMin, greenMin, blueMin = self.perfusion.rgb(x,y)
            # print(f"RGB Format: r: {int(red)} g: {int(green)} b: {int(blue)}")
            # print("Coordinates of pixel: X: ",x,"Y: ",y)
            # print(f'Calibrated Threshold: {blue}')
            """Display RGB at Bottom"""
            self.root3 = tk.Tk()
            self.root3.title('Calibration Threshold')
            bot_R = Label(self.root3, text =f'RMin: {redMin}', fg='red')
            bot_R.grid(row = 1, column = 1, padx=10, pady=1, sticky='e')
            bot_G = Label(self.root3, text =f'GMin: {greenMin}', fg='green')
            bot_G.grid(row = 1, column = 2, padx=10, pady=1, sticky='e')
            bot_B = Label(self.root3, text =f'BMin: {blueMin}', fg='blue')
            bot_B.grid(row = 1, column = 3, padx=10, pady=1, sticky='e')
            cal_thresh = int(redMin) - int(blueMin) -1
            bot_C_Threshold = Label(self.root3, text = f'Calibrated Threshold: {cal_thresh}', fg = 'black')
            bot_C_Threshold.grid(row = 1, column = 4, padx=10, pady=1, sticky='e')

            # auto update the threshold value
            self.perfusion.differenceThreshold = cal_thresh
            self.new_perfusion_value = cal_thresh
            
            # Button to rerun the PV calculation after calibrated
            enter_sel = tk.Button(self.root3, text = "Change Threshold", bg = 'White', fg = 'Black', font=("Arial Bold", 9), command =self.cal_selections)
            enter_sel.grid(row = 12, column = 3, columnspan = 1)

        elif self.counter < 2:
            x1 = int(self.canvas.canvasx(event.x))
            y1 = int(self.canvas.canvasy(event.y))

            self.pos.append((x1, y1))
            self.canvas.create_line(x1 - 5, y1, x1 + 5, y1, fill="red", tags="crosshair")
            self.canvas.create_line(x1, y1 - 5, x1, y1 + 5, fill="red", tags="crosshair")
            self.counter += 1
            # print(self.counter)
            # print(x1)
            # print(y1)

            redMax, greenMax, blueMax = self.perfusion.rgb(x1,y1)
            """The max perfusion possible"""
            max_perf = (int(redMax)+int(greenMax)+int(blueMax))/3
           
            bot_R_M = Label(self.root3, text =f'RMax: {redMax}', fg='red')
            bot_R_M.grid(row = 2, column = 1, padx=10, pady=1, sticky='e')
            bot_G_M = Label(self.root3, text =f'GMax: {greenMax}', fg='green')
            bot_G_M.grid(row = 2, column = 2, padx=10, pady=1, sticky='e')
            bot_B_M = Label(self.root3, text =f'BMax: {blueMax}', fg='blue')
            bot_B_M.grid(row = 2, column = 3, padx=10, pady=1, sticky='e')
            bot_C_MaxPerf= Label(self.root3, text = 'Calibrated Max Perfusion: ' + format(max_perf,'.2f'), fg = 'black')
            bot_C_MaxPerf.grid(row = 2, column = 4, padx=10, pady=1, sticky='e')

        else:
            self.canvas.delete("crosshair")
            self.pos = []
            self.counter = 0
            self.canvas.unbind("<Button 1>")

    def destroy_window(self):
        self.kill = self.info.destroy()

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
        title_msg = tk.Label(self.compare_show, text = "Image PV Comparison", bg ='#3A3B3C', fg = 'white', font=("Arial Bold", 14))
        title_msg.grid(row = 1, column = 1, columnspan = 2, padx=10, pady=5, ipady=5)
        
        # NEED TO ADD PATIENT ID BUT ITS BUGGY RIGHT NOW
        # if self.patient_ID == None:
        #     pass
        # else:
        #     pid = tk.Label(self.compare_show, text = "PID: " + str(format(self.patient_ID.get())), bg ='#3A3B3C', fg = 'white', font=("Arial", 10))
        #     pid.grid(row = 2, column = 1, columnspan = 2, padx=10)

        img_1 = tk.Label(self.compare_show, text = "Image 1: " + self.filename, bg ='#3A3B3C', fg = 'white', font=("Arial", 10))
        img_1.grid(row = 3, column = 1, columnspan = 2, padx=10)

        img_2 = tk.Label(self.compare_show, text = "Image 2: " + self.filename_2, bg ='#3A3B3C', fg = 'white', font=("Arial", 10))
        img_2.grid(row = 4, column = 1, columnspan = 2, padx=10)

        pv1 = tk.Label(self.compare_show, text = "Perfusion Value 1: " + str(format(pv_compare_1,'.2f')), bg ='#3A3B3C', fg = 'white', font=("Arial", 10))
        pv1.grid(row = 5, column = 1, columnspan = 2, padx=10)

        pv2 = tk.Label(self.compare_show, text = "Perfusion Value 2: " + str(format(pv_compare_2,'.2f')), bg ='#3A3B3C', fg = 'white', font=("Arial", 10))
        pv2.grid(row = 6, column = 1, columnspan = 2, padx=10)

        comparison = tk.Label(self.compare_show, text = "Comparison (Image 2 - Image 1): " + str(format(compare_PV,'.2f')), bg ='#3A3B3C', fg = 'white', font=("Arial", 10))
        comparison.grid(row = 7, column = 1, columnspan = 2, padx=10)

    def disable_event(self):
        pass

if __name__ == '__main__':

    root = Tk()
    app = Window(root)
    root.mainloop() 