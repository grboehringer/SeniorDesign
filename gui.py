from tkinter import *
from PIL import ImageTk, Image

root = Tk()
root.title('Testing GUI')
# root.iconbitmap('C:\Users\Johns\Desktop\School\BME 590\SeniorDesign')

myImage = ImageTk.PhotoImage(Image.open("test.jpg"))
myLabel = Label(image = myImage)
myLabel.pack()


buttonExit = Button(root, text = "Exit Program", command = root.quit)
buttonExit.pack()




root.mainloop()