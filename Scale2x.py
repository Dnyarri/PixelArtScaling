#!/usr/bin/env python3

"""
Scale2x aka AdvMAME2x bitmap image scaling using Python only, merged command line and GUI versions.
Created by: Ilya Razmanov (mailto:ilyarazmanov@gmail.com)
            aka Ilyich the Toad (mailto:amphisoft@gmail.com)

Usage:
    python Scale2x.py source.png result.png - rescales source.png and writes result.png
    python Scale2x.py source.png            - rescales source.png and overwrites source.png
    python Scale2x.py                       - starts GUI for selecting source and result

History:

2024.05.11  Initial release of merged GUI and CLI versions.
2024.05.14  Linked with IncSrc and IncScaleNx version 2024.05.14, data exchange format changed to incompatible with previous versions.
24.08.01    Complete I/O change, excluding IncSrc in favour of pnglpng.
24.10.01    Internal restructure, imports change.
25.01.01    PPM and PGM read and write support added, PBM read only.

"""

__author__ = 'Ilya Razmanov'
__copyright__ = '(c) 2024 Ilya Razmanov'
__credits__ = 'Ilya Razmanov'
__license__ = 'unlicense'
__version__ = '25.01.01'
__maintainer__ = 'Ilya Razmanov'
__email__ = 'ilyarazmanov@gmail.com'
__status__ = 'Production'

from pathlib import Path
from sys import argv

import pnglpng  # PNG-list-PNG joint, uses PyPNG
import pnmlpnm  # PNM-list-PNM
from scalenx import scale2x  # Scale2x and Scale3x from: https://github.com/Dnyarri/PixelArtScaling

""" ╔═════════════════════╗
    ║ commandline variant ║
    ╚═════════════════════╝ """

def cli(Rez, Dvo):
    """
    Command line variant of Scale2x. Input - source and result PNG filenames.

    """

    # --------------------------------------------------------------
    # Open source file

    if Path(Rez).suffix == '.png':
        # Reading image as list
        X, Y, Z, maxcolors, ImageAsListListList, info = pnglpng.png2list(Rez)

    elif (Path(Rez).suffix in ('.ppm', '.pgm', '.pbm')):
        # Reading image as list
        X, Y, Z, maxcolors, ImageAsListListList = pnmlpnm.pnm2list(Rez)
        # Creating dummy info
        info = {}
        # Fixing color mode. So far pnglpng does not make any assumptions on that; guess it must be fixed later.
        if Z < 3:
            info['greyscale'] = True
        else:
            info['greyscale'] = False
        if maxcolors > 255:
            info['bitdepth'] = 16

    else:
        raise ValueError('Extension not recognized')

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

    if Path(Dvo).suffix == '.png':
        pnglpng.list2png(Dvo, EPXImage, info)
    elif (Path(Dvo).suffix in ('.ppm', '.pgm')):
        pnmlpnm.list2pnm(Dvo, EPXImage, maxcolors)
    else:
        raise ValueError('Extension not recognized')

    return None  # end of CLI variant


""" ╔═════════════╗
    ║ GUI variant ║
    ╚═════════════╝ """

def gui():
    """
    GUI variant of Scale2x, based on tkinter.

    """

    from tkinter import Label, Tk, filedialog

    # Creating dialog
    iconpath = Path(__file__).resolve().parent / '2x.ico'
    iconname = str(iconpath)
    useicon = iconpath.exists()  # Check if icon file really exist. If False, it will not be used later.

    sortir = Tk()
    sortir.title('Scale2x')
    if useicon:
        sortir.iconbitmap(iconname)  # Replacement for simple sortir.iconbitmap('2xGUI.ico') - ugly but stable
    sortir.geometry('+200+100')
    zanyato = Label(sortir, text='Starting...', font=('arial', 14), padx=14, pady=10, justify='center')
    zanyato.pack()
    sortir.withdraw()
    # Main dialog created and hidden

    # Open source file
    sourcefilename = filedialog.askopenfilename(title='Open image file to reScale2x', filetypes=[('Supported formats', '.png .ppm .pgm .pbm'), ('PNG', '.png'), ('PNM', '.ppm .pgm .pbm')])
    if sourcefilename == '':
        return None

    # Updating dialog
    sortir.deiconify()
    zanyato.config(text=f'Reading {sourcefilename}...')
    sortir.update()
    sortir.update_idletasks()
    # Dialog shown and updated

    if Path(sourcefilename).suffix == '.png':
        # Reading image as list
        X, Y, Z, maxcolors, ImageAsListListList, info = pnglpng.png2list(sourcefilename)

    elif (Path(sourcefilename).suffix in ('.ppm', '.pgm', '.pbm')):
        # Reading image as list
        X, Y, Z, maxcolors, ImageAsListListList = pnmlpnm.pnm2list(sourcefilename)
        # Creating dummy info
        info = {}
        # Fixing color mode. So far pnglpng does not make any assumptions on that; guess it must be fixed later.
        if Z < 3:
            info['greyscale'] = True
        else:
            info['greyscale'] = False
        if maxcolors > 255:
            info['bitdepth'] = 16

    else:
        raise ValueError('Extension not recognized')

    # Updating dialog
    zanyato.config(text=f'Scaling {sourcefilename}...')
    sortir.update()
    sortir.update_idletasks()

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

    # Hiding dialog
    sortir.withdraw()

    # Adjusting "Save to" formats to be displayed according to bitdepth
    if Z < 3:
        format = [('PNG', '.png'), ('Portable grey map', '.pgm')]
    else:
        format = [('PNG', '.png'), ('Portable pixel map', '.ppm')]

    # Open export file
    resultfilename = filedialog.asksaveasfilename(
        title='Save Scale2x image file',
        filetypes=format,
        defaultextension=('PNG file', '.png'),
    )
    if resultfilename == '':
        return None

    # Updating dialog
    sortir.deiconify()
    zanyato.config(text=f'Saving {resultfilename}...')
    sortir.update()
    sortir.update_idletasks()

    if Path(resultfilename).suffix == '.png':
        pnglpng.list2png(resultfilename, EPXImage, info)
    elif (Path(resultfilename).suffix == '.ppm') or (Path(resultfilename).suffix == '.pgm'):
        pnmlpnm.list2pnm(resultfilename, EPXImage, maxcolors)

    # Destroying dialog
    sortir.destroy()
    sortir.mainloop()

    return None  # end of GUI variant


# --------------------------------------------------------------

if __name__ == '__main__':
    # Taking user input

    if len(argv) == 2:
        Rez = argv[1]
        Dvo = argv[1]  # will overwrite source file
        cli(Rez, Dvo)
    elif len(argv) == 3:
        Rez = argv[1]
        Dvo = argv[2]  # will write new file
        cli(Rez, Dvo)
    else:
        gui()  # will open GUI
