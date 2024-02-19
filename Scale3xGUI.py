# Attempt to write Scale3x aka AdvMAME3x using Python only
# Created by Ilyich the Toad (mailto: amphisoft@gmail.com)
# Versions:
# 01.001    Scale3x (AdvMAME3x) seem to work
# 01.002    Changed from self-contained to modular, IncSrc and IncScaleNx modules created
# 01.003    Ultimate modular evil, moving everything possible to IncSrc.py and IncScaleNx.py

import png  # PNG reading: PyPNG from: https://gitlab.com/drj11/pypng
from tkinter import filedialog
import IncSrc
from IncScaleNx import Scale3x

# --------------------------------------------------------------
# Open source file

sourcefilename = filedialog.askopenfilename(title='Open source PNG file', filetypes=[('PNG','.png')])
if (sourcefilename == ''):
    quit()

source = png.Reader(filename = sourcefilename)
X,Y,pixels,info = source.asDirect() # Opening image, iDAT comes to "pixels" as bytearray, to be tuple'd lated.
Z = (info['planes'])                # PyPNG returns X,Y directly, but not Z. Z should be extracted from info
imagedata = tuple((pixels))         # Attempt to fix all bytearrays as something solid


# Source file opened as imagedata
# --------------------------------------------------------------

# Reading image as list
ImageAsListListList = IncSrc.Img3D(imagedata, X, Y, Z)

# Scaling to 3x image list
EPXImage,tripleX,tripleY = Scale3x(ImageAsListListList, X, Y)

# Reshaping 3x scaled 3D list into 1D list for PyPNG .write_array method
ResultImageAsList = IncSrc.Img3Dto1D(EPXImage, tripleX, tripleY, Z)


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

# Export file written and closed
# --------------------------------------------------------------
