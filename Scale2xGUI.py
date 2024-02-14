# Attempt to write Scale2x aka AdvMAME2x using Python only
# Created by Ilyich the Toad (mailto: amphisoft@gmail.com)
# Versions:
# 01.001    Scale2x (AdvMAME2x) seem to work

import png  # PNG reading: PyPNG from: https://gitlab.com/drj11/pypng
from tkinter import filedialog

# Open source file
sourcefilename = filedialog.askopenfilename(title='Open source PNG file', filetypes=[('PNG','.png')])
if (sourcefilename == ''):
    quit()

source = png.Reader(filename = sourcefilename)

X,Y,pixels,info = source.asDirect() # Opening image, iDAT comes to "pixels" as bytearray, to be tuple'd lated.
Z = (info['planes'])            # Maximum CHANNEL NUMBER
imagedata = tuple((pixels))     # Attempt to fix all bytearrays

if (info['bitdepth'] == 8):
    maxcolors = 255             # Maximal value for 8-bit channel
if (info['bitdepth'] == 16):
    maxcolors = 65535           # Maximal value for 16-bit channel

# Notice: alpha == maxcolors means OPAQUE

# now the test program

# src a-la FM style src(x,y,z)
# Image should be opened as "imagedata" by main program before
# Note that X, Y, Z are not determined in function, you have to determine it in main program

def src(x, y, z):  # Analog src from FM, force repeate edge instead of out of range

    cx = int(x); cy = int(y)
    cx = max(0,cx); cx = min((X-1),cx)
    cy = max(0,cy); cy = min((Y-1),cy)

    position = (cx*Z) + z   # Here is the main magic of turning two x, z into one array position
    channelvalue = int(((imagedata[cy])[position]))
    
    return channelvalue
# end of src function

def srcY(x, y):  # Converting to greyscale, returns Y, force repeate edge instead of out of range

    cx = int(x); cy = int(y)
    cx = max(0,cx); cx = min((X-1),cx)
    cy = max(0,cy); cy = min((Y-1),cy)

    if (info['planes'] < 3):    # supposedly L and LA
        Yntensity = src(x, y, 0)
    else:                       # supposedly RGB and RGBA
        Yntensity = int(0.2989*src(x, y, 0) + 0.587*src(x, y, 1) + 0.114*src(x, y, 2))
    
    return Yntensity
# end of src function


# --------------------------------------------------------------
# First cycle - writing list
ImageAsListListList = list()
for y in range(0, Y, 1):
    RowAsListList = list()
    for x in range(0, X, 1):
        PixelAsList = list()
        for z in range(0, Z, 1):
            signal = src(x,y,z)
            PixelAsList.append(signal)
        RowAsListList.append(PixelAsList)
    ImageAsListListList.append(RowAsListList)
# creating list finished. ImageAsListListList is 3D array x,y,z
# --------------------------------------------------------------


# --------------------------------------------------------------
# Scaling to 2x image list

doubleX = 2*X; doubleY = 2*Y

EPXImage = list()

for y in range(0, Y, 1):
    RowRez = list(); RowDvo = list()
    for x in range(0, X, 1):

        P = ImageAsListListList[y][x]
        A = ImageAsListListList[max(y-1, 0)][x]
        B = ImageAsListListList[y][min(x+1, X-1)]
        C = ImageAsListListList[y][max(x-1, 0)]
        D = ImageAsListListList[min(y+1, Y-1)][x]

        r1 = P; r2 = P; r3 = P; r4 = P
        
        if ((C==A) and (C!=D) and (A!=B)):
            r1 = A
        if ((A==B) and (A!=C) and (B!=D)):
            r2 = B
        if ((D==C) and (D!=B) and (C!=A)):
            r3 = C
        if ((B==D) and (B!=A) and (D!=C)):
            r4 = D

        RowRez.append(r1); RowRez.append(r2)
        RowDvo.append(r3); RowDvo.append(r4)
    
    EPXImage.append(RowRez)
    EPXImage.append(RowDvo)

# rescaling two times finished
# --------------------------------------------------------------

# --------------------------------------------------------------
# reshaping 2x list from 3D to 1D
ResultImageAsList = list()
for y in range(0, doubleY, 1):
    for x in range(0, doubleX, 1):
        for z in range(0, Z, 1):
            signal = EPXImage[y][x][z]
            ResultImageAsList.append(signal)
# end reshaping cycle
# --------------------------------------------------------------

# --------------------------------------------------------------
# Open export file
resultPNG = filedialog.asksaveasfile(mode='wb', title='Save resulting PNG file', filetypes=[('PNG','.png')], defaultextension = ('PNG file','.png'))
if (resultPNG == ''):
    quit()
# Export file opened
# --------------------------------------------------------------

# --------------------------------------------------------------
# Writing export file
writer = png.Writer(doubleX, doubleY, greyscale = info['greyscale'], alpha = info['alpha'], bitdepth = info['bitdepth'])
writer.write_array(resultPNG, ResultImageAsList)
resultPNG.close()
# Export file closed
# --------------------------------------------------------------
