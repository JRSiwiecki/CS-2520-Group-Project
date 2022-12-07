from mosaic import *
import os

# Before Running:

# Check if the dataset is populated with folders of images of colors.
# If it is not, then run data_grabber.py and allow for the folder to populate.

# How To Run:
# 
# 1. Place any .png images you'd like to generate a mosaic of inside the testimages folder (some samples provided)
# 2. Run driver.py
# 3. Enter the name of the image you'd like to create a mosaic for (do not enter the file extension).
# 4. Enter the size of each unit you'd like for the picture (smaller = more detail = longer runtime).
# 	    Good example unit size = 20
# 5. Wait for the mosaic to generate! 
# 6. When the mosaic is created, a window called "Result" will appear.
# 7. Click on the "Result" window and view the mosaic! Close the window when done viewing.
# 8. Enter y to generate another mosaic following steps 3-7 or press n to quit!

#try as long as user wants to continue
while True:
    #try as long as user enters in a non image
    while True:
        try:
            image = input("Enter image name: ")
            if image + ".png" not in os.listdir("testimages"):
                raise OSError
            else:
                break
        except OSError:
            print("Can't find that file") 

    img = cv2.imread("testimages/" + image + ".png", cv2.IMREAD_COLOR)

    #try as long as user enters in a noninteger
    while True:
        try:
            size = int(input("Enter unit size: "))
            if size <= 0:
                raise ValueError
            else:
                break
        except ValueError:
            print("Please enter only an integer.")

    #create the mosaic image
    mosaic = MosaicImage(ref_img=img, unit_size=size, enable_debug=False)
    mosaic.show()

    #ask as long as they enter in not n or y
    while True:
        answer = input("Would you like to go again? Y/N").lower()
        if answer == "n":
            exit()
        if answer == "y":
            break