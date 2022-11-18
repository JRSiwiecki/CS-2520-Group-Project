from mosaic import *

try:
    img = cv2.imread("rainbow.png", cv2.IMREAD_COLOR)
except:
    print("Can't find that file")
    exit()    

mosaic = MosaicImage(ref_img=img, unit_size=60, enable_debug=True)
print(mosaic)
show_image(mosaic.resized_img)