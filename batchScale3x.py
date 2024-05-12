#!/usr/bin/env python3

'''
Batch rescaling of PNG image using Scale3x aka AdvMAME3x
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
2024.04.24  Async variants halve processing time, pool.map_async will go to production
2024.04.26  GUI still sucks and not updated, but now it apologize

'''

__author__ = "Ilya Razmanov"
__copyright__ = "(c) 2024 Ilya Razmanov"
__credits__ = "Ilya Razmanov"
__license__ = "unlicense"
__version__ = "2024.04.26"
__maintainer__ = "Ilya Razmanov"
__email__ = "ilyarazmanov@gmail.com"
__status__ = "Production"

from tkinter import Tk, Label, filedialog, X
from pathlib import Path
from multiprocessing import Pool, freeze_support

import png                      # PNG reading: PyPNG from:  https://gitlab.com/drj11/pypng
import IncSrc                   # Image reshaping from:     https://github.com/Dnyarri/PixelArtScaling
from IncScaleNx import Scale3x  # Scale2x and Scale3x from: https://github.com/Dnyarri/PixelArtScaling

def scalefile(runningfilename):
    '''
    Function that does all the job, and keeps quite. 

    '''

    oldfile = runningfilename
    newfile = oldfile  # Previous version used backup newfile = oldfile + '.3x.png'

    source = png.Reader(filename=oldfile)
    X, Y, pixels, info = source.asDirect()  # Opening image, iDAT comes to "pixels" as bytearray, to be tuple'd lated.
    Z = info['planes']                      # PyPNG returns X,Y directly, but not Z. Z should be extracted from info
    imagedata = tuple((pixels))             # Attempt to fix all bytearrays as something solid

    # Reading image as list
    ImageAsListListList = IncSrc.Img3D(imagedata, X, Y, Z)

    # Scaling list to 3x image list
    EPXImage, newX, newY = Scale3x(ImageAsListListList, X, Y)

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
    x_pixels_per_unit = 3 * x_pixels_per_unit   # Triple resolution to keep print size
    y_pixels_per_unit = 3 * y_pixels_per_unit   # Triple resolution to keep print size
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

    # Freezing for exe
    freeze_support()

    # Creating dialog
    iconpath = Path(__file__).resolve().parent / '3xBATCH.ico'
    iconname = str(iconpath)
    useicon = iconpath.exists() # Check if icon file really exist. If False, it will not be used later.

    sortir = Tk()
    sortir.title('Processing Scale3x...')
    if useicon:
        sortir.iconbitmap(iconname)
    sortir.geometry('+200+100')
    zanyato = Label(sortir, text='Allons-y!', font=("Arial", 16), state='normal', padx=12, pady=10, justify='center')
    zanyato.pack()
    small = Label(sortir, text='At 100% CPU load GUI tend to become unresponsive.\nWe apologize for making image processing as fast as possible.', font=("Courier", 10), state='disabled', padx=12, pady=10, justify='center')
    small.pack(fill=X)
    sortir.withdraw()
    # Main dialog created and hidden
    
    # Open source dir
    sourcedir = filedialog.askdirectory(title='Open DIR to resize PNG images using Scale3x')
    if sourcedir == '' or sourcedir == None:
        sortir.destroy()
        quit()
    path=Path(sourcedir)

    # Updating dialog
    sortir.deiconify()
    zanyato.config(text='Asynchronous processes ensued, pronto!')
    sortir.update()
    sortir.update_idletasks()
    
    # Creating pool
    scalepool = Pool()

    # Feeding pool (no pun!)
    scalepool.map_async(scalefile,path.rglob('*.png'))

    # Everything fed into the pool, waiting and closing
    scalepool.close()
    scalepool.join()

    # Destroying dialog
    sortir.destroy()
    sortir.mainloop()
