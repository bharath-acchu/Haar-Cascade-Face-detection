# USAGE
# tkinter_test.py

# import the necessary packages
from tkinter import *
from PIL import Image
from PIL import ImageTk
from tkinter import filedialog
import time

import cv2
import numpy as np



def draw_rectangle(faces,img_copy):
    for (x,y,w,h) in faces:
      		cv2.rectangle(img_copy, (x, y), (x+w, y+h), (300, 0, 0), 2)
    return img_copy
    

def select_image():
	# grab a reference to the image panels
	global panelA, panelB

	# open a file chooser dialog and allow the user to select an input
	# image
	path = filedialog.askopenfilename()

	# ensure a file path was selected
	if len(path) > 0:
		# load the image from disk, convert it to grayscale, and detect
		# edges in it
		image = cv2.imread(path)
		img_copy = np.copy(image)
		face_cascade = cv2.CascadeClassifier('haarcascade_frontalface_default.xml')

		gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
		# Detect faces
		faces = face_cascade.detectMultiScale(gray, 1.1, 8)
		img_copy = draw_rectangle(faces,img_copy)

		# OpenCV represents images in BGR order; however PIL represents
		# images in RGB order, so we need to swap the channels
		image = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)
		img_copy =cv2.cvtColor(img_copy,cv2.COLOR_BGR2RGB)
		# convert the images to PIL format...
		image = Image.fromarray(image)
		img_copy = Image.fromarray(img_copy)

		# ...and then to ImageTk format
		image = ImageTk.PhotoImage(image)
		img_copy = ImageTk.PhotoImage(img_copy)

		# if the panels are None, initialize them
		if panelA is None or panelB is None:
			# the first panel will store our original image
			panelA = Label(root,image=image)
		
			panelA.image = image
			
			
			panelA.pack(side="left",padx=10, pady=10)


			# while the second panel will store the detected img
			panelB = Label(image=img_copy)
			panelB.image = img_copy
			panelB.pack(side="right", padx=10, pady=10)
			

		# otherwise, update the image panels
		else:
			# update the pannels
			panelA.configure(image=image)
			panelB.configure(image=img_copy)
			panelA.image = image
			panelB.image = img_copy


# initialize the window toolkit along with the two image panels
root = Tk()
panelA = None
panelB = None


# create a button, then when pressed, will trigger a file chooser
# dialog and allow the user to select an input image; then add the
# button the GUI
btn = Button(root, text="Select an image", command=select_image)
btn.pack(side="bottom", fill="both", expand="yes", padx="50", pady="40")


# kick off the GUI
root.mainloop()