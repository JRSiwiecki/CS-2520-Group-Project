import cv2
import colorsys
import numpy
from enum import Enum
import os


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
                    sub_img = self.get_image_slice(c, r)
                    color_RGB = averageColor(sub_img)
                    color_HSV = colorsys.rgb_to_hsv(color_RGB[0], color_RGB[1], color_RGB[2])
                    self.chunks[(c,r)] = Chunk((c,r), self.unit_size, color_HSV)
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
                    cv2.putText(img=self.resized_img, text=str(self.chunks[(c,r)].color.value), org=org, fontFace=cv2.FONT_HERSHEY_TRIPLEX, fontScale=0.7, color=(0, 0, 0),thickness=2)
        return self.resized_img

    def set_sub_images(self):
        baseAdd = "./dataset/candy AND green/" #base address of data
        dir_list = os.listdir(baseAdd) #grab a list of all files in that directory
        print(dir_list) #probably remove this
        dir_index = 0
        
        print("Setting sub images...")
        for r in range(self.mosaic_height):
            for c in range(self.mosaic_width):
                img = cv2.imread(baseAdd + dir_list[dir_index], cv2.IMREAD_COLOR) #load the image
                self.set_sub_img((c,r), img)
                print("\tSet image for",c,r)
                
                dir_index+=1 #if you don't have enough images (shouldn't happen)
                if dir_index >= len(dir_list):
                    dir_index = 0

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
        self.color = eval_color(hsv[0])
        print(self.color)

    def set_img(self, img):
        self.img = cv2.resize(img, (self.size, self.size), interpolation=cv2.INTER_LINEAR)


class GeneralColor(Enum):
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

COLOR_RANGES = [
    ColorRange(GeneralColor.CYAN, 0, 0.24),
    ColorRange(GeneralColor.GREEN, 0.24, 0.45),
    ColorRange(GeneralColor.YELLOW, 0.45, 0.52),
    ColorRange(GeneralColor.ORANGE, 0.52, 0.62),
    ColorRange(GeneralColor.RED, 0.62, 0.71),
    ColorRange(GeneralColor.PINK, 0.71, 0.81),
    ColorRange(GeneralColor.PURPLE, 0.81, 0.91),
    ColorRange(GeneralColor.BLUE, 0.91, 1.0),
]

def eval_color(hue):
    for range in COLOR_RANGES:
        if range.belongs(hue):
            return range.color
    print(hue,"didn't fit!")

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
