#!/usr/bin/env python3

'''
Scale2x aka AdvMAME2x bitmap image scaling using Python only, command line version
Created by: Ilya Razmanov (mailto:ilyarazmanov@gmail.com)
            aka Ilyich the Toad (mailto:amphisoft@gmail.com)

Usage: python Scale2xCLI.py source.png result.png

Versions:
01.001    Initial working Scale2x (AdvMAME2x) release 
01.002    Changed from self-contained to modular, IncSrc and IncScaleNx modules created 
01.003    Ultimate modular evil, moving everything possible to IncSrc.py and IncScaleNx.py 
2024.02.24  Cleanup, minimizing import, versioning changed to YYYY.MM.DD
2024.03.30  pHYs chunk editing to keep image print size constant
2024.05.04  Small improvement in argv handling
2024.05.10  Fixes

'''

__author__ = 'Ilya Razmanov'
__copyright__ = '(c) 2024 Ilya Razmanov'
__credits__ = 'Ilya Razmanov'
__license__ = 'unlicense'
__version__ = '2024.05.10'
__maintainer__ = 'Ilya Razmanov'
__email__ = 'ilyarazmanov@gmail.com'
__status__ = 'Production'

from sys import argv

import png                      # PNG reading: PyPNG from: https://gitlab.com/drj11/pypng
import IncSrc                   # Image reshaping from: https://github.com/Dnyarri/PixelArtScaling
from IncScaleNx import Scale2x  # Scale2x and Scale3x from: https://github.com/Dnyarri/PixelArtScaling

# Taking user input

if len(argv) == 2:
    Rez = argv[1]
    Dvo = argv[1]
elif len(argv) == 3:
    Rez = argv[1]
    Dvo = argv[2]
else:
    print('Usage: Scale2CLI input.png output.png')
    quit()

# Open source file
source = png.Reader(filename=Rez)

X, Y, pixels, info = source.asDirect()  # Opening image, iDAT comes to "pixels" as bytearray, to be tuple'd lated.
Z = info['planes']                      # Maximum CHANNEL NUMBER
imagedata = tuple((pixels))             # Attempt to fix all bytearrays

# Source file opened as imagedata
# --------------------------------------------------------------


# Reading image as list
ImageAsListListList = IncSrc.Img3D(imagedata, X, Y, Z)

# Scaling list to 2x image list
EPXImage, doubleX, doubleY = Scale2x(ImageAsListListList, X, Y)

# Reshaping 2x scaled 3D list into 1D list for PyPNG .write_array method
ResultImageAsList = IncSrc.Img3Dto1D(EPXImage, doubleX, doubleY, Z)

# --------------------------------------------------------------
# Fixing resolution to match original print size.
# If no pHYs found in original, 96 ppi is assumed as original value.
if 'physical' in info:
    res = info['physical']      # Reading resolution as tuple
    x_pixels_per_unit = res[0]
    y_pixels_per_unit = res[1]
    unit_is_meter = res[2]
else:
    x_pixels_per_unit = 3780    # 3780 px/meter = 96 px/inch, 2834 px/meter = 72 px/inch
    y_pixels_per_unit = 3780    # 3780 px/meter = 96 px/inch, 2834 px/meter = 72 px/inch
    unit_is_meter = True
x_pixels_per_unit = 2 * x_pixels_per_unit   # Double resolution to keep print size
y_pixels_per_unit = 2 * y_pixels_per_unit   # Double resolution to keep print size
# Resolution changed
# --------------------------------------------------------------

# --------------------------------------------------------------
# Open export file

resultPNG = open(Dvo, mode='wb')
# Writing export file
writer = png.Writer(
    doubleX,
    doubleY,
    greyscale=info['greyscale'],
    alpha=info['alpha'],
    bitdepth=info['bitdepth'],
    physical=[x_pixels_per_unit, y_pixels_per_unit, unit_is_meter],
)
writer.write_array(resultPNG, ResultImageAsList)
resultPNG.close()

# Export file closed
# --------------------------------------------------------------
