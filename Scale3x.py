#!/usr/bin/env python3

'''
Scale3x aka AdvMAME3x bitmap image scaling using Python only, merged command line and GUI versions.
Created by: Ilya Razmanov (mailto:ilyarazmanov@gmail.com)
            aka Ilyich the Toad (mailto:amphisoft@gmail.com)

Usage:
    python Scale3x.py source.png result.png - rescales source.png and writes result.png
    python Scale3x.py source.png            - rescales source.png and overwrites source.png
    python Scale3x.py                       - starts GUI for selecting source and result

Versions:
2024.05.11  Initial release of merged GUI and CLI versions.
2024.05.14  Linked with IncSrc and IncScaleNx version 2024.05.14,
            data exchange format changed to incompatible with previous versions.

'''

__author__ = 'Ilya Razmanov'
__copyright__ = '(c) 2024 Ilya Razmanov'
__credits__ = 'Ilya Razmanov'
__license__ = 'unlicense'
__version__ = '2024.05.17'
__maintainer__ = 'Ilya Razmanov'
__email__ = 'ilyarazmanov@gmail.com'
__status__ = 'Production'

from sys import argv

import png                      # PNG reading: PyPNG from: https://gitlab.com/drj11/pypng
import IncSrc                   # Image reshaping from: https://github.com/Dnyarri/PixelArtScaling
from IncScaleNx import Scale3x  # Scale2x and Scale3x from: https://github.com/Dnyarri/PixelArtScaling

def cli(Rez, Dvo):
    '''
    Command line variant of Scale3x. Input - source and result PNG filenames.

    '''

    # --------------------------------------------------------------
    # Open source file
    source = png.Reader(filename=Rez)

    X, Y, pixels, info = source.asDirect()  # Opening image, iDAT comes to "pixels" as bytearray, to be tuple'd lated.
    Z = info['planes']                      # Maximum CHANNEL NUMBER
    imagedata = tuple((pixels))             # Attempt to fix all bytearrays
    # Source file opened as imagedata

    # Reading image as list
    ImageAsListListList = IncSrc.Img3D(imagedata, X, Y, Z)

    # Scaling to 3x image list
    EPXImage = Scale3x(ImageAsListListList)
    
    # determining image size from list
    newY = len(EPXImage)
    newX = len(EPXImage[0])

    # Reshaping 3x scaled 3D list into 1D list for PyPNG .write_array method
    ResultImageAsList = IncSrc.Img3Dto1D(EPXImage)

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

    # Open export file
    resultPNG = open(Dvo, mode='wb')

    # Writing export file
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
    # Export file closed

    return None
# end of CLI variant

def gui():
    '''
    GUI variant of Scale3x, based on tkinter.

    '''

    from tkinter import Tk, filedialog, Label
    from pathlib import Path

    # --------------------------------------------------------------
    # Creating dialog
    iconpath = Path(__file__).resolve().parent / '3x.ico'
    iconname = str(iconpath)
    useicon = iconpath.exists()     # Check if icon file really exist. If False, it will not be used later.

    sortir = Tk()
    sortir.title('Scale3x')
    if useicon:
        sortir.iconbitmap(iconname) # Replacement for simple sortir.iconbitmap('3xGUI.ico') - ugly but stable.
    sortir.geometry('+200+100')
    zanyato = Label(sortir, text='Starting...', font=('arial', 14), padx=14, pady=10, justify='center')
    zanyato.pack()
    sortir.withdraw()
    # Main dialog created and hidden

    # Open source file
    sourcefilename = filedialog.askopenfilename(title='Open source PNG file to reScale3x', filetypes=[('PNG', '.png')])
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

    # Scaling to 3x image list
    EPXImage = Scale3x(ImageAsListListList)
    
    # determining image size from list
    newY = len(EPXImage)
    newX = len(EPXImage[0])

    # Updating dialog
    zanyato.config(text='Almost there...')
    sortir.update()
    sortir.update_idletasks()

    # Reshaping 3x scaled 3D list into 1D list for PyPNG .write_array method
    ResultImageAsList = IncSrc.Img3Dto1D(EPXImage)

    # Hiding dialog
    sortir.withdraw()

    # Open export file
    resultfilename = filedialog.asksaveasfilename(
        title='Save resulting Scale3x PNG file',
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

    # Updating dialog
    sortir.deiconify()
    zanyato.config(text=f'Saving {resultfilename}...')
    sortir.update()
    sortir.update_idletasks()

    # Writing export file
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
    # Export file written and closed

    # Destroying dialog
    sortir.destroy()
    sortir.mainloop()

    return None
# end of GUI variant

if __name__ == '__main__':

    # Taking user input

    if len(argv) == 2:
        Rez = argv[1]
        Dvo = argv[1]   # will overwrite source file
        cli(Rez, Dvo)
    elif len(argv) == 3:
        Rez = argv[1]
        Dvo = argv[2]   # will write new file
        cli(Rez, Dvo)
    else:
        gui()           # will open GUI
