#!/usr/bin/env python3

"""
ScaleNx GUI - Common shell for ScaleNx single file and batch PNG, PPM and PGM rescaling.
---

Created by: Ilya Razmanov <ilyarazmanov@gmail.com> aka Ilyich the Toad <amphisoft@gmail.com>

History:
---

25.01.17.00 Initial GUI version for ScaleNx.

25.01.17.21 Fully operational.

25.03.01.01 PNM batch processing added. GUI simplified to reduce imports.

25.07.01.07 Compression for PNG batch processing diminished from 9 to 3 to increase batch speed.

25.08.27.10 PNG compression and PNM format prefs may be saved/loaded to/from file.
Prefs OptionMenu added to GUI.

---
Main site: <https://dnyarri.github.io>

Source at Github: <https://github.com/Dnyarri/PixelArtScaling>

"""

__author__ = 'Ilya Razmanov'
__copyright__ = '(c) 2025 Ilya Razmanov'
__credits__ = 'Ilya Razmanov'
__license__ = 'unlicense'
__version__ = '25.08.27.10'
__maintainer__ = 'Ilya Razmanov'
__email__ = 'ilyarazmanov@gmail.com'
__status__ = 'Production'

from json import dump, load
from multiprocessing import Pool, freeze_support
from pathlib import Path
from time import ctime, time
from tkinter import Button, Frame, Label, LabelFrame, OptionMenu, PhotoImage, StringVar, Tk
from tkinter.filedialog import askdirectory, askopenfilename, asksaveasfilename

from pypng.pnglpng import list2png, png2list
from pypnm.pnmlpnm import list2pnm, pnm2list
from scalenx import scalenx, scalenxsfx


def DisMiss(event=None) -> None:
    """Kill dialog and continue"""

    sortir.destroy()
    return None


def UINormal() -> None:
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


def UIWaiting() -> None:
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


def UIBusy() -> None:
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


def FileNx(size: int, sfx: bool) -> None:
    """Single file ScaleNx with variable N and method.

    Arguments:
        size: scale size, either 2 or 3;
        sfx: use either sfx or classic scaler version.

    """

    UIWaiting()
    # ↓ Getting prefs from UI
    FormatPrefs()
    # ↓ Open source file
    sourcefilename = askopenfilename(title='Open image file to rescale', filetypes=[('Supported formats', '.png .ppm .pgm .pbm'), ('Portable network graphics', '.png'), ('Portable network map', '.ppm .pgm .pbm')])
    if sourcefilename == '':
        UINormal()
        return None

    UIBusy()

    if Path(sourcefilename).suffix == '.png':
        # ↓ Reading image as list
        X, Y, Z, maxcolors, image3d, info = png2list(sourcefilename)

    elif Path(sourcefilename).suffix in ('.ppm', '.pgm', '.pbm'):
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
        filetypes=format,
        defaultextension='.png',  # No extension should never happen but just in case
    )
    if resultfilename == '':
        UINormal()
        return None

    UIBusy()

    if Path(resultfilename).suffix == '.png':
        list2png(resultfilename, scaled_image, info)
    elif Path(resultfilename).suffix in ('.ppm', '.pgm'):
        list2pnm(resultfilename, scaled_image, maxcolors, bin=prefs['single_binarity'])

    UINormal()
    return None


def scale_file_png(runningfilename: Path, size: int, sfx: bool, compression: int = 3) -> None:
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


def scale_file_pnm(runningfilename: Path, size: int, sfx: bool, bin: bool = True) -> None:
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


