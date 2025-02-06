#!/usr/bin/env python3

"""
ScaleNx GUI
-

Created by: Ilya Razmanov (mailto:ilyarazmanov@gmail.com) aka Ilyich the Toad (mailto:amphisoft@gmail.com)

History:
-

25.01.17.00 Initial.

25.01.17.21 Fully operational.

-
Main site:  https://dnyarri.github.io

Project at Github:  https://github.com/Dnyarri/PixelArtScaling

"""

__author__ = 'Ilya Razmanov'
__copyright__ = '(c) 2025 Ilya Razmanov'
__credits__ = 'Ilya Razmanov'
__license__ = 'unlicense'
__version__ = '25.02.06.08'
__maintainer__ = 'Ilya Razmanov'
__email__ = 'ilyarazmanov@gmail.com'
__status__ = 'Production'

from multiprocessing import Pool, freeze_support
from pathlib import Path
from tkinter import Button, Frame, Label, Tk, filedialog
from tkinter.ttk import Separator

from pypng import pnglpng
from pypnm import pnmlpnm
from scalenx import scalenx, scalenxsfx


def DisMiss():
    """Kill dialog and continue"""

    sortir.destroy()


def UINormal():
    """Normal UI state, buttons enabled"""
    for widget in frame_left.winfo_children():
        if widget.winfo_class() in ('Label', 'Button'):
            widget.config(state='normal')
    for widget in frame_right.winfo_children():
        if widget.winfo_class() in ('Label', 'Button'):
            widget.config(state='normal')
    info_string.config(text=info_normal['txt'], foreground=info_normal['fg'], background=info_normal['bg'])


def UIWaiting():
    """Waiting UI state, buttons disabled"""
    for widget in frame_left.winfo_children():
        if widget.winfo_class() in ('Label', 'Button'):
            widget.config(state='disabled')
    for widget in frame_right.winfo_children():
        if widget.winfo_class() in ('Label', 'Button'):
            widget.config(state='disabled')
    info_string.config(text=info_waiting['txt'], foreground=info_waiting['fg'], background=info_waiting['bg'])
    sortir.update()


def UIBusy():
    """Busy UI state, buttons disabled"""
    for widget in frame_left.winfo_children():
        if widget.winfo_class() in ('Label', 'Button'):
            widget.config(state='disabled')
    for widget in frame_right.winfo_children():
        if widget.winfo_class() in ('Label', 'Button'):
            widget.config(state='disabled')
    info_string.config(text=info_busy['txt'], foreground=info_busy['fg'], background=info_busy['bg'])
    sortir.update()


def FileNx(size: int, sfx: bool) -> None:
    """Single file ScaleNx with variable N and method.

    Arguments:
        size: scale size, either 2 or 3.
        sfx: use either sfx or classic scaler version.
    """

    UIWaiting()

    # Open source file
    sourcefilename = filedialog.askopenfilename(title='Open image file to rescale', filetypes=[('Supported formats', '.png .ppm .pgm .pbm'), ('PNG', '.png'), ('PNM', '.ppm .pgm .pbm')])
    if sourcefilename == '':
        UINormal()
        return None

    UIBusy()

    if Path(sourcefilename).suffix == '.png':
        # Reading image as list
        X, Y, Z, maxcolors, image3d, info = pnglpng.png2list(sourcefilename)

    elif Path(sourcefilename).suffix in ('.ppm', '.pgm', '.pbm'):
        # Reading image as list
        X, Y, Z, maxcolors, image3d = pnmlpnm.pnm2list(sourcefilename)
        # Creating dummy info
        info = {}
        # Fixing color mode. The rest is fixed with pnglpng v. 25.01.07.
        if maxcolors > 255:
            info['bitdepth'] = 16
        else:
            info['bitdepth'] = 8

    else:
        raise ValueError('Extension not recognized')

    # Choosing working scaler from the list of imported scalers
    if sfx:
        if size == 2:
            chosen_scaler = scalenxsfx.scale2x
        if size == 3:
            chosen_scaler = scalenxsfx.scale3x
    else:
        if size == 2:
            chosen_scaler = scalenx.scale2x
        if size == 3:
            chosen_scaler = scalenx.scale3x

    # Scaling using scaler chosen above
    scaled_image = chosen_scaler(image3d)

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

    # Adjusting "Save to" formats to be displayed according to bitdepth
    if Z < 3:
        format = [('PNG', '.png'), ('Portable grey map', '.pgm')]
    else:
        format = [('PNG', '.png'), ('Portable pixel map', '.ppm')]

    UIWaiting()

    # Open export file
    resultfilename = filedialog.asksaveasfilename(
        title='Save image file',
        filetypes=format,
        defaultextension=('PNG file', '.png'),
    )
    if resultfilename == '':
        UINormal()
        return None

    UIBusy()

    if Path(resultfilename).suffix == '.png':
        pnglpng.list2png(resultfilename, scaled_image, info)
    elif (Path(resultfilename).suffix == '.ppm') or (Path(resultfilename).suffix == '.pgm'):
        pnmlpnm.list2pnm(resultfilename, scaled_image, maxcolors)

    UINormal()

    return None


