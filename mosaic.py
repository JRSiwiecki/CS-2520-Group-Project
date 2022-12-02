import cv2
import colorsys
import numpy
import os
import random
from color import *

class MosaicImage:
    def __init__(self, ref_img, unit_size, enable_debug = False):
        self.unit_size = unit_size #how wide/tall each chunk that we are sampling is (for example, 60 px)

        self.ref_img = ref_img #the original image
        self.ref_height = ref_img.shape[0] #the height of the original image
        self.ref_width = ref_img.shape[1] #the width of the original image

        self.resize_height = self.ref_height - self.ref_height%unit_size #height of the resized image (divisible by unit size)
        self.resize_width = self.ref_width - self.ref_width%unit_size #width of the resized image (divisible by unit size)

        self.mosaic_height = self.resize_height // self.unit_size #how many chunks tall is our mosaic?
        self.mosaic_width = self.resize_width // self.unit_size #how many chunks wide is our mosaic?

        #resize the original to fit our new constraints
        self.resized_img = cv2.resize(self.ref_img, (self.resize_width, self.resize_height), interpolation=cv2.INTER_LINEAR)

        self.chunkify()

        if enable_debug:
            self.resized_img = self.debug_draw()
        else:
            self.set_sub_images()
            self.generate_collage()

    #returns a sub-image of the resized image
    def get_image_slice(self, r, c):
        x1 = c * self.unit_size
        x2 = x1 + self.unit_size
        y1 = r * self.unit_size
        y2 = y1 + self.unit_size
        unit = self.resized_img[x1:x2, y1:y2]
        return unit

    #split the image into chunks
    def chunkify(self):
        self.chunks = {}
        for r in range(self.mosaic_height):
            for c in range(self.mosaic_width):
                    sub_img = self.get_image_slice(c, r) #get the image at this location
                    color_RGB = averageColor(sub_img) #loop through all pixels and get average RGB
                    color_HSV = colorsys.rgb_to_hsv(color_RGB[0], color_RGB[1], color_RGB[2]) #turn the RGB into HSV
                    self.chunks[(c,r)] = Chunk(position=(c,r), size=self.unit_size, hsv=color_HSV) #create a new chunk and pass in HSV

    def set_sub_img(self, coor, img):
        self.chunks[coor].set_img(img)

    def set_sub_images(self):
        baseAdd = "./testdata/" #base address of data

        print("Setting sub images...")
        for r in range(self.mosaic_height):
            for c in range(self.mosaic_width):
                chunk = self.chunks[(c,r)] #get chunk at this location
                path = baseAdd + str(chunk.color) #get the path to the specific color folder
                image_pool = os.listdir(path) #grab a list of all files in that directory
                
                #remove files that we don't care about
                if "desktop.ini" in image_pool:
                    image_pool.remove("desktop.ini")
                
                random_image = path+"/"+random.choice(image_pool) #pick a random image
                img = cv2.imread(random_image, cv2.IMREAD_ANYCOLOR) #load the image
                self.set_sub_img((c,r), img) #set the chunk's sub image

    def debug_draw(self):
        #draw a line for each row
        for i in range(self.resize_height):
            draw_row(self.resized_img, self.unit_size, i, self.resize_height)
        #draw a line for each column
        for i in range(self.resize_width):
            draw_col(self.resized_img, self.unit_size, i, self.resize_width)
        #for every chunk
        if self.chunks:
            for r in range(self.mosaic_height):
                for c in range(self.mosaic_width):
                    #center of chunk
                    org = (c * self.unit_size, r * self.unit_size + self.unit_size//2)
                    #place text with its color index in that chunk
                    cv2.putText(img=self.resized_img, text=str(self.chunks[(c,r)].color.hue.value), org=org, fontFace=cv2.FONT_HERSHEY_TRIPLEX, fontScale=0.7, color=(255, 255, 255),thickness=2)
        return self.resized_img

    def generate_collage(self):
        rows = []
        print("Building columns...")
        #create an array of all columns
        for c in range(self.mosaic_width):
            row = []
            #make a list of rows
            for r in range(self.mosaic_height):
                row.append(self.chunks[(c,r)].img)
            #add row to rows list
            rows.append(numpy.vstack(row))
        #compress all rows
        columns = numpy.hstack(rows)
        self.collage = columns
        print("Collage generated!")
    
    def show(self):
        show_image(self.collage)
        
class Chunk:
    def __init__(self, position, size, hsv):
        self.position = position
        self.size = size
        self.y = position[0]
        self.x = position[1]
        self.hsv = hsv

        #what color is this chunk supposed to be?
        self.color = eval_color(hsv)

    def set_img(self, img):
        self.img = cv2.resize(img, (self.size, self.size), interpolation=cv2.INTER_LINEAR)

def show_image(img):
    cv2.imshow("Image", img)
    cv2.waitKey(0)
    cv2.destroyAllWindows()

def draw_row(img, unitSize, row, height):
    y = unitSize * row
    cv2.line(img, (y, 0), (y, height), (255,255,255))

def draw_col(img, unitSize, col, width):
    x = unitSize * col
    cv2.line(img, (0, x), (width, x), (255,255,255))

def averageColor(img):
    h = img.shape[0]
    w = img.shape[1]
    avgRed = 0
    avgGreen = 0
    avgBlue = 0

    for i in range(h):
        for j in range(w):
            avgRed += img[i,j][0]
            avgGreen += img[i,j][1]
            avgBlue += img[i,j][2]

    avgRed /= h*w
    avgGreen /= h*w
    avgBlue /= h*w

    return [avgRed, avgGreen, avgBlue]
