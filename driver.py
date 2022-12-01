from mosaic import *

try:
    image = input("Enter image name: ")
    img = cv2.imread(image + ".png", cv2.IMREAD_COLOR)
except:
    print("Can't find that file")
    exit()    

size = int(input("Enter unit size: "))
mosaic = MosaicImage(ref_img=img, unit_size=size, enable_debug=False)
print(mosaic)
#show_image(mosaic.resized_img)
show_image(mosaic.generate_collage())
