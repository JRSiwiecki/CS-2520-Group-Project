'''
HOW TO ADD NEW COLORS
1. Add the color or value to its respective enum class (11 - 26)
2. Add the color or value's corresponding string to its respective dictionary (30 - 45)
3. Add the color or value's range (See bottom of script)
4. If you added a new color, then you need to make a folder per value, excluding black and white. 
For example, if we add "red" as a color we need to add a folder of images called "red", "dark red", "bright red", etc.
   If you added a new value, then you need to make a folder per color.
For example, if we add "darkish" as a value, then we need to add a folder of images called "darkish red", "darkish orange", etc.
'''

from enum import Enum

#A master list of all possible colors.
#Hue represents what kind of color it is - where can it be placed on a rainbow?
class GeneralHue(Enum):
    RED = 1
    ORANGE = 2
    YELLOW = 3
    GREEN = 4
    CYAN = 5
    BLUE = 6
    PURPLE = 7
    PINK = 8

#Value represents the light to darkness of a given color
class GeneralValue(Enum):
    BLACK = 1
    DARK = 2
    NORMAL = 3
    BRIGHT = 4
    WHITE = 5

#Below are 2 dictionaries which give a string for every corresponding hue and value
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
    GeneralValue.BLACK: "black",
    GeneralValue.DARK: "dark",
    GeneralValue.BRIGHT: "bright",
    GeneralValue.WHITE: "white"
}

class Range:
    def __init__(self, val, start, end):
        self.start = start
        self.end = end
        self.val = val

    #does a value fall within this range?
    def belongs(self, hue):
        if hue >= self.start and hue < self.end:
            return True
        else:
            return False

    def __str__(self):
        return self.color

class Color:
    def __init__(self, hue, value):
        self.hue = hue
        self.value = value
    
    def __str__(self):
        #white and black are special, in that it does not matter what the hue is
        if self.value == GeneralValue.WHITE or self.value == GeneralValue.BLACK:
            return getValueString[self.value] #return just the value name
        #if a color is at a normal value, then no prefix is needed, just use the color name
        elif self.value == GeneralValue.NORMAL:
            return getColorString[self.hue]
        #otherwise, use color name with prefix
        else:
            return getValueString[self.value] + " " + getColorString[self.hue]

#takes in a list [hue, saturation, value] and returns a Color object
def eval_color(color):
    for range in COLOR_RANGES:
        if range.belongs(color[0]):
            hue = range.val
            break
    
    for range in VALUE_RANGES:
        if range.belongs(color[2]):
            val = range.val
            break

    return Color(hue, val)

#Below are 2 master lists that are used to determine the ranges
#0 to 1
COLOR_RANGES = [
    Range(GeneralHue.CYAN, 0, 0.24),
    Range(GeneralHue.GREEN, 0.24, 0.50),
    Range(GeneralHue.YELLOW, 0.50, 0.55),
    Range(GeneralHue.ORANGE, 0.55, 0.62),
    Range(GeneralHue.RED, 0.62, 0.71),
    Range(GeneralHue.PINK, 0.71, 0.81),
    Range(GeneralHue.PURPLE, 0.81, 0.91),
    Range(GeneralHue.BLUE, 0.91, 1.0),
]

#0 to 256
VALUE_RANGES = [
    Range(GeneralValue.BLACK, 0, 70),
    Range(GeneralValue.DARK, 70, 140),
    Range(GeneralValue.NORMAL, 140, 200),
    Range(GeneralValue.BRIGHT, 200, 240),
    Range(GeneralValue.WHITE, 240, 256)
]