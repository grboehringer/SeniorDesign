import cv2 

# Coordinate selection
# Revamp perfusion index value

# function to display the coordinates of
# of the points clicked on the image
def select_coordinates(event, x, y, flags, params):
	# checking for left mouse clicks
	if event == cv2.EVENT_LBUTTONDOWN:

		# displaying the coordinates
		# on the Shell
		print(x, ' ', y)

# driver function
if __name__=="__main__":

	# setting mouse handler for the image
	# and calling the click_event() function
	cv2.setMouseCallback('Perfusion Index', select_coordinates)

	# wait for a key to be pressed to exit
	cv2.waitKey(0)

	# close the window
	cv2.destroyAllWindows()


if __name__ == '__main__':
    print("This is main rn")