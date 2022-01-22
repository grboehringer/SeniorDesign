from tkinter import *
from PIL import ImageTk, Image

root = Tk()
root.title('Testing GUI')
#filepath on my computer, a filepath is only needed if the photo is not running in the same location as the code
# root.iconbitmap('C:\Users\Johns\Desktop\School\BME 590\SeniorDesign')

#tells software what photo to open, would like to learn how to make this so the user doesn't have to name their photo's 'test.jpg'
myImage = ImageTk.PhotoImage(Image.open("test.jpg"))
myLabel = Label(image = myImage)
myLabel.pack()

#button that allows the user to exit the program
buttonExit = Button(root, text = "Exit Program", command = root.quit)
buttonExit.pack()




root.mainloop()