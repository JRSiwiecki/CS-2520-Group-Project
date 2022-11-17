import cv2
import colorsys

class Chunk:
    def __init__(self, position, color):
        self.position = position
        self.y = position[0]
        self.x = position[1]
        self.color = color

def showImg(img):
    cv2.imshow("Test", img)
    cv2.waitKey(0)
    cv2.destroyAllWindows()

def drawRow(img, unitSize, row, height):
    y = unitSize * row
    cv2.line(img, (y, 0), (y, height), (255,255,255))

def drawCol(img, unitSize, col, width):
    x = unitSize * col
    cv2.line(img, (0, x), (width, x), (255,255,255))

def debugDraw(mosaicWidth, mosaicHeight):
    for i in range(mosaicWidth):
        drawRow(resized, mosaicUnitSize, i, resizeHeight)

    for i in range(mosaicHeight):
        drawCol(resized, mosaicUnitSize, i, resizeWidth)
    return resized

def getUnit(img, unitSize, r, c):
    x1 = c * unitSize
    x2 = x1 + unitSize
    y1 = r * unitSize
    y2 = y1 + unitSize
    unit = img[x1:x2, y1:y2]
    return unit

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
    
try:
    img = cv2.imread("apple2.png", cv2.IMREAD_COLOR)
except:
    print("Can't find that file")
    exit()    

mosaicUnitSize = 70

height = img.shape[0]
width = img.shape[1]

resizeHeight = height - height%mosaicUnitSize
resizeWidth = width - width%mosaicUnitSize

mosaicHeight = resizeHeight // mosaicUnitSize
mosaicWidth = resizeWidth // mosaicUnitSize

print(resizeHeight)
print(resizeWidth)

print(mosaicHeight)
print(mosaicWidth)

resized = cv2.resize(img, (resizeWidth, resizeHeight), interpolation=cv2.INTER_LINEAR)

colorMap = []

for i in range(mosaicHeight):
    for j in range(mosaicWidth):
        try:
            unit = getUnit(img, mosaicUnitSize, j, i)
            colRGB = averageColor(unit)
            colHSV = colorsys.rgb_to_hsv(colRGB[0], colRGB[1], colRGB[2])
            print(colHSV[0])
            colorMap.append(Chunk((i,j), colHSV))
        except:
            print("Image size is 0!", j, i)
showImg(debugDraw(mosaicWidth, mosaicHeight))