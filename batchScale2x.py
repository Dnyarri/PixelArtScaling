#!/usr/bin/env python

'''
Batch rescaling of PNG image using Scale2x aka AdvMAME2x
Created by: Ilya Razmanov (mailto:ilyarazmanov@gmail.com)
            aka Ilyich the Toad (mailto:amphisoft@gmail.com)
Versions:
01.000      Initial working release 
01.001      Progress indication added, showing name of file being processed
2024.02.24  Cleanup, GUI tweaks, versioning changed to YYYY.MM.DD
2024.03.30  pHYs chunk editing to keep image print size constant
2024.04.03  pathlib Path.exists flightcheck to make GUI Nuitka-proof
2024.04.23  Self-calling scalefile(runningfilename)
2024.04.23  Multiprocessing!!!
            pool.map version
            Unfortunately, GUI went to hell (mostly)
2024.04.24  pool.map_async will go to production

'''

__author__ = "Ilya Razmanov"
__copyright__ = "(c) 2024 Ilya Razmanov"
__credits__ = "Ilya Razmanov"
__license__ = "unlicense"
__version__ = "2024.04.24"
__maintainer__ = "Ilya Razmanov"
__email__ = "ilyarazmanov@gmail.com"
__status__ = "Production"

from tkinter import Tk, Label, filedialog
from pathlib import Path
from glob import glob
from multiprocessing import Pool

import png                      # PNG reading: PyPNG from:  https://gitlab.com/drj11/pypng
import IncSrc                   # Image reshaping from:     https://github.com/Dnyarri/PixelArtScaling
from IncScaleNx import Scale2x  # Scale2x and Scale3x from: https://github.com/Dnyarri/PixelArtScaling

def scalefile(runningfilename):
    '''
    Function that does all the job, and keeps quite. 

    '''

    oldfile = runningfilename
    newfile = oldfile  # Previous version used backup newfile = oldfile + '.2x.png'

    source = png.Reader(filename=oldfile)
    X, Y, pixels, info = source.asDirect()  # Opening image, iDAT comes to "pixels" as bytearray, to be tuple'd lated.
    Z = info['planes']                      # PyPNG returns X,Y directly, but not Z. Z should be extracted from info
    imagedata = tuple((pixels))             # Attempt to fix all bytearrays as something solid

    # Reading image as list
    ImageAsListListList = IncSrc.Img3D(imagedata, X, Y, Z)

    # Scaling list to 2x image list
    EPXImage, newX, newY = Scale2x(ImageAsListListList, X, Y)

    # Reshaping 2x scaled 3D list into 1D list for PyPNG .write_array method
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
    x_pixels_per_unit = 2 * x_pixels_per_unit   # Double resolution to keep print size
    y_pixels_per_unit = 2 * y_pixels_per_unit   # Double resolution to keep print size
    # Resolution changed
    # --------------------------------------------------------------

    # Writing new image
    resultPNG = open(newfile, mode='wb')
    writer = png.Writer(
        newX,
        newY,
        greyscale=info['greyscale'],
        alpha=info['alpha'],
        bitdepth=info['bitdepth'],
        physical=[x_pixels_per_unit, y_pixels_per_unit, unit_is_meter],
    )
    writer.write_array(resultPNG, ResultImageAsList)
    resultPNG.close()
# end scalefile, no return

if __name__ == '__main__':

    # Creating dialog
    iconpath = Path(__file__).resolve().parent / '2xBATCH.ico'
    iconname = str(iconpath)
    useicon = iconpath.exists() # Check if icon file really exist. If False, it will not be used later.

    sortir = Tk()
    sortir.title('Processing Scale2x...')
    if useicon:
        sortir.iconbitmap(iconname)
    sortir.geometry('+100+100')
    zanyato = Label(sortir, text='Allons-y!', font=("Arial", 16), state='disabled', padx=12, pady=10, justify='center')
    zanyato.pack()
    sortir.withdraw()
    # Main dialog created and hidden
    
    # Open source dir
    sourcedir = filedialog.askdirectory(title='Open DIR to resize PNG images using Scale2x')
    if sourcedir == '' or sourcedir == None:
        quit()

    # Updating dialog
    sortir.deiconify()
    zanyato.config(text='Asynchronous processes in action, just wait...')
    sortir.update()
    sortir.update_idletasks()
    
    # Creating pool
    scalepool = Pool()

    # Feeding pool (no pun!)
    scalepool.map_async(scalefile,glob(sourcedir + "/**/*.png", recursive=True))

    # Everything fed into the pool, waiting and closing
    scalepool.close()
    scalepool.join()

    # Destroying dialog
    sortir.destroy()
    sortir.mainloop()
