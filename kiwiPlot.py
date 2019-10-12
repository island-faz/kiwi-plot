#!/usr/bin/env python

"""kiwiPlot.py: KiwiPlot main"""

__author__      = "Amine BOURHIME"
__copyright__   = "Copyright 2018, kiwi-Plot Project"
__version__     = "1.0.1"
__email__       = "bourhime_amine@hotmail.fr"
__date__        = "12/12/2018"

try:
    from tkinter import *
    from tkinter import messagebox
    from tkinter import filedialog
except:
    print("please try to install tkinter dependency for python")
    exit()

try:
    from PIL import ImageTk, Image, ImageDraw
except:
    print("please try to install PIL dependency for python")
    exit()

import os
import kiwiCore

def plotClick():
    global photo
    global parseError

    errorFlag = False

    rangeX = [0, 0]
    rangeY = [0, 0]

    error_msg = "must be integer, exemple of integers: (-7, -2, 0, 1 , 5, ...)"

    try:
        rangeX[0] = int(xMinRange.get("1.0","end-1c"))
    except:
        errorFlag = True
        messagebox.showinfo("Input Error", "x1 %s"%(error_msg))
        return None

    try:
        rangeX[1] = int(xMaxRange.get("1.0","end-1c"))
    except:
        errorFlag = True        
        messagebox.showinfo("Input Error", "x2 %s"%(error_msg))
        return None

    try:
        rangeY[0] = int(yMinRange.get("1.0","end-1c"))
    except:
        errorFlag = True
        messagebox.showinfo("Input Error", "y1 %s"%(error_msg))
        return None

    try:
        rangeY[1] = int(yMaxRange.get("1.0","end-1c"))
    except:
        errorFlag = True        
        messagebox.showinfo("Input Error", "y2 %s"%(error_msg))
        return None

    try:
        pointsNbr = int(pointNbr_txt.get("1.0", "end-1c"))
        if (pointsNbr < 10):
            messagebox.showinfo("Input Error", "Number of points should be at least 10")            
            errorFlag = True
        elif (pointsNbr > 10000):
            messagebox.showinfo("Input Error", "Number of points is too large, Maximum value is 10000")
            errorFlag = True
    except:
        errorFlag = True
        messagebox.showinfo("Input Error", "Number of points should be at least 10")
        return None

    if (rangeX[1] - rangeX[0] <= 0 or rangeY[1] - rangeY[0] <= 0):
        errorFlag = True        
        messagebox.showinfo("Input Error", "x1 must be superior to x1 and y2 superior to y1")

    elif (rangeX[0] > 100000 or rangeX[0] < -100000 or rangeX[1] > 100000 or rangeX[1] < -100000
        or rangeY[0] > 100000 or rangeY[0] < -100000 or rangeY[1] > 100000 or rangeY[1] < -100000):
        errorFlag = True        
        messagebox.showinfo("Input Error", "Range of X and range of Y shoud be between [-100000, 100000]")

    exp = f_Text.get("1.0","end-1c")

    res = kiwiCore.evalExp(exp, 0)
    if (type(res) is bool and res == False):
        messagebox.showinfo("Syntax Error", "Syntax Error: %s"%(kiwiCore.parseError))
    elif (errorFlag == False):
        img.paste((255, 255, 255), [0, 0, img.size[0], img.size[1]])
        kiwiCore.plot_function(draw, exp, rangeX, rangeY, pointsNbr, W, H, plot_points.get())
        photo = ImageTk.PhotoImage(img)
        w.create_image(W/2, H/2, image=photo)

def save_graph():
    file = filedialog.asksaveasfile(mode='w', defaultextension=".png",
        filetypes=(("PNG file", "*.png"),("All Files", "*.*") ))
    if file:
        abs_path = os.path.abspath(file.name)
        img.save(abs_path)
        file.close()

def helpClick():
    messagebox.showinfo("KiwiPlot Help", "allowed functions : cos, sin, exp, sqrt, abs, log, acos, asin, atan, acosh, asinh, atanh, cosh, sinh, tanh, gamma, erf, erfc, lgamma.")

W = 450
H = 450
win_height = 760

root = Tk()
root.title("KiwiPlot")
root.iconbitmap('assets/fav.ico')
_tmp = root.winfo_screenwidth() // 2 - W // 2
root.geometry("500x800+%s+40"%(_tmp))
root.maxsize(W, win_height)
root.minsize(W, win_height)

w = Canvas(root, width=W, height=H)
w.pack()

topFrame = Frame(root)
topFrame.pack(side=TOP, pady=10, padx=10, fill=X)

middleFrame = Frame(root)
middleFrame.pack(side=TOP, pady=10, padx=10, fill=X)

xMinRange = Text(middleFrame, height=1, width=10)
xMinRange.insert(END, "-4")
xMaxRange = Text(middleFrame, height=1, width=10)
xMaxRange.insert(END, "2")

xRange_label = Label(middleFrame, text="Range of x")

twoPoints_label = Label(middleFrame, text=":")

xRange_label.pack(side=LEFT)
xMinRange.pack(side=LEFT)
twoPoints_label.pack(side=LEFT)
xMaxRange.pack(side=LEFT)

middleFrame2 = Frame(root)
middleFrame2.pack(side=TOP, padx=10, pady=10, fill=X)

middleFrame3 = Frame(root)
middleFrame3.pack(side=TOP, padx=10, pady=10, fill=X)

pointNbr_label = Label(middleFrame3, text="Number of points to evaluate: ")
pointNbr_label.pack(side=LEFT)

pointNbr_txt = Text(middleFrame3, height=1, width=10)
pointNbr_txt.insert(END, "100")
pointNbr_txt.pack(side=LEFT)

yRange_label = Label(middleFrame2, text="Range of y")
yRange_label.pack(side=LEFT)

yMinRange = Text(middleFrame2, height=1, width=10)
yMinRange.insert(END, "-2")
yMinRange.pack(side=LEFT)

twoPoints_label2 = Label(middleFrame2, text=":")
twoPoints_label2.pack(side=LEFT)

yMaxRange = Text(middleFrame2, height=1, width=10)
yMaxRange.insert(END, "7")
yMaxRange.pack(side=LEFT)

plot_points = IntVar()

c = Checkbutton(middleFrame3, text="plot points", variable=plot_points)
c.pack()

bottomFrame = Frame(root)
bottomFrame.pack(side=TOP, pady=10, padx=10, fill=X)

btn1 = Button(bottomFrame, text="plot", command=plotClick)
btn1.pack(fill=X)

btn2 = Button(bottomFrame, text="help", command=helpClick)
btn2.pack(fill=X)

btn3 = Button(bottomFrame, text="save graph", command=save_graph)
btn3.pack(fill=X)

f_label = Label(topFrame, text="f(x)=")
f_label.pack(side=LEFT)

f_Text = Text(topFrame, height=3, width=50)
f_Text.insert(END, "x^2")
f_Text.pack(side=LEFT)

img = Image.new( 'RGB', (W, H), "white")
draw = ImageDraw.Draw(img)

plotClick()
root.mainloop()