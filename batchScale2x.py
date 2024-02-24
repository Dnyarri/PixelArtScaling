#!/usr/bin/env python

'''
Batch rescaling of PNG image using Scale2x aka AdvMAME2x
Created by: Ilya Razmanov (mailto:ilyarazmanov@gmail.com)
            aka Ilyich the Toad (mailto:amphisoft@gmail.com)
Versions:
01.000      Initial working release 
01.001      Progress indication added, showing name of file being processed
2024.02.24  Cleanup, GUI tweaks, versioning changed to YYYY.MM.DD

'''

__author__ = "Ilya Razmanov"
__copyright__ = "(c) 2024 Ilya Razmanov"
__credits__ = "Ilya Razmanov"
__license__ = "unlicense"
__version__ = "2024.02.24"
__maintainer__ = "Ilya Razmanov"
__email__ = "ilyarazmanov@gmail.com"
__status__ = "Production"

from tkinter import Tk
from tkinter import Label
from tkinter import filedialog

from glob import glob

import png                      # PNG reading: PyPNG from: https://gitlab.com/drj11/pypng
import IncSrc                   # Image reshaping from: https://github.com/Dnyarri/PixelArtScaling
from IncScaleNx import Scale2x  # Scale2x and Scale3x from: https://github.com/Dnyarri/PixelArtScaling

# --------------------------------------------------------------
# Creating dialog

sortir = Tk()
sortir.title('Processing Scale2x...')
sortir.geometry('+100+100')
zanyato = Label(sortir, text = 'Starting...', font=("arial", 12), padx=16, pady=10, justify='center')
zanyato.pack()
sortir.withdraw()

# Main dialog created and hidden
# --------------------------------------------------------------

# Open source dir
sourcedir = filedialog.askdirectory(title='Open DIR to resize PNG images using scale2x')
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
    newfile = oldfile + '.2x.png'       # If you wish originals to be replaced, set newfile = oldfile

    zanyato.config(text = oldfile)      # Updating label, showing processed file name
    sortir.update()
    sortir.update_idletasks()

    source = png.Reader(filename = oldfile)
    X,Y,pixels,info = source.asDirect() # Opening image, iDAT comes to "pixels" as bytearray, to be tuple'd lated.
    Z = (info['planes'])                # PyPNG returns X,Y directly, but not Z. Z should be extracted from info
    imagedata = tuple((pixels))         # Attempt to fix all bytearrays as something solid


    # Reading image as list
    ImageAsListListList = IncSrc.Img3D(imagedata, X, Y, Z)

    # Scaling list to 2x image list
    EPXImage,newX,newY = Scale2x(ImageAsListListList, X, Y)

    # Reshaping 2x scaled 3D list into 1D list for PyPNG .write_array method
    ResultImageAsList = IncSrc.Img3Dto1D(EPXImage, newX, newY, Z)

    # Writing new image
    resultPNG = open(newfile, mode='wb')
    writer = png.Writer(newX, newY, greyscale = info['greyscale'], alpha = info['alpha'], bitdepth = info['bitdepth'])
    writer.write_array(resultPNG, ResultImageAsList)
    resultPNG.close()

# --------------------------------------------------------------
# Destroying dialog

sortir.destroy()
sortir.mainloop()

# Dialog destroyed and closed
# --------------------------------------------------------------
