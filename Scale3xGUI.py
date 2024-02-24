#!/usr/bin/env python

'''
Scale3x aka AdvMAME3x bitmap image scaling using Python only
Created by: Ilya Razmanov (mailto:ilyarazmanov@gmail.com)
            aka Ilyich the Toad (mailto:amphisoft@gmail.com)
Versions:
01.001      Scale3x (AdvMAME3x) seem to work 
01.002      Changed from self-contained to modular, IncSrc and IncScaleNx modules created 
01.003      Ultimate modular evil, moving everything possible to IncSrc.py and IncScaleNx.py 
01.004      Progress indication added, showing processing stage 
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

import png                      # PNG reading: PyPNG from: https://gitlab.com/drj11/pypng
import IncSrc                   # Image reshaping from: https://github.com/Dnyarri/PixelArtScaling
from IncScaleNx import Scale3x  # Scale2x and Scale3x from: https://github.com/Dnyarri/PixelArtScaling

# --------------------------------------------------------------
# Creating dialog

sortir = Tk()
sortir.title('Scale3x')
sortir.geometry('+200+100')
zanyato = Label(sortir, text = 'Starting...', font=("arial", 36), padx=15, pady=10, justify='center')
zanyato.pack()
sortir.withdraw()

# Main dialog created and hidden
# --------------------------------------------------------------

# --------------------------------------------------------------
# Open source file

sourcefilename = filedialog.askopenfilename(title='Open source PNG file to reScale3x', filetypes=[('PNG','.png')])
if (sourcefilename == ''):
    quit()

source = png.Reader(filename = sourcefilename)
X,Y,pixels,info = source.asDirect() # Opening image, iDAT comes to "pixels" as bytearray, to be tuple'd lated.
Z = (info['planes'])                # PyPNG returns X,Y directly, but not Z. Z should be extracted from info
imagedata = tuple((pixels))         # Attempt to fix all bytearrays as something solid

# Source file opened as imagedata
# --------------------------------------------------------------

# --------------------------------------------------------------
# Updating dialog

sortir.deiconify()
zanyato.config(text = 'Reading...')
sortir.update()
sortir.update_idletasks()

# Dialog shown and updated
# --------------------------------------------------------------

# Reading image as list
ImageAsListListList = IncSrc.Img3D(imagedata, X, Y, Z)

# --------------------------------------------------------------
# Updating dialog

zanyato.config(text = 'Scaling...')
sortir.update()
sortir.update_idletasks()

# Dialog updated
# --------------------------------------------------------------

# Scaling to 3x image list
EPXImage,tripleX,tripleY = Scale3x(ImageAsListListList, X, Y)

# --------------------------------------------------------------
# Updating dialog

zanyato.config(text='Almost there...')
sortir.update()
sortir.update_idletasks()

# Dialog updated
# --------------------------------------------------------------

# Reshaping 3x scaled 3D list into 1D list for PyPNG .write_array method
ResultImageAsList = IncSrc.Img3Dto1D(EPXImage, tripleX, tripleY, Z)

# --------------------------------------------------------------
# Hiding dialog

sortir.withdraw()

# Dialog hidden
# --------------------------------------------------------------

# --------------------------------------------------------------
# Open export file

resultPNG = filedialog.asksaveasfile(mode='wb', title='Save resulting Scale3x PNG file', filetypes=[('PNG','.png')], defaultextension = ('PNG file','.png'))
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

# --------------------------------------------------------------
# Destroying dialog

sortir.destroy()
sortir.mainloop()

# Dialog destroyed and closed
# --------------------------------------------------------------