def scalefile(runningfilename: str, size: int, sfx: bool) -> None:
    """Function upscales one file and keeps quite.

    Arguments:
        runningfilename: name of file to process
        size: scale size, either 2 or 3.
        sfx: use either sfx or classic scaler version.
    """

    oldfile = str(runningfilename)
    newfile = oldfile  # Previous version used backup newfile = oldfile + '.2x.png'

    # Reading image as list
    X, Y, Z, maxcolors, image3d, info = pnglpng.png2list(oldfile)

    # Choosing working scaler from the list of imported scalers
    if sfx:
        if size == 2:
            chosen_scaler = scalenxsfx.scale2x
        if size == 3:
            chosen_scaler = scalenxsfx.scale3x
    else:
        if size == 2:
            chosen_scaler = scalenx.scale2x
        if size == 3:
            chosen_scaler = scalenx.scale3x

    # Scaling using scaler chosen above
    scaled_image = chosen_scaler(image3d)

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
    pnglpng.list2png(newfile, scaled_image, info)  # end scalefile, no return

    return None


def FolderNx(size: int, sfx: bool) -> None:
    """Multiprocessing pool to feed `scalefile` processes to.

    Arguments:
        size: scale size, either 2 or 3.
        sfx: use either sfx or classic scaler version.
    """

    UIWaiting()

    # Open source dir
    sourcedir = filedialog.askdirectory(title='Open folder to rescale PNG images')
    if sourcedir == '':
        UINormal()
        return None

    path = Path(sourcedir)

    UIBusy()

    # Creating pool
    scalepool = Pool()

    # Feeding the pool (no pun!)
    for runningfilename in path.rglob('*.png'):
        scalepool.apply_async(
            scalefile,
            args=(
                runningfilename,
                size,
                sfx,
            ),
        )

    # Everything fed into the pool, waiting and closing
    scalepool.close()
    scalepool.join()

    UINormal()

    return None


""" ╔═══════════╗
    ║ Main body ║
    ╚═══════════╝ """

