from tkinter import *
from PIL import ImageTk, Image
from tkinter import filedialog as fd

perIndex = 55.5

root = Tk()
root.title('Testing GUI')
#filepath on my computer, a filepath is only needed if the photo is not running in the same location as the code
# root.iconbitmap('C:\Users\Johns\Desktop\School\BME 590\SeniorDesign')

#finding the filename
def select_file():
    
    # define allowed file types
    filetypes = (
        ('Image files', '*.jpg'),
        ('All files', '*.*')
    )

        # prompt dialog box
    filename = fd.askopenfilename(
        title='Open an image',
        initialdir='/',
        filetypes=filetypes)
        
    return filename

def importImg(filename):
    #tells software what photo to open
    #myImage = ImageTk.PhotoImage(Image.open(filename))
    #myLabel = Label(image = myImage)
    #myLabel.pack()

    image = Image.open(filename)
    image.Label(image)

#creating a label for the perfusion index, using a filler value now
perfusion = Label(root, text = "Perfusion Index = " + str(perIndex))

#button that allows the user to exit the program
buttonExit = Button(root, text = "Exit Program", command = root.quit)
#buttonExit.pack(expand=YES)

#Grid layout for the GUI
buttonExit.grid(row = 1, column = 1)
perfusion.grid(row = 2, column = 0, columnspan = 3)

filename = select_file()
importImg(filename)



root.mainloop()