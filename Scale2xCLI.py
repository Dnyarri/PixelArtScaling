# Attempt to write Scale2x aka AdvMAME2x using Python only
# Created by Ilyich the Toad (mailto: amphisoft@gmail.com)
# Versions:
# 01.001    Scale2x (AdvMAME2x) seem to work 
# 01.002    Changed from self-contained to modular, IncSrc and IncScaleNx modules created 
# 01.003    Ultimate modular evil, moving everything possible to IncSrc.py and IncScaleNx.py 

from sys import argv

import png                      # PNG reading: PyPNG from: https://gitlab.com/drj11/pypng
import IncSrc                   # Image reshaping from: https://github.com/Dnyarri/PixelArtScaling
from IncScaleNx import Scale2x  # Scale2x and Scale3x from: https://github.com/Dnyarri/PixelArtScaling

# Taking user input

Rez = argv[1]
Dvo = argv[2]

# Open source file
source = png.Reader(filename = Rez)

X,Y,pixels,info = source.asDirect() # Opening image, iDAT comes to "pixels" as bytearray, to be tuple'd lated.
Z = (info['planes'])            # Maximum CHANNEL NUMBER
imagedata = tuple((pixels))     # Attempt to fix all bytearrays

# Source file opened as imagedata
# --------------------------------------------------------------


# Reading image as list
ImageAsListListList = IncSrc.Img3D(imagedata, X, Y, Z)

# Scaling list to 2x image list
EPXImage,doubleX,doubleY = Scale2x(ImageAsListListList, X, Y)

# Reshaping 2x scaled 3D list into 1D list for PyPNG .write_array method
ResultImageAsList = IncSrc.Img3Dto1D(EPXImage, doubleX, doubleY, Z)


# --------------------------------------------------------------
# Open export file

resultPNG = open(Dvo, mode='wb')
# Writing export file
writer = png.Writer(doubleX, doubleY, greyscale = info['greyscale'], alpha = info['alpha'], bitdepth = info['bitdepth'])
writer.write_array(resultPNG, ResultImageAsList)
resultPNG.close()

# Export file closed
# --------------------------------------------------------------
