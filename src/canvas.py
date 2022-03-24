import tkinter as tk
from tkinter.constants import *
from PIL import Image, ImageTk
import time

from matplotlib import image

root = tk.Tk()
root.geometry("750x750")

canvas = tk.Canvas(width=600, height=600, bg='black')
canvas.pack(expand=YES, fill=BOTH)
load = Image.open("images/test.jpg")
render = ImageTk.PhotoImage(load)
image_container = canvas.create_image(50, 10, image=render, anchor=NW)

time.sleep(5)

load = Image.open("images/Instructions.jpg")
render = ImageTk.PhotoImage(load)
canvas.itemconfig(image_container, image=render)

root.mainloop()