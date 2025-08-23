#!/usr/bin/env python3

"""
ScaleNx GUI - Common shell for ScaleNx single file and batch PNG, PPM and PGM rescaling. NOTE: This is special Python 3.4 compatible build.
---

Created by: Ilya Razmanov <ilyarazmanov@gmail.com> aka Ilyich the Toad <amphisoft@gmail.com>

History:
---

25.01.17.00 Initial GUI version.

25.01.17.21 Fully operational.

25.03.01.01 PNM batch processing added. GUI simplified to reduce imports.

25.08.20.34 Numerous GUI updates; simulating MRU for old Tkinter.

25.08.22.34 Intentionally downgraded from `pathlib` to `os`.
PNG compression and PNM format prefs may be saved/loaded to/from file.

---
Main site:  <https://dnyarri.github.io>

Project at Github:  <https://github.com/Dnyarri/PixelArtScaling>

"""

__author__ = 'Ilya Razmanov'
__copyright__ = '(c) 2025 Ilya Razmanov'
__credits__ = 'Ilya Razmanov'
__license__ = 'unlicense'
__version__ = '25.08.22.34'
__maintainer__ = 'Ilya Razmanov'
__email__ = 'ilyarazmanov@gmail.com'
__status__ = 'Production'

import os
from json import dump, load
from multiprocessing import Pool, freeze_support
from time import ctime, time
from tkinter import Button, Frame, Label, Tk
from tkinter.filedialog import askdirectory, askopenfilename, asksaveasfilename

from pypng.pnglpng import list2png, png2list
from pypnm.pnmlpnm import list2pnm, pnm2list
from scalenx import scalenx, scalenxsfx


def DisMiss(event=None) -> None:
    """Kill dialog and continue"""

    sortir.destroy()
    return None


def UINormal():
    """Normal UI state, buttons enabled"""

    for widget in frame_left.winfo_children():
        if widget.winfo_class() in ('Label', 'Button'):
            widget.config(state='normal')
    for widget in frame_right.winfo_children():
        if widget.winfo_class() in ('Label', 'Button'):
            widget.config(state='normal')
    info_string.config(text=info_normal['txt'], foreground=info_normal['fg'], background=info_normal['bg'], state=info_normal['status'])
    sortir.update()
    return None


def UIWaiting():
    """Waiting UI state, buttons disabled"""

    for widget in frame_left.winfo_children():
        if widget.winfo_class() in ('Label', 'Button'):
            widget.config(state='disabled')
    for widget in frame_right.winfo_children():
        if widget.winfo_class() in ('Label', 'Button'):
            widget.config(state='disabled')
    info_string.config(text=info_waiting['txt'], foreground=info_waiting['fg'], background=info_waiting['bg'], disabledforeground=info_waiting['fg'], state=info_waiting['status'])
    sortir.update()
    return None


def UIBusy():
    """Busy UI state, buttons disabled"""

    for widget in frame_left.winfo_children():
        if widget.winfo_class() in ('Label', 'Button'):
            widget.config(state='disabled')
    for widget in frame_right.winfo_children():
        if widget.winfo_class() in ('Label', 'Button'):
            widget.config(state='disabled')
    info_string.config(text=info_busy['txt'], foreground=info_busy['fg'], background=info_busy['bg'], disabledforeground=info_busy['fg'], state=info_busy['status'])
    sortir.update()
    return None


