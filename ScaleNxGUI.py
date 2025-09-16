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

25.08.27.34 Intentionally downgraded from `pathlib` to `os`.
PNG compression and PNM format prefs may be saved/loaded to/from file.
Prefs OptionMenu added to GUI.

---
Main site:  <https://dnyarri.github.io>

Project at Github:  <https://github.com/Dnyarri/PixelArtScaling>

"""

__author__ = 'Ilya Razmanov'
__copyright__ = '(c) 2025 Ilya Razmanov'
__credits__ = 'Ilya Razmanov'
__license__ = 'unlicense'
__version__ = '25.09.16.34'
__maintainer__ = 'Ilya Razmanov'
__email__ = 'ilyarazmanov@gmail.com'
__status__ = 'Production'

import os
from json import dump, load
from multiprocessing import Pool, freeze_support
from time import ctime, time
from tkinter import Button, Frame, Label, LabelFrame, OptionMenu, StringVar, Tk
from tkinter.filedialog import askdirectory, askopenfilename, asksaveasfilename

from pypng.pnglpng import list2png, png2list
from pypnm.pnmlpnm import list2pnm, pnm2list
from scalenx import scalenx, scalenxsfx


def DisMiss(event=None):
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
    info_string.config(text=info_normal['txt'], font=info_normal['font'], foreground=info_normal['fg'], background=info_normal['bg'], state=info_normal['status'])
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
    info_string.config(text=info_waiting['txt'], font=info_waiting['font'], foreground=info_waiting['fg'], background=info_waiting['bg'], state=info_waiting['status'], disabledforeground=info_waiting['fg'])
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
    info_string.config(text=info_busy['txt'], font=info_busy['font'], foreground=info_busy['fg'], background=info_busy['bg'], state=info_busy['status'], disabledforeground=info_busy['fg'])
    sortir.update()
    return None


def FileNx(size, sfx):
    """Single file ScaleNx with variable N and method.

    Arguments:
        size: scale size, either 2 or 3;
        sfx: use either sfx or classic scaler version.
    """

    global prefs  # Remember MRU directory for old Tkinter

    UIWaiting()
    # ↓ Getting prefs from UI
    FormatPrefs()
    # ↓ Open source file
    sourcefilename = askopenfilename(title='Open image file to rescale', initialdir=prefs['mru'], filetypes=[('Supported formats', '.png .ppm .pgm .pbm'), ('Portable network graphics', '.png'), ('Portable network map', '.ppm .pgm .pbm')])
    if sourcefilename == '':
        UINormal()
        return None
    prefs['mru'] = os.path.dirname(sourcefilename)
    UIBusy()

    if os.path.splitext(sourcefilename)[1] == '.png':
        # ↓ Reading image as list
        X, Y, Z, maxcolors, image3d, info = png2list(sourcefilename)

    elif os.path.splitext(sourcefilename)[1] in ('.ppm', '.pgm', '.pbm'):
        # ↓ Reading image as list
        X, Y, Z, maxcolors, image3d = pnm2list(sourcefilename)
        # ↓ Creating dummy info for PyPNG
        info = {}
        # ↓ Fixing color mode. The rest is fixed with pnglpng since ver. 25.01.07.
        info['bitdepth'] = 16 if maxcolors > 255 else 8

    else:
        raise ValueError('Extension not recognized')

    # ↓ Choosing working chosen_scaler from the list of imported scalers
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

    # ↓ Scaling image using chosen_scaler chosen above
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
        initialdir=prefs['mru'],
        filetypes=format,
        defaultextension='.png',  # No extension should never happen but just in case
    )
    if resultfilename == '':
        UINormal()
        return None

    UIBusy()

    if os.path.splitext(resultfilename)[1] == '.png':
        list2png(resultfilename, scaled_image, info)
    elif os.path.splitext(resultfilename)[1] in ('.ppm', '.pgm'):
        list2pnm(resultfilename, scaled_image, maxcolors, bin=prefs['single_binarity'])

    UINormal()
    return None


def scale_file_png(runningfilename, size, sfx, compression):
    """Function upscales one PNG file and keeps quite.

    Arguments:
        runningfilename: name of file to process;
        size: scale size, either 2 or 3;
        sfx: use either sfx or classic scaler version;
        compression: zlib deflate setting.

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
        sfx: use either sfx or classic scaler version;
        bin: whether write binary PNM or ASCII.

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

    global prefs  # Remember MRU directory for old Tkinter

    UIWaiting()
    # ↓ Getting prefs from UI
    FormatPrefs()
    # ↓ Open source dir
    sourcedir = askdirectory(title='Open folder to rescale images', initialdir=prefs['mru'])
    if sourcedir == '':
        UINormal()
        return None
    prefs['mru'] = sourcedir

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