def FolderNx(size: int, sfx: bool) -> None:
    """Multiprocessing pool to feed `scale_file_*` processes to.

    Arguments:
        size: scale size, either 2 or 3;
        sfx: use either sfx or classic scaler version.

    """

    UIWaiting()
    # ↓ Getting prefs from UI
    FormatPrefs()
    # ↓ Open source dir
    sourcedir = askdirectory(title='Open folder to rescale images')
    if sourcedir == '':
        UINormal()
        return None

    path = Path(sourcedir)

    UIBusy()

    # ↓ Reading global prefs dict and converting some values to local vars
    #   to transmit to pool functions since pool don't digest globals.
    compression = prefs['batch_deflation']
    bin = prefs['batch_binarity']

    # ↓ Creating pool
    scalepool = Pool()

    # ↓ Feeding the pool (no pun!)
    for runningfilename in path.rglob('*.*'):
        if runningfilename.suffix == '.png':
            scalepool.apply_async(
                scale_file_png,
                args=(
                    runningfilename,
                    size,
                    sfx,
                    compression,
                ),
            )
        if runningfilename.suffix in ('.ppm', '.pgm'):
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
    pref_path = Path.home() / 'scalenx.ini'
    if pref_path.exists() and pref_path.is_file:
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
    # ↓ Feeding values to UI
    png_single.set(str(prefs['single_deflation']))
    pnm_single.set('bin' if prefs['single_binarity'] else 'ascii')
    png_batch.set(str(prefs['batch_deflation']))
    pnm_batch.set('bin' if prefs['batch_binarity'] else 'ascii')
    # ↓ Changing status
    info_string.config(text=f'Batch comp:{prefs["batch_deflation"]} bin:{prefs["batch_binarity"]}; Single comp:{prefs["single_deflation"]} bin:{prefs["single_binarity"]} loaded')
    info_string.focus_set()
    sortir.update()
    return None


def IniFileSave(event=None) -> None:
    """Dump preferences as json.

    Saves current file saving preferences to `scalenx.ini` file in User directory.
    User directory is chosen to provide compiling to exe
    since User directory is not related to file location.

    """

    global prefs
    FormatPrefs()
    prefs['time'] = ctime(time())
    pref_path = Path.home() / 'scalenx.ini'
    with open(pref_path, 'w') as pref_file:
        dump(prefs, pref_file, sort_keys=False, indent=4)
    info_string.config(text=f'Saved preferences as {pref_path}')
    sortir.clipboard_clear()
    sortir.clipboard_append(str(pref_path.parent))
    info_string.focus_set()
    return None