def FileNx(size, sfx):
    """Single file ScaleNx with variable N and method.

    Arguments:
        size: scale size, either 2 or 3;
        sfx: use either sfx or classic scaler version.
    """

    global mru  # Remember MRU directory for old Tkinter

    UIWaiting()

    # ↓ Open source file
    sourcefilename = askopenfilename(title='Open image file to rescale', initialdir=mru, filetypes=[('Supported formats', '.png .ppm .pgm .pbm'), ('Portable network graphics', '.png'), ('Portable network map', '.ppm .pgm .pbm')])
    if sourcefilename == '':
        UINormal()
        return None
    mru = os.path.dirname(sourcefilename)
    UIBusy()

    if os.path.splitext(sourcefilename)[1] == '.png':
        # ↓ Reading image as list
        X, Y, Z, maxcolors, image3d, info = png2list(sourcefilename)

    elif os.path.splitext(sourcefilename)[1] in ('.ppm', '.pgm', '.pbm'):
        # ↓ Reading image as list
        X, Y, Z, maxcolors, image3d = pnm2list(sourcefilename)
        # ↓ Creating dummy info
        info = {}
        # ↓ Fixing color mode. The rest is fixed with pnglpng v. 25.01.07.
        info['bitdepth'] = 16 if maxcolors > 255 else 8

    else:
        raise ValueError('Extension not recognized')

    # ↓ Choosing working scaler from the list of imported scalers
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

    # ↓ Scaling using scaler chosen above
    scaled_image = chosen_scaler(image3d)

    # ↓ Fixing resolution to match original print size.
    #   If no pHYs found in original, 96 ppi is assumed as original value.
    if 'physical' in info:
        res = info['physical']  # Reading resolution as tuple
        x_pixels_per_unit = res[0]
        y_pixels_per_unit = res[1]
        unit_is_meter = res[2]
    else:
        x_pixels_per_unit = y_pixels_per_unit = 3780
        # 3780 px/meter = 96 px/inch, 2834 px/meter = 72 px/inch
        unit_is_meter = True

    x_pixels_per_unit = size * x_pixels_per_unit  # Change resolution to keep print size
    y_pixels_per_unit = size * y_pixels_per_unit  # Change resolution to keep print size

    info['physical'] = [x_pixels_per_unit, y_pixels_per_unit, unit_is_meter]
    # ↑ Resolution changed

    # ↓ Explicitly setting compression for a single file processing
    info['compression'] = prefs['single_deflation']

    # ↓ Adjusting "Save to" formats to be displayed according to bitdepth
    if Z == 1:
        format = [('Portable network graphics', '.png'), ('Portable grey map', '.pgm')]
    elif Z == 3:
        format = [('Portable network graphics', '.png'), ('Portable pixel map', '.ppm')]
    else:
        format = [('Portable network graphics', '.png')]

    UIWaiting()

    # ↓ Open export file
    resultfilename = asksaveasfilename(
        title='Save image file',
        initialdir=mru,
        filetypes=format,
        defaultextension='.png',
    )
    if resultfilename == '':
        UINormal()
        return None

    UIBusy()

    if os.path.splitext(sourcefilename)[1] == '.png':
        list2png(resultfilename, scaled_image, info)
    elif os.path.splitext(sourcefilename)[1] in ('.ppm', '.pgm'):
        list2pnm(resultfilename, scaled_image, maxcolors, bin=prefs['single_binarity'])

    UINormal()
    return None


def scale_file_png(runningfilename, size, sfx, compression):
    """Function upscales one PNG file and keeps quite.

    Arguments:
        runningfilename: name of file to process;
        size: scale size, either 2 or 3;
        sfx: use either sfx or classic scaler version.
    """

    oldfile = str(runningfilename)
    newfile = oldfile  # Previous version used backup newfile = oldfile + '.2x.png'

    # ↓ Reading image as list
    X, Y, Z, maxcolors, image3d, info = png2list(oldfile)

    # ↓ Choosing working scaler from the list of imported scalers
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

    # ↓ Scaling using scaler chosen above
    scaled_image = chosen_scaler(image3d)

    # ↓ Fixing resolution to match original print size.
    #   If no pHYs found in original, 96 ppi is assumed as original value.
    if 'physical' in info:
        res = info['physical']  # Reading resolution as tuple
        x_pixels_per_unit = res[0]
        y_pixels_per_unit = res[1]
        unit_is_meter = res[2]
    else:
        x_pixels_per_unit = y_pixels_per_unit = 3780
        # 3780 px/meter = 96 px/inch, 2834 px/meter = 72 px/inch
        unit_is_meter = True

    x_pixels_per_unit = size * x_pixels_per_unit  # Change resolution to keep print size
    y_pixels_per_unit = size * y_pixels_per_unit  # Change resolution to keep print size

    info['physical'] = [x_pixels_per_unit, y_pixels_per_unit, unit_is_meter]
    # ↑ Resolution changed

    # ↓ Explicitly setting compression for batch processing
    info['compression'] = compression

    # ↓ Writing PNG file
    list2png(newfile, scaled_image, info)
    return None


