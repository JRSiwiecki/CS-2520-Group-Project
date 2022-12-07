from mosaic import *
from tkinter import *
from PIL import ImageTk, Image

root = Tk()

root.title("Mosaic Generator")

imglbl = Label(root, text = "Enter Image name: ")
imglbl.grid(padx= (10, 5))

sizelbl = Label(root, text = "Enter unit size: ")
sizelbl.grid(padx= (10, 10))

imageTxt = Entry(root, width = 20)
imageTxt.grid(column = 1, row = 0)

sizeTxt = Entry(root, width = 20)
sizeTxt.grid(column = 1, row = 1)

oglbl = Label(root)
oglbl.grid(column = 1, row = 4)

lbl = Label(root)
lbl.grid(column=1, row = 6, padx= (0, 20))

def check():
    try:
        og = "Original Image:"
        oglbl.config(text = og)
        filename = Image.open("testimages/" + imageTxt.get() + ".png")
        width = filename.width
        height = filename.height

        image = filename.resize((width // 6, height // 6), Image.ANTIALIAS)
        photo = ImageTk.PhotoImage(image)

        lbl.config(image = photo)
        lbl.image = photo
        lbl.grid(column=1, row = 6, padx= (0, 20))
    except:
        errorlbl = "No Photo Found"
        oglbl.config(text = errorlbl)
        lbl.grid_forget()
    

def clicked():
    try:
        image = imageTxt.get()
        img = cv2.imread("testimages/" + image + ".png", cv2.IMREAD_COLOR)

    except:
        print("Can't find that file")
        exit() 

    size = int(sizeTxt.get())
    mosaic = MosaicImage(ref_img=img, unit_size=size, enable_debug=False)
    mosaic.show()

def restart():
    imageTxt.delete(0, "end")
    sizeTxt.delete(0, "end")
    oglbl.config(text = "")
    lbl.config(image = "")


checkBtn = Button(root, text = "check", fg = "black", command = check)
checkBtn.grid(column = 2, row = 0, padx= (5, 10))

generateBtn = Button(root, text = "Generate", fg = "black", command = clicked)
generateBtn.grid(column = 1, row = 2)

restartBtn = Button(root, text = "New Mosaic", fg = "black", command = restart)
restartBtn.grid(column = 1, row = 8)

root.mainloop()
