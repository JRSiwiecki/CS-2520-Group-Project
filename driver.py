from mosaic import *
import os

#try as long as user wants to continue
while True:
    #try as long as user enters in a non image
    while True:
        try:
            image = input("Enter image name: ")
            if image+".png" not in os.listdir():
                raise OSError
            else:
                break
        except OSError:
            print("Can't find that file") 

    img = cv2.imread(image + ".png", cv2.IMREAD_COLOR)

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