def scale_file_pnm(runningfilename, size, sfx, bin):
    """Function upscales one PNM file and keeps quite.

    Arguments:
        runningfilename: name of file to process;
        size: scale size, either 2 or 3;
        sfx: use either sfx or classic scaler version.
    """

    oldfile = str(runningfilename)
    newfile = oldfile  # Overwrite!

    # ↓ Reading image as list
    X, Y, Z, maxcolors, image3d = pnm2list(oldfile)

    # ↓ Choosing working scaler from the list of imported scalers
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

    # ↓ Scaling using scaler chosen above
    scaled_image = chosen_scaler(image3d)

    # ↓ Writing PNM file
    list2pnm(newfile, scaled_image, maxcolors, bin)
    return None


def ListDir(directory):
    """Replacement for recursive glob which does not exist in Python 3.4"""

    for root, dirs, files in os.walk(directory):
        for basename in files:
            filename = os.path.join(root, basename)
            yield filename


def FolderNx(size, sfx):
    """Multiprocessing pool to feed `scale_file_*` processes to.

    Arguments:
        size: scale size, either 2 or 3;
        sfx: use either sfx or classic scaler version.
    """

    global mru  # Remember MRU directory for old Tkinter

    UIWaiting()

    # ↓ Open source dir
    sourcedir = askdirectory(title='Open folder to rescale images', initialdir=mru)
    if sourcedir == '':
        UINormal()
        return None
    mru = sourcedir

    UIBusy()

    # ↓ Reading global prefs dict and converting some values to local vars
    #   to transmit to pool functions since pool don't digest globals.
    compression = prefs['batch_deflation']
    bin = prefs['batch_binarity']

    # ↓ Creating pool
    scalepool = Pool()

    # ↓ Feeding the pool (no pun!)
    for runningfilename in ListDir(sourcedir):
        if os.path.splitext(runningfilename)[1] == '.png':
            scalepool.apply_async(
                scale_file_png,
                args=(
                    runningfilename,
                    size,
                    sfx,
                    compression,
                ),
            )
        if os.path.splitext(runningfilename)[1] in ('.ppm', '.pgm'):
            scalepool.apply_async(
                scale_file_pnm,
                args=(
                    runningfilename,
                    size,
                    sfx,
                    bin,
                ),
            )

    # ↓ Everything fed into the pool, waiting and closing
    scalepool.close()
    scalepool.join()

    UINormal()
    return None


def IniFileLoad(event=None) -> dict:
    """Try to read scalenx.ini, if none or defective - fix it with factory settings."""

    global prefs
    # ↓ Preferences dictionary, hardcoded factory settings
    factory = {
        # ↓ some fields used for debug and possibly good for compatibility
        'program': 'ScaleNx',
        'version': __version__,
        'time': ctime(time()),
        # ↓ now necessary fields
        'batch_deflation': 3,
        'batch_binarity': True,
        'single_deflation': 9,
        'single_binarity': True,
    }
    # ↓ Checking external preference file existence,
    #   loading if one exist, otherwise writing factory settings.
    pref_path = os.path.expanduser('~') + '/scalenx.ini'
    if os.path.exists(pref_path) and os.path.isfile(pref_path):
        with open(pref_path, 'r') as pref_file:
            prefs = load(pref_file)
    else:
        prefs = factory.copy()
    # ↓ Checking keys existence, then value types, then values,
    #   loading if ok, otherwise writing factory settings.
    if (
        ('batch_deflation' not in prefs)
        or ('batch_binarity' not in prefs)
        or ('single_binarity' not in prefs)
        or ('single_deflation' not in prefs)
        or (type(prefs['batch_deflation']) is not int)
        or (type(prefs['single_deflation']) is not int)
        or (type(prefs['batch_binarity']) is not bool)
        or (type(prefs['single_binarity']) is not bool)
    ):
        prefs = factory.copy()
    if prefs['batch_deflation'] not in range(10):
        prefs['batch_deflation'] = 3
    if prefs['single_deflation'] not in range(10):
        prefs['single_deflation'] = 9
    info_string.config(text='Batch comp:{} bin:{}; Single comp:{} bin:{} loaded'.format(prefs['batch_deflation'], prefs['batch_binarity'], prefs['single_deflation'], prefs['single_binarity']))
    info_string.bind('<Leave>', lambda event=None: info_string.config(text=info_normal['txt']))
    info_string.focus_set()
    return None


