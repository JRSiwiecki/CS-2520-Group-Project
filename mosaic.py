import cv2
import colorsys

class MosaicImage:
    def __init__(self, ref_img, unit_size):
        self.unit_size = unit_size #how wide/tall each chunk that we are sampling is (for example, 60 px)

        self.ref_img = ref_img #the original image
        self.ref_height = ref_img.shape[0] #the height of the original image
        self.ref_width = ref_img.shape[1] #the width of the original image

        self.resize_height = self.ref_height - self.ref_height%unit_size #height of the resized image (divisible by unit size)
        self.resie_width = self.ref_width - self.ref_width%unit_size #width of the resized image (divisible by unit size)

        self.mosaic_height = self.resize_height // self.unit_size #how many chunks tall is our mosaic?
        self.mosaic_width = self.resie_width // self.unit_size #how many chunks wide is our mosaic?

        #resize the original to fit our new constraints
        self.resized_img = cv2.resize(self.ref_img, (self.resie_width, self.resize_height), interpolation=cv2.INTER_LINEAR)

        self.chunks = []
        self.chunkify()

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
        for r in range(self.mosaic_height):
            for c in range(self.mosaic_width):
                try:
                    sub_img = self.get_image_slice(c, r)
                    color_RGB = averageColor(sub_img)
                    color_HSV = colorsys.rgb_to_hsv(color_RGB[0], color_RGB[1], color_RGB[2])
                    self.chunks.append(Chunk((c, r), color_HSV))
                except:
                    print("Image size is 0!", r, c)

class Chunk:
    def __init__(self, position, color):
        self.position = position
        self.y = position[0]
        self.x = position[1]
        self.color = color

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

def debug_draw(img, unit_size):
    for i in range(img.shape[1]):
        draw_row(img, unit_size, i, img.shape[1])

    for i in range(img.shape[0]):
        draw_col(img, unit_size, i, img.shape[0])
    
    return img

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