def IniFileLoad(event=None):
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
        'mru': '{}'.format(os.path.dirname(__file__)),
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
    if 'mru' in prefs and (type(prefs['mru']) is str):
        if os.path.exists(prefs['mru']) and os.path.isdir(prefs['mru']):
            mru = prefs['mru']
        elif os.path.exists(os.path.dirname(prefs['mru'])):
            mru = os.path.dirname(prefs['mru'])
        else:
            mru = '{}'.format(os.path.dirname(__file__))
        prefs['mru'] = mru
    else:
        prefs['mru'] = '{}'.format(os.path.dirname(__file__))

    # ↓ Feeding values to UI
    png_single.set(str(prefs['single_deflation']))
    pnm_single.set('bin' if prefs['single_binarity'] else 'ascii')
    png_batch.set(str(prefs['batch_deflation']))
    pnm_batch.set('bin' if prefs['batch_binarity'] else 'ascii')
    # ↓ Changing status
    info_string.config(text='Batch comp:{} bin:{}; Single comp:{} bin:{} loaded'.format(prefs['batch_deflation'], prefs['batch_binarity'], prefs['single_deflation'], prefs['single_binarity']))
    info_string.focus_set()
    sortir.update()
    return None


def IniFileSave(event=None):
    """Dump preferences as json.

    Saves current file saving preferences to `scalenx.ini` file in User directory.
    User directory is chosen to provide compiling to exe
    since User directory is not related to file location.

    """

    global prefs
    FormatPrefs()
    prefs['time'] = ctime(time())
    pref_path = os.path.expanduser('~') + '/scalenx.ini'
    with open(pref_path, 'w') as pref_file:
        dump(prefs, pref_file, sort_keys=False, indent=4)
    info_string.config(text='Saved preferences as {}'.format(pref_path))
    sortir.clipboard_clear()
    sortir.clipboard_append(os.path.dirname(pref_path))
    info_string.focus_set()
    return None


def IniFileDel(event=None):
    """Delete preference file without questions"""

    pref_path = os.path.expanduser('~') + '/scalenx.ini'
    if os.path.exists(pref_path):
        os.unlink(pref_path)
        info_string.config(text='File {} deleted'.format(pref_path))
    else:
        info_string.config(text='File {} not found'.format(pref_path))
    info_string.focus_set()
    return None


def FormatPrefs():
    """Reading file output settings from UI and pushing it into global prefs dict"""

    prefs['single_deflation'] = int(png_single.get())
    prefs['single_binarity'] = False if pnm_single.get() == 'ascii' else True
    prefs['batch_deflation'] = int(png_batch.get())
    prefs['batch_binarity'] = False if pnm_batch.get() == 'ascii' else True
    return None


""" ╔═══════════╗
    ║ Main body ║
    ╚═══════════╝ """