if __name__ == '__main__':
    freeze_support()  # Freezing for exe

    sortir = Tk()

    # Info statuses dictionaries
    info_normal = {'txt': f'ScaleNx ver. {__version__} at your command', 'fg': 'grey', 'bg': 'light grey'}
    info_waiting = {'txt': 'Waiting for input', 'fg': 'green', 'bg': 'light grey'}
    info_busy = {'txt': 'BUSY, PLEASE WAIT', 'fg': 'red', 'bg': 'yellow'}

    iconpath = Path(__file__).resolve().parent / '32.ico'
    if iconpath.exists():
        sortir.iconbitmap(str(iconpath))

    sortir.title('ScaleNx')
    sortir.geometry('+200+100')
    sortir.minsize(540, 400)

    butt99 = Button(sortir, text='Exit', font=('helvetica', 14), cursor='hand2', justify='center', state='normal', command=DisMiss)
    butt99.pack(side='bottom', padx=4, pady=2, fill='both')

    info_string = Label(sortir, text=info_normal['txt'], font=('courier', 10), foreground=info_normal['fg'], background=info_normal['bg'], relief='groove')
    info_string.pack(side='bottom', padx=2, pady=[6, 1], fill='both')

    frame_left = Frame(sortir, borderwidth=2, relief='groove')
    frame_left.pack(side='left', anchor='nw', padx=2, pady=[0, 12])

    sep_middle1 = Separator(sortir, orient='vertical')
    sep_middle1.pack(side='left', padx=2, pady=12, fill='y')

    frame_right = Frame(sortir, borderwidth=2, relief='groove')
    frame_right.pack(side='right', anchor='nw', padx=2, pady=[0, 12])

    sep_middle2 = Separator(sortir, orient='vertical')
    sep_middle2.pack(side='right', padx=2, pady=12, fill='y')

    label00 = Label(frame_left, text='ScaleNx', font=('helvetica', 20), justify='center', padx=12, pady=2, borderwidth=2, relief='flat', foreground='brown', background='light grey')
    label00.pack(side='top', pady=0, fill='both')

    sep01 = Separator(frame_left, orient='horizontal')
    sep01.pack(side='top', padx=0, pady=[0, 12], fill='x')

    label01 = Label(frame_left, text='Single file rescaling (PNG, PPM, PGM)'.center(40, ' '), font=('helvetica', 10), justify='center', padx=12, pady=2, borderwidth=2, relief='flat', foreground='dark blue')
    label01.pack(side='top', pady=0)

    butt01 = Button(frame_left, text='Open file ➔ 2x', font=('helvetica', 14), cursor='hand2', justify='center', state='normal', command=lambda: FileNx(2, False))
    butt01.pack(side='top', padx=4, pady=[4, 12], fill='both')

    butt02 = Button(frame_left, text='Open file ➔ 3x', font=('helvetica', 14), cursor='hand2', justify='center', state='normal', command=lambda: FileNx(3, False))
    butt02.pack(side='top', padx=4, pady=2, fill='both')

    sep02 = Separator(frame_left, orient='horizontal')
    sep02.pack(side='top', padx=0, pady=[0, 12], fill='x')

    label02 = Label(frame_left, text='Folder batch process (PNG only)', font=('helvetica', 10), justify='center', borderwidth=2, relief='flat', foreground='dark blue')
    label02.pack(side='top', pady=[12, 0])

    butt03 = Button(frame_left, text='Select folder ➔ 2x', font=('helvetica', 14), cursor='hand2', justify='center', state='normal', command=lambda: FolderNx(2, False))
    butt03.pack(side='top', padx=4, pady=2, fill='both')

    butt04 = Button(frame_left, text='Select folder ➔ 3x', font=('helvetica', 14), cursor='hand2', justify='center', state='normal', command=lambda: FolderNx(3, False))
    butt04.pack(side='top', padx=4, pady=2, fill='both')

    label10 = Label(frame_right, text='ScaleNxSFX', font=('helvetica', 20), justify='center', padx=12, pady=2, borderwidth=2, relief='flat', foreground='brown', background='light grey')
    label10.pack(side='top', pady=0, fill='both')

    sep11 = Separator(frame_right, orient='horizontal')
    sep11.pack(side='top', padx=0, pady=[0, 12], fill='x')

    label11 = Label(frame_right, text='Single file rescaling (PNG, PPM, PGM)'.center(40, ' '), font=('helvetica', 10), justify='center', padx=12, pady=2, borderwidth=2, relief='flat', foreground='dark blue')
    label11.pack(side='top', pady=0)

    butt11 = Button(frame_right, text='Open file ➔ 2xSFX', font=('helvetica', 14), cursor='hand2', justify='center', command=lambda: FileNx(2, True))
    butt11.pack(side='top', padx=4, pady=[4, 12], fill='both')

    butt12 = Button(frame_right, text='Open file ➔ 3xSFX', font=('helvetica', 14), cursor='hand2', justify='center', state='normal', command=lambda: FileNx(3, True))
    butt12.pack(side='top', padx=4, pady=2, fill='both')

    sep12 = Separator(frame_right, orient='horizontal')
    sep12.pack(side='top', padx=0, pady=[0, 12], fill='x')

    label12 = Label(frame_right, text='Folder batch process (PNG only)', font=('helvetica', 10), justify='center', borderwidth=2, relief='flat', foreground='dark blue')
    label12.pack(side='top', pady=[12, 0])

    butt13 = Button(frame_right, text='Select folder ➔ 2xSFX', font=('helvetica', 14), cursor='hand2', justify='center', state='normal', command=lambda: FolderNx(2, True))
    butt13.pack(side='top', padx=4, pady=2, fill='both')

    butt14 = Button(frame_right, text='Select folder ➔ 3xSFX', font=('helvetica', 14), cursor='hand2', justify='center', state='normal', command=lambda: FolderNx(3, True))
    butt14.pack(side='top', padx=4, pady=2, fill='both')

    sortir.mainloop()