def FormatPrefs() -> None:
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
    sortir.minsize(602, 448)

    # ↓ ICO icon.
    #   Tkinter seem to read number 0 one and interpolate.
    # iconpath = Path(__file__).resolve().parent / '32.ico'
    # if iconpath.exists():
    #    sortir.iconbitmap(str(iconpath))

    # ↓ PNG icon.
    #   Requires PhotoImage which makes exe bigger
    #   but result looks sharper on screen.
    iconpath_32 = Path(__file__).resolve().parent / '32.png'
    iconpath_16 = Path(__file__).resolve().parent / '16.png'
    if iconpath_32.exists() and iconpath_16.exists():
        sortir.iconphoto(True, PhotoImage(file=iconpath_32), PhotoImage(file=iconpath_16))

    # ↓ Info statuses dictionaries
    info_normal = {
        'txt': f'ScaleNx ver. {__version__} at your command',
        'font': ('courier', 10),
        'fg': 'grey',
        'bg': 'light grey',
        'status': 'normal',
    }
    info_waiting = {
        'txt': 'Waiting for input',
        'font': ('courier', 10),
        'fg': 'green',
        'bg': 'light grey',
        'status': 'disabled',
    }
    info_busy = {
        'txt': 'BUSY, PLEASE WAIT',
        'font': ('courier', 10),
        'fg': 'red',
        'bg': 'yellow',
        'status': 'disabled',
    }

    # ↓ Frequently used formatting
    blue = {
        'pady': (12, 0),
        'center': 48,
        'font': ('helvetica', 10),
        'foreground': 'dark blue',
        'background': 'light blue',
    }
    butt = {
        'font': ('helvetica', 14),
        'cursor': 'hand2',
    }

    # ↓ Widgets
    butt99 = Button(sortir, text='Exit', font=butt['font'], cursor=butt['cursor'], state='normal', command=DisMiss)
    butt99.pack(side='bottom', padx=4, pady=2, fill='both')

    info_string = Label(sortir, text=info_normal['txt'], font=info_normal['font'], foreground=info_normal['fg'], background=info_normal['bg'], relief='groove', state=info_normal['status'])
    info_string.pack(side='bottom', padx=2, pady=(6, 1), fill='both')

    # ↓ Info string binding
    info_string.bind('<Enter>', lambda event=None: info_string.config(text='Prefs save: Ctrl+Click, reload: Alt+Click, delete: Ctrl+Alt+Click', font=('courier', 10)))
    info_string.bind('<Leave>', lambda event=None: UINormal())
    info_string.bind('<Alt-Button-1>', IniFileLoad)
    info_string.bind('<Control-Button-1>', IniFileSave)  # Path.home() / 'scalenx.ini'
    info_string.bind('<Control-Alt-Button-1>', lambda event=None: (Path.home() / 'scalenx.ini').unlink(missing_ok=True))

    # ↓ Main UI frames
    frame_left = Frame(sortir, borderwidth=2, relief='groove')
    frame_left.pack(side='left', anchor='nw', padx=(2, 6), pady=0)

    frame_right = Frame(sortir, borderwidth=2, relief='groove')
    frame_right.pack(side='right', anchor='ne', padx=(6, 2), pady=0)

    # ↓ Left frame
    label00 = Label(frame_left, text='Single file rescaling', wraplength=200, font=('helvetica', 24), justify='right', borderwidth=2, relief='groove', foreground='brown', background='light grey')
    label00.pack(side='top', anchor='e', padx=0, pady=(0, 6), fill='both')

    label01 = Label(frame_left, text='ScaleNx'.center(blue['center'], ' '), font=blue['font'], borderwidth=2, relief='flat', foreground=blue['foreground'], background=blue['background'])
    label01.pack(side='top', pady=blue['pady'], fill='both')

    butt01 = Button(frame_left, text='Open file ➔ 2x', font=butt['font'], cursor=butt['cursor'], state='normal', command=lambda: FileNx(2, False))
    butt01.pack(side='top', padx=4, pady=2, fill='both')

    butt02 = Button(frame_left, text='Open file ➔ 3x', font=butt['font'], cursor=butt['cursor'], state='normal', command=lambda: FileNx(3, False))
    butt02.pack(side='top', padx=4, pady=2, fill='both')

    label11 = Label(frame_left, text='ScaleNxSFX', font=blue['font'], borderwidth=2, relief='flat', foreground=blue['foreground'], background=blue['background'])
    label11.pack(side='top', pady=blue['pady'], fill='both')

    butt11 = Button(frame_left, text='Open file ➔ 2xSFX', font=butt['font'], cursor=butt['cursor'], command=lambda: FileNx(2, True))
    butt11.pack(side='top', padx=4, pady=2, fill='both')

    butt12 = Button(frame_left, text='Open file ➔ 3xSFX', font=butt['font'], cursor=butt['cursor'], state='normal', command=lambda: FileNx(3, True))
    butt12.pack(side='top', padx=4, pady=2, fill='both')

    # ↓ Right frame
    label10 = Label(frame_right, text='Batch folder processing', wraplength=200, font=('helvetica', 24), justify='left', borderwidth=2, relief='groove', foreground='brown', background='light grey')
    label10.pack(side='top', anchor='w', padx=0, pady=(0, 6), fill='both')

    label12 = Label(frame_right, text='ScaleNx'.center(blue['center'], ' '), font=blue['font'], borderwidth=2, relief='flat', foreground=blue['foreground'], background=blue['background'])
    label12.pack(side='top', pady=blue['pady'], fill='both')

    butt03 = Button(frame_right, text='Select folder ➔ 2x', font=butt['font'], cursor=butt['cursor'], state='normal', command=lambda: FolderNx(2, False))
    butt03.pack(side='top', padx=4, pady=2, fill='both')

    butt04 = Button(frame_right, text='Select folder ➔ 3x', font=butt['font'], cursor=butt['cursor'], state='normal', command=lambda: FolderNx(3, False))
    butt04.pack(side='top', padx=4, pady=2, fill='both')

    label02 = Label(frame_right, text='ScaleNxSFX', font=blue['font'], borderwidth=2, relief='flat', foreground=blue['foreground'], background=blue['background'])
    label02.pack(side='top', pady=blue['pady'], fill='both')

    butt13 = Button(frame_right, text='Select folder ➔ 2xSFX', font=butt['font'], cursor=butt['cursor'], state='normal', command=lambda: FolderNx(2, True))
    butt13.pack(side='top', padx=4, pady=2, fill='both')

    butt14 = Button(frame_right, text='Select folder ➔ 3xSFX', font=butt['font'], cursor=butt['cursor'], state='normal', command=lambda: FolderNx(3, True))
    butt14.pack(side='top', padx=4, pady=2, fill='both')

    # ↓ Left frame file output options
    options_left = LabelFrame(frame_left, text='Single file saving options', font=('helvetica', 8))
    options_left.pack(side='top', anchor='ne', fill='x')

    options_left_png_label = Label(options_left, text='PNG Compression:', font=('helvetica', 8))
    options_left_png_label.pack(side='left', anchor='w')
    png_single = StringVar(value=9)
    options_left_png = OptionMenu(
        options_left,
        png_single,
        *['0', '1', '2', '3', '4', '5', '6', '7', '8', '9'],
    )
    options_left_png.pack(side='left', anchor='w')
    options_left_png.configure(font=('courier', 8), width=1)

    options_left_pnm_label = Label(options_left, text='PNM Type:', font=('helvetica', 8))
    options_left_pnm_label.pack(side='left', anchor='e')
    pnm_single = StringVar(value='bin')
    options_left_pnm = OptionMenu(
        options_left,
        pnm_single,
        *['bin', 'ascii'],
    )
    options_left_pnm.pack(side='right', anchor='e')
    options_left_pnm.configure(font=('courier', 8), width=5)

    # ↓ Right frame file output options
    options_right = LabelFrame(frame_right, text='Batch file saving options', font=('helvetica', 8))
    options_right.pack(side='top', anchor='ne', fill='x')

    options_right_png_label = Label(options_right, text='PNG Compression:', font=('helvetica', 8))
    options_right_png_label.pack(side='left', anchor='w')
    png_batch = StringVar(value=3)
    options_right_png = OptionMenu(
        options_right,
        png_batch,
        *['0', '1', '2', '3', '4', '5', '6', '7', '8', '9'],
    )
    options_right_png.pack(side='left', anchor='w')
    options_right_png.configure(font=('courier', 8), width=1)

    options_right_pnm_label = Label(options_right, text='PNM Type:', font=('helvetica', 8))
    options_right_pnm_label.pack(side='left', anchor='e')
    pnm_batch = StringVar(value='bin')
    options_right_pnm = OptionMenu(
        options_right,
        pnm_batch,
        *['bin', 'ascii'],
    )
    options_right_pnm.pack(side='right', anchor='e')
    options_right_pnm.configure(font=('courier', 8), width=5)

    # ↓ Loading file formats prefs from ini file to dict
    IniFileLoad()
    info_string.config(text=info_normal['txt'])

    # ↓ Pushing prefs from UI to dict
    FormatPrefs()

    sortir.bind_all('<Control-q>', DisMiss)

    # ↓ Center window horizontally, one third vertically
    sortir.update()
    sortir.geometry(f'+{(sortir.winfo_screenwidth() - sortir.winfo_width()) // 2}+{(sortir.winfo_screenheight() - sortir.winfo_height()) // 3}')

    sortir.mainloop()  # That's the end, little girl la-la-la
