#!/usr/bin/env python3

'''
Batch rescaling of PNG image using Scale2x aka AdvMAME2x
Created by: Ilya Razmanov (mailto:ilyarazmanov@gmail.com)
            aka Ilyich the Toad (mailto:amphisoft@gmail.com)
Versions:
01.000      Initial working release. 
2024.02.24  Cleanup, GUI tweaks, versioning changed to YYYY.MM.DD
2024.03.30  pHYs chunk editing to keep image print size constant.
2024.04.03  pathlib Path.exists flightcheck to make GUI exe packagers-friendly,
            glob replaced with path.rglob
2024.04.23  Self-calling scalefile(runningfilename)
2024.04.23  Multiprocessing introduced, pool.map_async version will go to production.
            GUI hangs and not updated, but now it apologize.
2024.05.14  Linked with IncSrc and IncScaleNx version 2024.05.14,
            data exchange format changed to incompatible with previous versions.
24.08.01    Complete I/O change, excluding IncSrc in favour of pnglpng.
24.10.01    Internal restructure.

'''

__author__ = 'Ilya Razmanov'
__copyright__ = '(c) 2024 Ilya Razmanov'
__credits__ = 'Ilya Razmanov'
__license__ = 'unlicense'
__version__ = '24.10.01'
__maintainer__ = 'Ilya Razmanov'
__email__ = 'ilyarazmanov@gmail.com'
__status__ = 'Production'

from multiprocessing import Pool, freeze_support
from pathlib import Path
from tkinter import Label, Tk, X, filedialog

import pnglpng  # PNG-list-PNG joint, uses PyPNG
from scalenx import scale2x  # Scale2x and Scale3x from: https://github.com/Dnyarri/PixelArtScaling


def scalefile(runningfilename):
    '''
    Function that does all the job, and keeps quite.

    '''

    oldfile = str(runningfilename)
    newfile = oldfile  # Previous version used backup newfile = oldfile + '.2x.png'

    # Reading image as list
    ImageAsListListList = pnglpng.png2list(oldfile)[4]
    info = pnglpng.png2list(oldfile)[5]

    # Scaling list to 2x image list
    EPXImage = scale2x(ImageAsListListList)

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

    info['physical'] = [x_pixels_per_unit, y_pixels_per_unit, unit_is_meter]
    # Resolution changed
    # --------------------------------------------------------------

    # Explicitly setting compression
    info['compression'] = 9

    # Writing PNG file
    pnglpng.list2png(newfile, EPXImage, info)  # end scalefile, no return


# --------------------------------------------------------------

if __name__ == '__main__':

    # Freezing for exe
    freeze_support()

    # Creating dialog
    iconpath = Path(__file__).resolve().parent / 'b2x.ico'
    iconname = str(iconpath)
    useicon = iconpath.exists()  # Check if icon file really exist. If False, it will not be used later.

    sortir = Tk()
    sortir.title('Processing Scale2x...')
    if useicon:
        sortir.iconbitmap(iconname)
    sortir.geometry('+200+100')
    zanyato = Label(sortir, text='Allons-y!', font=('Arial', 16), state='normal', padx=12, pady=10, justify='center')
    zanyato.pack()
    small = Label(
        sortir,
        text='At 100% CPU load GUI tend to become unresponsive.\nWe apologize for making image processing as fast as possible.',
        font=('Courier', 10),
        state='disabled',
        padx=12,
        pady=10,
        justify='center',
    )
    small.pack(fill=X)
    sortir.withdraw()
    # Main dialog created and hidden

    # Open source dir
    sourcedir = filedialog.askdirectory(title='Open DIR to resize PNG images using Scale2x')
    if sourcedir == '' or sourcedir is None:
        sortir.destroy()
        quit()
    path = Path(sourcedir)

    # Updating dialog
    sortir.deiconify()
    zanyato.config(text='Asynchronous processes ensued, pronto!')
    sortir.update()
    sortir.update_idletasks()

    # Creating pool
    scalepool = Pool()

    # Feeding pool (no pun!)
    scalepool.map_async(scalefile, path.rglob('*.png'))

    # Everything fed into the pool, waiting and closing
    scalepool.close()
    scalepool.join()

    # Destroying dialog
    sortir.destroy()
    sortir.mainloop()
