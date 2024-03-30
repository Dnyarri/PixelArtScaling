#!/usr/bin/env python

'''
Batch rescaling of PNG image using Scale3x aka AdvMAME3x
Created by: Ilya Razmanov (mailto:ilyarazmanov@gmail.com)
            aka Ilyich the Toad (mailto:amphisoft@gmail.com)
Versions:
01.000      Initial working release 
01.001      Progress indication added, showing name of file being processed
2024.02.24  Cleanup, GUI tweaks, versioning changed to YYYY.MM.DD
2024.03.30  pHYs chunk editing to keep image print size constant

'''

__author__ = "Ilya Razmanov"
__copyright__ = "(c) 2024 Ilya Razmanov"
__credits__ = "Ilya Razmanov"
__license__ = "unlicense"
__version__ = "2024.03.30"
__maintainer__ = "Ilya Razmanov"
__email__ = "ilyarazmanov@gmail.com"
__status__ = "Production"

from tkinter import Tk
from tkinter import Label
from tkinter import filedialog

from glob import glob

import png                      # PNG reading: PyPNG from: https://gitlab.com/drj11/pypng
import IncSrc                   # Image reshaping from: https://github.com/Dnyarri/PixelArtScaling
from IncScaleNx import Scale3x  # Scale2x and Scale3x from: https://github.com/Dnyarri/PixelArtScaling

# --------------------------------------------------------------
# Creating dialog

sortir = Tk()
sortir.title('Processing Scale3x...')
sortir.iconbitmap('3xBATCH.ico')
sortir.geometry('+100+100')
zanyato = Label(sortir, text = 'Starting...', font=("arial", 12), padx=16, pady=10, justify='center')
zanyato.pack()
sortir.withdraw()

# Main dialog created and hidden
# --------------------------------------------------------------

# Open source dir
sourcedir = filedialog.askdirectory(title='Open DIR to resize PNG images using Scale3x')
if (sourcedir == ''):
    quit()

# --------------------------------------------------------------
# Updating dialog

sortir.deiconify()
zanyato.config(text = 'Allons-y!')
sortir.update()
sortir.update_idletasks()

# Dialog shown and updated
# --------------------------------------------------------------

# Process file list
for runningfilename in glob(sourcedir + "/**/*.png", recursive=True):   # select all PNG files in all subfolders

    oldfile = runningfilename
    newfile = oldfile                   # Previous version used backup newfile = oldfile + '.3x.png'

    zanyato.config(text = oldfile)      # Updating label, showing processed file name
    sortir.update()
    sortir.update_idletasks()

    source = png.Reader(filename = oldfile)
    X,Y,pixels,info = source.asDirect() # Opening image, iDAT comes to "pixels" as bytearray, to be tuple'd lated.
    Z = (info['planes'])                # PyPNG returns X,Y directly, but not Z. Z should be extracted from info
    imagedata = tuple((pixels))         # Attempt to fix all bytearrays as something solid


    # Reading image as list
    ImageAsListListList = IncSrc.Img3D(imagedata, X, Y, Z)

    # Scaling list to 3x image list
    EPXImage,newX,newY = Scale3x(ImageAsListListList, X, Y)

    # Reshaping 3x scaled 3D list into 1D list for PyPNG .write_array method
    ResultImageAsList = IncSrc.Img3Dto1D(EPXImage, newX, newY, Z)

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
    x_pixels_per_unit = 3*x_pixels_per_unit # Triple resolution to keep print size
    y_pixels_per_unit = 3*y_pixels_per_unit # Triple resolution to keep print size
    # Resolution changed
    # --------------------------------------------------------------

    # Writing new image
    resultPNG = open(newfile, mode='wb')
    writer = png.Writer(newX, newY, greyscale = info['greyscale'], alpha = info['alpha'], bitdepth = info['bitdepth'], physical = [x_pixels_per_unit, y_pixels_per_unit, unit_is_meter])
    writer.write_array(resultPNG, ResultImageAsList)
    resultPNG.close()

# --------------------------------------------------------------
# Destroying dialog

sortir.destroy()
sortir.mainloop()

# Dialog destroyed and closed
# --------------------------------------------------------------
