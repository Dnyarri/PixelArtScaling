#!/usr/bin/env python3

'''
Scale2x aka AdvMAME2x bitmap image scaling using Python only
Created by: Ilya Razmanov (mailto:ilyarazmanov@gmail.com)
            aka Ilyich the Toad (mailto:amphisoft@gmail.com)
Versions:
01.001      Scale2x (AdvMAME2x) seem to work 
01.002      Changed from self-contained to modular, IncSrc and IncScaleNx modules created 
01.003      Ultimate modular evil, moving everything possible to IncSrc.py and IncScaleNx.py 
01.004      Progress indication added, showing processing stage 
2024.02.24  Cleanup, GUI tweaks, versioning changed to YYYY.MM.DD
2024.03.30  pHYs chunk editing to keep image print size constant
2024.04.03  pathlib Path.exists flightcheck to make GUI Nuitka-proof
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

from tkinter import Tk
from tkinter import Label
from tkinter import filedialog

from pathlib import Path

import png                      # PNG reading: PyPNG from: https://gitlab.com/drj11/pypng
import IncSrc                   # Image reshaping from: https://github.com/Dnyarri/PixelArtScaling
from IncScaleNx import Scale2x  # Scale2x and Scale3x from: https://github.com/Dnyarri/PixelArtScaling

# --------------------------------------------------------------
# Creating dialog
iconpath = Path(__file__).resolve().parent / '2xGUI.ico'
iconname = str(iconpath)
useicon = iconpath.exists()     # Check if icon file really exist. If False, it will not be used later.

sortir = Tk()
sortir.title('Scale2x')
if useicon:
    sortir.iconbitmap(iconname) # Replacement for simple sortir.iconbitmap('2xGUI.ico') - ugly but stable.
sortir.geometry('+200+100')
zanyato = Label(sortir, text='Starting...', font=('arial', 16), padx=12, pady=10, justify='center')
zanyato.pack()
sortir.withdraw()
# Main dialog created and hidden

# Open source file
sourcefilename = filedialog.askopenfilename(title='Open source PNG file to reScale2x', filetypes=[('PNG', '.png')])
if sourcefilename == '':
    quit()

source = png.Reader(filename=sourcefilename)
X, Y, pixels, info = source.asDirect()  # Opening image, iDAT comes to "pixels" as bytearray, to be tuple'd lated.
Z = info['planes']                      # PyPNG returns X,Y directly, but not Z. Z should be extracted from info
imagedata = tuple((pixels))             # Attempt to fix all bytearrays as something solid
# Source file opened as imagedata

# Updating dialog
sortir.deiconify()
zanyato.config(text=f'Reading {sourcefilename}...')
sortir.update()
sortir.update_idletasks()
# Dialog shown and updated

# Reading image as list
ImageAsListListList = IncSrc.Img3D(imagedata, X, Y, Z)

# Updating dialog
zanyato.config(text=f'Scaling {sourcefilename}...')
sortir.update()
sortir.update_idletasks()

# Scaling list to 2x image list
EPXImage, doubleX, doubleY = Scale2x(ImageAsListListList, X, Y)

# Updating dialog
zanyato.config(text='Almost there...')
sortir.update()
sortir.update_idletasks()

# Reshaping 2x scaled 3D list into 1D list for PyPNG .write_array method
ResultImageAsList = IncSrc.Img3Dto1D(EPXImage, doubleX, doubleY, Z)

# Hiding dialog
sortir.withdraw()

# --------------------------------------------------------------
# Open export file
resultfilename = filedialog.asksaveasfilename(
    title='Save resulting Scale2x PNG file',
    filetypes=[('PNG', '.png')],
    defaultextension=('PNG file', '.png'),
)
if resultfilename == '':
    quit()
resultPNG = open(resultfilename, mode='wb')
# Export file opened

# --------------------------------------------------------------
# Fixing resolution to match original print size.
# If no pHYs found in original, 96 ppi is assumed as original value.
if 'physical' in info:
    res = info['physical']  # Reading resolution as tuple
    x_pixels_per_unit = res[0]
    y_pixels_per_unit = res[1]
    unit_is_meter = res[2]
else:
    x_pixels_per_unit = 3780  # 3780 px/meter = 96 px/inch, 2834 px/meter = 72 px/inch
    y_pixels_per_unit = 3780  # 3780 px/meter = 96 px/inch, 2834 px/meter = 72 px/inch
    unit_is_meter = True
x_pixels_per_unit = 2 * x_pixels_per_unit  # Double resolution to keep print size
y_pixels_per_unit = 2 * y_pixels_per_unit  # Double resolution to keep print size
# Resolution changed
# --------------------------------------------------------------

# Updating dialog
sortir.deiconify()
zanyato.config(text=f'Saving {resultfilename}...')
sortir.update()
sortir.update_idletasks()

# --------------------------------------------------------------
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
# Export file written and closed

# Destroying dialog
sortir.destroy()
sortir.mainloop()