if __name__ == '__main__':
    freeze_support()  # Freezing for exe

    sortir = Tk()
    sortir.title('ScaleNx')
    sortir.minsize(602, 440)

    icon_path = os.path.dirname(os.path.realpath(__file__)) + '/32.ico'
    if os.path.exists(icon_path):
        sortir.iconbitmap(icon_path)

    # ↓ Info statuses dictionaries
    info_normal = {'txt': 'ScaleNx ver. {} at your command'.format(__version__), 'font': ('courier', 10), 'fg': 'grey', 'bg': 'light grey', 'status': 'normal'}
    info_waiting = {'txt': 'Waiting for input', 'font': ('courier', 10), 'fg': 'green', 'bg': 'light grey', 'status': 'disabled'}
    info_busy = {'txt': 'BUSY, PLEASE WAIT', 'font': ('courier', 10), 'fg': 'red', 'bg': 'yellow', 'status': 'disabled'}

    # ↓ Frequently used formatting
    blue = {
        'pady': (12, 0),
        'center': 48,
        'font': ('helvetica', 10),
        'foreground': 'dark blue',
        'background': 'light blue',
    }
    butt = {
        'font': ('helvetica', 16),
        'cursor': 'hand2',
        'border': '2',
        'relief': 'groove',
        'overrelief': 'ridge',
        'foreground': 'SystemButtonText',
        'background': 'SystemButtonFace',
        'activeforeground': 'dark blue',
        'activebackground': '#E5F1FB',
    }

    # ↓ Widgets
    butt99 = Button(sortir, text='Exit', font=(butt['font'][0], butt['font'][1] + 2), cursor=butt['cursor'], state='normal', border=butt['border'], relief=butt['relief'], overrelief=butt['overrelief'], command=DisMiss)
    butt99.pack(side='bottom', padx=2, pady=(4, 2), fill='both')
    butt99.bind('<Enter>', lambda event=None: butt99.config(foreground=butt['activeforeground'], background=butt['activebackground']))
    butt99.bind('<Leave>', lambda event=None: butt99.config(foreground=butt['foreground'], background=butt['background']))

    info_string = Label(sortir, text=info_normal['txt'], font=info_normal['font'], foreground=info_normal['fg'], background=info_normal['bg'], relief='groove', state=info_normal['status'])
    info_string.pack(side='bottom', padx=2, pady=(6, 1), fill='both')

    # ↓ Info string binding
    info_string.bind('<Enter>', lambda event=None: info_string.config(text='Options save: Ctrl+Click, reload: Alt+Click, delete: Ctrl+Alt+Click', font=('courier', 10)))
    info_string.bind('<Leave>', lambda event=None: UINormal())
    info_string.bind('<Alt-Button-1>', IniFileLoad)
    info_string.bind('<Control-Button-1>', IniFileSave)
    info_string.bind('<Control-Alt-Button-1>', IniFileDel)

    # ↓ Main UI frames
    frame_left = Frame(sortir, borderwidth=2, relief='groove')
    frame_left.pack(side='left', anchor='nw', padx=(2, 6), pady=0)

    frame_right = Frame(sortir, borderwidth=2, relief='groove')
    frame_right.pack(side='right', anchor='ne', padx=(6, 2), pady=0)

    # ↓ Left frame
    label00 = Label(frame_left, text='Single image rescaling', font=('helvetica', 18), justify='right', borderwidth=2, relief='groove', foreground='brown', background='light grey')
    label00.pack(side='top', anchor='e', padx=0, pady=(0, 6), fill='both')

    label01 = Label(frame_left, text='ScaleNx'.center(blue['center'], ' '), font=blue['font'], borderwidth=2, relief='flat', foreground=blue['foreground'], background=blue['background'])
    label01.pack(side='top', pady=blue['pady'], fill='both')

    butt01 = Button(frame_left, text='Open file -> 2x', font=butt['font'], cursor=butt['cursor'], state='normal', border=butt['border'], relief=butt['relief'], overrelief=butt['overrelief'], command=lambda: FileNx(2, False))
    butt01.pack(side='top', padx=4, pady=2, fill='both')
    butt01.bind('<Enter>', lambda event=None: butt01.config(foreground=butt['activeforeground'], background=butt['activebackground']))
    butt01.bind('<Leave>', lambda event=None: butt01.config(foreground=butt['foreground'], background=butt['background']))

    butt02 = Button(frame_left, text='Open file -> 3x', font=butt['font'], cursor=butt['cursor'], state='normal', border=butt['border'], relief=butt['relief'], overrelief=butt['overrelief'], command=lambda: FileNx(3, False))
    butt02.pack(side='top', padx=4, pady=2, fill='both')
    butt02.bind('<Enter>', lambda event=None: butt02.config(foreground=butt['activeforeground'], background=butt['activebackground']))
    butt02.bind('<Leave>', lambda event=None: butt02.config(foreground=butt['foreground'], background=butt['background']))

    label11 = Label(frame_left, text='ScaleNxSFX', font=blue['font'], borderwidth=2, relief='flat', foreground=blue['foreground'], background=blue['background'])
    label11.pack(side='top', pady=blue['pady'], fill='both')

    butt11 = Button(frame_left, text='Open file -> 2xSFX', font=butt['font'], cursor=butt['cursor'], state='normal', border=butt['border'], relief=butt['relief'], overrelief=butt['overrelief'], command=lambda: FileNx(2, True))
    butt11.pack(side='top', padx=4, pady=2, fill='both')
    butt11.bind('<Enter>', lambda event=None: butt11.config(foreground=butt['activeforeground'], background=butt['activebackground']))
    butt11.bind('<Leave>', lambda event=None: butt11.config(foreground=butt['foreground'], background=butt['background']))

    butt12 = Button(frame_left, text='Open file -> 3xSFX', font=butt['font'], cursor=butt['cursor'], state='normal', border=butt['border'], relief=butt['relief'], overrelief=butt['overrelief'], command=lambda: FileNx(3, True))
    butt12.pack(side='top', padx=4, pady=2, fill='both')
    butt12.bind('<Enter>', lambda event=None: butt12.config(foreground=butt['activeforeground'], background=butt['activebackground']))
    butt12.bind('<Leave>', lambda event=None: butt12.config(foreground=butt['foreground'], background=butt['background']))

    # ↓ Right frame
    label10 = Label(frame_right, text='Batch folder processing', font=('helvetica', 18), justify='left', borderwidth=2, relief='groove', foreground='brown', background='light grey')
    label10.pack(side='top', anchor='w', padx=0, pady=(0, 6), fill='both')

    label12 = Label(frame_right, text='ScaleNx'.center(blue['center'], ' '), font=blue['font'], borderwidth=2, relief='flat', foreground=blue['foreground'], background=blue['background'])
    label12.pack(side='top', pady=blue['pady'], fill='both')

    butt03 = Button(frame_right, text='Select folder -> 2x', font=butt['font'], cursor=butt['cursor'], state='normal', border=butt['border'], relief=butt['relief'], overrelief=butt['overrelief'], command=lambda: FolderNx(2, False))
    butt03.pack(side='top', padx=4, pady=2, fill='both')
    butt03.bind('<Enter>', lambda event=None: butt03.config(foreground=butt['activeforeground'], background=butt['activebackground']))
    butt03.bind('<Leave>', lambda event=None: butt03.config(foreground=butt['foreground'], background=butt['background']))

    butt04 = Button(frame_right, text='Select folder -> 3x', font=butt['font'], cursor=butt['cursor'], state='normal', border=butt['border'], relief=butt['relief'], overrelief=butt['overrelief'], command=lambda: FolderNx(3, False))
    butt04.pack(side='top', padx=4, pady=2, fill='both')
    butt04.bind('<Enter>', lambda event=None: butt04.config(foreground=butt['activeforeground'], background=butt['activebackground']))
    butt04.bind('<Leave>', lambda event=None: butt04.config(foreground=butt['foreground'], background=butt['background']))

    label02 = Label(frame_right, text='ScaleNxSFX', font=blue['font'], borderwidth=2, relief='flat', foreground=blue['foreground'], background=blue['background'])
    label02.pack(side='top', pady=blue['pady'], fill='both')

    butt13 = Button(frame_right, text='Select folder -> 2xSFX', font=butt['font'], cursor=butt['cursor'], state='normal', border=butt['border'], relief=butt['relief'], overrelief=butt['overrelief'], command=lambda: FolderNx(2, True))
    butt13.pack(side='top', padx=4, pady=2, fill='both')
    butt13.bind('<Enter>', lambda event=None: butt13.config(foreground=butt['activeforeground'], background=butt['activebackground']))
    butt13.bind('<Leave>', lambda event=None: butt13.config(foreground=butt['foreground'], background=butt['background']))

    butt14 = Button(frame_right, text='Select folder -> 3xSFX', font=butt['font'], cursor=butt['cursor'], state='normal', border=butt['border'], relief=butt['relief'], overrelief=butt['overrelief'], command=lambda: FolderNx(3, True))
    butt14.pack(side='top', padx=4, pady=2, fill='both')
    butt14.bind('<Enter>', lambda event=None: butt14.config(foreground=butt['activeforeground'], background=butt['activebackground']))
    butt14.bind('<Leave>', lambda event=None: butt14.config(foreground=butt['foreground'], background=butt['background']))

    # ↓ Left frame file output options
    options_left = LabelFrame(frame_left, text='Single file saving options', font=('helvetica', 8), foreground=blue['foreground'])
    options_left.pack(side='top', anchor='ne', fill='x')

    options_left_png_label = Label(options_left, text='PNG Compression:', font=('helvetica', 8))
    options_left_png_label.pack(side='left', anchor='w')

    png_single = StringVar(value=9)
    options_left_png = OptionMenu(options_left, png_single, *['0', '1', '2', '3', '4', '5', '6', '7', '8', '9'])
    options_left_png.pack(side='left', anchor='w')
    options_left_png.configure(font=('courier', 8), width=1, relief=butt['relief'], activebackground=butt['activebackground'])
    options_left_png['menu'].configure(font=options_left_png['font'])

    options_left_pnm_label = Label(options_left, text='PNM Type:', font=('helvetica', 8))
    options_left_pnm_label.pack(side='left', anchor='e')
    pnm_single = StringVar(value='bin')
    options_left_pnm = OptionMenu(options_left, pnm_single, *['bin', 'ascii'])
    options_left_pnm.pack(side='right', anchor='e')
    options_left_pnm.configure(font=('courier', 8), width=5, relief=butt['relief'], activebackground=butt['activebackground'])
    options_left_pnm['menu'].configure(font=options_left_pnm['font'])

    # ↓ Right frame file output options
    options_right = LabelFrame(frame_right, text='Batch file saving options', font=('helvetica', 8), foreground=blue['foreground'])
    options_right.pack(side='top', anchor='ne', fill='x')

    options_right_png_label = Label(options_right, text='PNG Compression:', font=('helvetica', 8))
    options_right_png_label.pack(side='left', anchor='w')

    png_batch = StringVar(value=3)
    options_right_png = OptionMenu(options_right, png_batch, *['0', '1', '2', '3', '4', '5', '6', '7', '8', '9'])
    options_right_png.pack(side='left', anchor='w')
    options_right_png.configure(font=('courier', 8), width=1, relief=butt['relief'], activebackground=butt['activebackground'])
    options_right_png['menu'].configure(font=options_right_png['font'])

    options_right_pnm_label = Label(options_right, text='PNM Type:', font=('helvetica', 8))
    options_right_pnm_label.pack(side='left', anchor='e')
    pnm_batch = StringVar(value='bin')
    options_right_pnm = OptionMenu(options_right, pnm_batch, *['bin', 'ascii'])
    options_right_pnm.pack(side='right', anchor='e')
    options_right_pnm.configure(font=('courier', 8), width=5, relief=butt['relief'], activebackground=butt['activebackground'])
    options_right_pnm['menu'].configure(font=options_right_pnm['font'])

    # ↓ Loading file formats prefs from ini file to dict
    IniFileLoad()
    info_string.config(text=info_normal['txt'])

    # ↓ Pushing prefs from UI to dict
    FormatPrefs()

    sortir.bind_all('<Control-q>', DisMiss)

    # ↓ Center window horizontally, one third vertically
    sortir.update()
    # print(sortir.winfo_width(), sortir.winfo_height())
    sortir.geometry('+{x_position:d}+{y_position:d}'.format(x_position=(sortir.winfo_screenwidth() - sortir.winfo_width()) // 2, y_position=(sortir.winfo_screenheight() - sortir.winfo_height()) // 3))

    sortir.mainloop()
