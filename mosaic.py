import cv2
import colorsys
import numpy
from enum import Enum
import os
import random


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
        self.set_sub_images()

        if enable_debug:
            self.resized_img = self.debug_draw()

    #returns a sub-image of the resized image
    def get_image_slice(self, r, c):
        x1 = c * self.unit_size
        x2 = x1 + self.unit_size
        y1 = r * self.unit_size
        y2 = y1 + self.unit_size
        unit = self.resized_img[x1:x2, y1:y2]
        return unit

    #split the image into chunks and whatnot
    def chunkify(self):
        self.chunks = {}
        for r in range(self.mosaic_height):
            for c in range(self.mosaic_width):
                try:
                    sub_img = self.get_image_slice(c, r) #get the image at this location
                    color_RGB = averageColor(sub_img) #loop through all pixels and get average RGB
                    color_HSV = colorsys.rgb_to_hsv(color_RGB[0], color_RGB[1], color_RGB[2]) #turn the RGB into HSV
                    self.chunks[(c,r)] = Chunk((c,r), self.unit_size, color_HSV) #create a new chunk and pass in HSV
                    print("created",c,r) #debug
                except:
                    print("Image size is 0!", r, c)

    def __str__(self):
        return "Mosaic Width: " + str(self.mosaic_width) + "\nMosaic Height: " + str(self.mosaic_height)

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
                    cv2.putText(img=self.resized_img, text=str(self.chunks[(c,r)].color[0].value), org=org, fontFace=cv2.FONT_HERSHEY_TRIPLEX, fontScale=0.7, color=(255, 255, 255),thickness=2)
        return self.resized_img

    def set_sub_images(self):
        baseAdd = "./dataset/" #base address of data

        print("Setting sub images...")
        for r in range(self.mosaic_height):
            for c in range(self.mosaic_width):
                chunk = self.chunks[(c,r)] #get chunk at this location

                #get the filepath to reference from
                #chunk.color[0] = color (e.g RED, ORANGE, YELLOW)
                #chunk.color[1] = value (e.g BLACK, GRAY, WHITE)
                chunk_color_string = getValueString[chunk.color[1]] + " " + getColorString[chunk.color[0]]
                path = baseAdd+chunk_color_string+"/"

                image_pool = os.listdir(baseAdd + chunk_color_string) #grab a list of all files in that directory
                
                #remove files that we don't care about
                if "desktop.ini" in image_pool:
                    image_pool.remove("desktop.ini")
                
                random_image = path+random.choice(image_pool) #pick a random image
                print(random_image) #debug
                img = cv2.imread(random_image, cv2.IMREAD_ANYCOLOR) #load the image
                self.set_sub_img((c,r), img)
                print("Set image for",c,r)

    def set_sub_img(self, coor, img):
        self.chunks[coor].set_img(img)

    def generate_collage(self):
        columns = []
        print("Building columns...")
        #create an array of all columns
        for r in range(self.mosaic_height):
            col = []
            for c in range(self.mosaic_width):
                col.append(self.chunks[(c,r)].img)
                print("\tAdded chunk",c,r)
            columns.append(numpy.vstack(col))
            print("Built row",r)
        #compress all columns into a row
        rows = numpy.hstack(columns)
        return rows
        
class Chunk:
    def __init__(self, position, size, hsv):
        self.position = position
        self.size = size
        self.y = position[0]
        self.x = position[1]
        self.hsv = hsv

        #what color is this chunk supposed to be?
        self.color = eval_color(hsv)
        #print(self.color)

    def set_img(self, img):
        self.img = cv2.resize(img, (self.size, self.size), interpolation=cv2.INTER_LINEAR)


class GeneralHue(Enum):
    RED = 1
    ORANGE = 2
    YELLOW = 3
    GREEN = 4
    CYAN = 5
    BLUE = 6
    PURPLE = 7
    PINK = 8
    BROWN = 9
    BLACK = 10
    GRAY = 11
    WHITE = 12

class GeneralValue(Enum):
    BLACK = 1
    GRAY = 2
    WHITE = 3

getColorString = {
    GeneralHue.RED: "red",
    GeneralHue.ORANGE: "orange",
    GeneralHue.YELLOW: "yellow",
    GeneralHue.GREEN: "green",
    GeneralHue.CYAN: "cyan",
    GeneralHue.BLUE: "blue",
    GeneralHue.PURPLE: "purple",
    GeneralHue.PINK: "pink",
}

getValueString = {
    GeneralValue.BLACK: "dark",
    GeneralValue.GRAY: "",
    GeneralValue.WHITE: "bright"
}

class ColorRange:
    def __init__(self, color, start, end):
        self.start = start
        self.end = end
        self.color = color

    def belongs(self, hue):
        if hue >= self.start and hue < self.end:
            return True
        else:
            return False

    def __str__(self):
        return self.color

class ValueRange:
    def __init__(self, value, start, end):
        self.start = start
        self.end = end
        self.value = value

    def belongs(self, value):
        if value >= self.start and value < self.end:
            return True
        else:
            return False

COLOR_RANGES = [
    ColorRange(GeneralHue.CYAN, 0, 0.24),
    ColorRange(GeneralHue.GREEN, 0.24, 0.45),
    ColorRange(GeneralHue.YELLOW, 0.45, 0.52),
    ColorRange(GeneralHue.ORANGE, 0.52, 0.62),
    ColorRange(GeneralHue.RED, 0.62, 0.71),
    ColorRange(GeneralHue.PINK, 0.71, 0.81),
    ColorRange(GeneralHue.PURPLE, 0.81, 0.91),
    ColorRange(GeneralHue.BLUE, 0.91, 1.0),
]

VALUE_RANGES = [
    ValueRange(GeneralValue.BLACK, 0, 50),
    ValueRange(GeneralValue.GRAY, 50, 240),
    ValueRange(GeneralValue.WHITE, 240, 256),
]

def eval_color(color):
    color_result = []

    for range in COLOR_RANGES:
        if range.belongs(color[0]):
            color_result.append(range.color)
            break
    
    for range in VALUE_RANGES:
        if range.belongs(color[2]):
            color_result.append(range.value)
            break
 
    if len(color_result) != 2:
        print("Huh")
        print(color_result)
        print(color)

    return color_result

def show_image(img):
    cv2.imshow("Test", img)
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
