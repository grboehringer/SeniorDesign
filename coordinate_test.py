from tkinter import *
from PIL import Image, ImageTk

class Window(Frame):

    def __init__(self, master=None):
        Frame.__init__(self, master)

        self.master = master
        self.pos = []
        self.master.title("GUI")
        self.pack(fill=BOTH, expand=1)

        self.counter = 0

        menu = Menu(self.master)
        self.master.config(menu=menu)

        file = Menu(menu)
        file.add_command(label="Exit", command=self.client_exit)
        menu.add_cascade(label="File", menu=file)
        analyze = Menu(menu)

        analyze.add_command(label="Region of Interest", 
        command=self.regionOfInterest)

        menu.add_cascade(label="Analyze", menu=analyze)
        load = Image.open("images/Instructions.jpg")
        render = ImageTk.PhotoImage(load)

        img = Label(self, image=render)
        img.image = render
        img.place(x=0, y=0)

    def regionOfInterest(self):
        root.config(cursor="plus")
        canvas.bind("<Button-1>", self.imgClick)


    def client_exit(self):
        exit()

    def imgClick(self, event):

        if self.counter < 3:
            x = canvas.canvasx(event.x)
            y = canvas.canvasy(event.y)
            self.pos.append((x, y))
            print(self.pos)
            canvas.create_line(x - 5, y, x + 5, y, fill="red", tags="crosshair")
            canvas.create_line(x, y - 5, x, y + 5, fill="red", tags="crosshair")
            self.counter += 1
        else:
            canvas.unbind("<Button 1>")
            root.config(cursor="arrow")
            self.counter = 0


root = Tk()
imgSize = Image.open("images/Instructions.jpg")
tkimage =  ImageTk.PhotoImage(imgSize)
w, h = imgSize.size

canvas = Canvas(root, width=w, height=h)
canvas.create_image((w/2,h/2),image=tkimage)
canvas.pack()

root.geometry("%dx%d"%(w,h))
app = Window(root)
root.mainloop() 