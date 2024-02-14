# Attempt to write Scale3x aka AdvMAME3x using Python only
# Created by Ilyich the Toad (mailto: amphisoft@gmail.com)
# Versions:
# 01.001    Scale3x (AdvMAME3x) seem to work

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
# Scaling to 3x image list

tripleX = 3*X; tripleY = 3*Y

EPXImage = list()

for y in range(0, Y, 1):
    RowRez = list(); RowDvo = list(); RowTre = list()
    for x in range(0, X, 1):

        E = ImageAsListListList[y][x]   # E is a center of 3x3 square

        A = ImageAsListListList[max(y-1, 0)][max(x-1, 0)]
        B = ImageAsListListList[max(y-1, 0)][x]
        C = ImageAsListListList[max(y-1, 0)][min(x+1, X-1)]

        D = ImageAsListListList[y][max(x-1, 0)]
        # central pixel E = ImageAsListListList[y][x] calculated already
        F = ImageAsListListList[y][min(x+1, X-1)]

        G = ImageAsListListList[min(y+1, Y-1)][max(x-1, 0)]
        H = ImageAsListListList[min(y+1, Y-1)][x]
        I = ImageAsListListList[min(y+1, Y-1)][min(x+1, X-1)]

        r1 = E; r2 = E; r3 = E; r4 = E; r5 = E; r6 = E; r7 = E; r8 = E; r9 = E
        
        if ((D==B) and (D!=H) and (B!=F)):
            r1 = D
        if (((D==B) and (D!=H) and (B!=F) and (E!=C)) or ((B==F) and (B!=D) and (F!=H) and (E!=A))):
            r2 = B
        if ((B==F) and (B!=D) and (F!=H)):
            r3 = F
        if  (((H==D) and (H!=F) and (D!=B) and (E!=A)) or ((D==B) and (D!=H) and (B!=F) and (E!=G))):
            r4 = D
        # r5 = E already
        if  (((B==F) and (B!=D) and (F!=H) and (E!=I)) or ((F==H) and (F!=B) and (H!=D) and (E!=C))):
            r6 = F
        if  ((H==D) and (H!=F) and (D!=B)):
            r7 = D
        if  (((F==H) and (F!=B) and (H!=D) and (E!=G)) or ((H==D) and (H!=F) and (D!=B) and (E!=I))):
            r8 = H
        if  ((F==H) and (F!=B) and (H!=D)):
            r9 = F

        RowRez.append(r1); RowRez.append(r2); RowRez.append(r3)
        RowDvo.append(r4); RowDvo.append(r5); RowDvo.append(r6)
        RowTre.append(r7); RowTre.append(r8); RowTre.append(r9)
    
    EPXImage.append(RowRez)
    EPXImage.append(RowDvo)
    EPXImage.append(RowTre)

# rescaling three times finished
# --------------------------------------------------------------

# --------------------------------------------------------------
# reshaping 3x list from 3D to 1D
ResultImageAsList = list()
for y in range(0, tripleY, 1):
    for x in range(0, tripleX, 1):
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
writer = png.Writer(tripleX, tripleY, greyscale = info['greyscale'], alpha = info['alpha'], bitdepth = info['bitdepth'])
writer.write_array(resultPNG, ResultImageAsList)
resultPNG.close()
# Export file closed
# --------------------------------------------------------------
