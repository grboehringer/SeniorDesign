from tkinter import *

# Event Handler

def select_coordinates(event, x, y, flags, params):
	# checking for left mouse clicks
	if event == cv2.EVENT_LBUTTONDOWN:

		# displaying the coordinates
		# on the Shell
		print(x, ' ', y)

if __name__ == '__main__':
    print("This is main rn. Run GUI.")