def IniFileSave(event=None) -> None:
    """Dump preferences as json"""

    global prefs
    prefs['time'] = ctime(time())
    pref_path = os.path.expanduser('~') + '/scalenx.ini'
    with open(pref_path, 'w') as pref_file:
        dump(prefs, pref_file, sort_keys=False, indent=4)
    info_string.config(text='Saved preferences as {}'.format(pref_path))
    sortir.clipboard_clear()
    sortir.clipboard_append(os.path.dirname(pref_path))
    info_string.focus_set()
    return None


def IniFileDel(event=None) -> None:
    """Delete preference file without questions"""

    pref_path = os.path.expanduser('~') + '/scalenx.ini'
    if os.path.exists(pref_path):
        os.unlink(os.path.expanduser('~') + '/scalenx.ini')
    info_string.focus_set()
    return None


""" ╔═══════════╗
    ║ Main body ║
    ╚═══════════╝ """
mru = ''  # For storing MRU directory

if __name__ == '__main__':
    freeze_support()  # Freezing for exe

    sortir = Tk()
    sortir.title('ScaleNx')
    sortir.minsize(560, 370)
    iconpath = os.path.dirname(__file__) + '/32.ico'
    if os.path.exists(iconpath):
        sortir.iconbitmap(iconpath)

    # ↓ Info statuses dictionaries
    info_normal = {'txt': 'ScaleNx {} at your command'.format(__version__), 'fg': 'grey', 'bg': 'light grey', 'status': 'normal'}
    info_waiting = {'txt': 'Waiting for input', 'fg': 'green', 'bg': 'light grey', 'status': 'disabled'}
    info_busy = {'txt': 'BUSY, PLEASE WAIT', 'fg': 'red', 'bg': 'yellow', 'status': 'disabled'}

    # ↓ Widgets
    butt99 = Button(sortir, text='Exit', font=('helvetica', 14), cursor='hand2', justify='center', state='normal', command=DisMiss)
    butt99.pack(side='bottom', padx=4, pady=2, fill='both')

    info_string = Label(sortir, text=info_normal['txt'], font=('courier', 10), foreground=info_normal['fg'], background=info_normal['bg'], relief='groove', state=info_normal['status'])
    info_string.pack(side='bottom', padx=2, pady=(6, 1), fill='both')

    # ↓ Info string binding
    info_string.bind('<Enter>', lambda event=None: info_string.config(text='Prefs reload: Alt+Click, save: Ctrl+Click, delete: Ctrl+Alt+Click'))
    info_string.bind('<Leave>', lambda event=None: UINormal)
    info_string.bind('<Alt-Button-1>', IniFileLoad)
    info_string.bind('<Control-Button-1>', IniFileSave)
    info_string.bind('<Control-Alt-Button-1>', IniFileDel)

    frame_left = Frame(sortir, borderwidth=2, relief='groove')
    frame_left.pack(side='left', anchor='nw', padx=(2, 6), pady=0)

    frame_right = Frame(sortir, borderwidth=2, relief='groove')
    frame_right.pack(side='right', anchor='ne', padx=(6, 2), pady=0)

    label00 = Label(frame_left, text='ScaleNx', font=('helvetica', 24), justify='center', borderwidth=2, relief='groove', foreground='brown', background='light grey')
    label00.pack(side='top', pady=(0, 6), fill='both')

    label01 = Label(frame_left, text='Single image rescaling (PNG, PPM, PGM)'.center(42, ' '), font=('helvetica', 10), justify='center', borderwidth=2, relief='flat', foreground='dark blue')
    label01.pack(side='top', pady=(12, 0))

    butt01 = Button(frame_left, text='Open file => 2x', font=('helvetica', 14), cursor='hand2', justify='center', state='normal', command=lambda: FileNx(2, False))
    butt01.pack(side='top', padx=4, pady=2, fill='both')

    butt02 = Button(frame_left, text='Open file => 3x', font=('helvetica', 14), cursor='hand2', justify='center', state='normal', command=lambda: FileNx(3, False))
    butt02.pack(side='top', padx=4, pady=2, fill='both')

    label02 = Label(frame_left, text='Folder batch process (PNG, PPM, PGM)', font=('helvetica', 10), justify='center', borderwidth=2, relief='flat', foreground='dark blue')
    label02.pack(side='top', pady=(12, 0))

    butt03 = Button(frame_left, text='Select folder => 2x', font=('helvetica', 14), cursor='hand2', justify='center', state='normal', command=lambda: FolderNx(2, False))
    butt03.pack(side='top', padx=4, pady=2, fill='both')

    butt04 = Button(frame_left, text='Select folder => 3x', font=('helvetica', 14), cursor='hand2', justify='center', state='normal', command=lambda: FolderNx(3, False))
    butt04.pack(side='top', padx=4, pady=2, fill='both')

    label10 = Label(frame_right, text='ScaleNxSFX', font=('helvetica', 24), justify='center', borderwidth=2, relief='groove', foreground='brown', background='light grey')
    label10.pack(side='top', pady=(0, 6), fill='both')

    label11 = Label(frame_right, text='Single image rescaling (PNG, PPM, PGM)'.center(42, ' '), font=('helvetica', 10), justify='center', borderwidth=2, relief='flat', foreground='dark blue')
    label11.pack(side='top', pady=(12, 0))

    butt11 = Button(frame_right, text='Open file => 2xSFX', font=('helvetica', 14), cursor='hand2', justify='center', command=lambda: FileNx(2, True))
    butt11.pack(side='top', padx=4, pady=2, fill='both')

    butt12 = Button(frame_right, text='Open file => 3xSFX', font=('helvetica', 14), cursor='hand2', justify='center', state='normal', command=lambda: FileNx(3, True))
    butt12.pack(side='top', padx=4, pady=2, fill='both')

    label12 = Label(frame_right, text='Folder batch process (PNG, PPM, PGM)', font=('helvetica', 10), justify='center', borderwidth=2, relief='flat', foreground='dark blue')
    label12.pack(side='top', pady=(12, 0))

    butt13 = Button(frame_right, text='Select folder => 2xSFX', font=('helvetica', 14), cursor='hand2', justify='center', state='normal', command=lambda: FolderNx(2, True))
    butt13.pack(side='top', padx=4, pady=2, fill='both')

    butt14 = Button(frame_right, text='Select folder => 3xSFX', font=('helvetica', 14), cursor='hand2', justify='center', state='normal', command=lambda: FolderNx(3, True))
    butt14.pack(side='top', padx=4, pady=2, fill='both')

    sortir.bind_all('<Control-q>', DisMiss)  # Ctrl+Q exit I used to use

    # ↓ Loading file formats prefs
    IniFileLoad()
    info_string.config(text=info_normal['txt'])

    # ↓ Center window horizontally, one third vertically
    sortir.update()
    sortir.geometry('+{x_position:d}+{y_position:d}'.format(x_position=(sortir.winfo_screenwidth() - sortir.winfo_width()) // 2, y_position=(sortir.winfo_screenheight() - sortir.winfo_height()) // 3))

    sortir.mainloop()
