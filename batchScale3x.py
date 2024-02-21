# Batch processing a directory to rescale all PNG files using
# Scale3x aka AdvMAME3x method
# Created by Ilyich the Toad (mailto: amphisoft@gmail.com)
# Versions:
# 01.000    Seem to work 
# 01.001    Progress indication added, showing name of file being processed 

from tkinter import Tk
from tkinter import Label
from tkinter import filedialog

from glob import glob

import png                      # PNG reading: PyPNG from: https://gitlab.com/drj11/pypng
import IncSrc                   # Image reshaping from: https://github.com/Dnyarri/PixelArtScaling
from IncScaleNx import Scale3x  # Scale2x and Scale3x from: https://github.com/Dnyarri/PixelArtScaling

# --------------------------------------------------------------
# Creating dialog

sortir = Tk()
sortir.title('Processing Scale3x...')
zanyato = Label(sortir, text = 'Starting...', font=("arial", 12), padx=16, pady=10, justify='center')
zanyato.pack()
sortir.withdraw()

# Main dialog created and hidden
# --------------------------------------------------------------

# Open source dir
sourcedir = filedialog.askdirectory(title='Open DIR to resize PNG images')
if (sourcedir == ''):
    quit()

# --------------------------------------------------------------
# Updating dialog

sortir.deiconify()
zanyato.config(text = 'Allons-y!')
sortir.update()
sortir.update_idletasks()

# Dialog shown and updated
# --------------------------------------------------------------

# Process file list
for runningfilename in glob(sourcedir + "/**/*.png", recursive=True):   # select all PNG files in all subfolders

    oldfile = runningfilename
    newfile = oldfile + '.3x.png'       # If you wish originals to be replaced, set newfile = oldfile

    zanyato.config(text = oldfile)      # Updating label, showing processed file name
    sortir.update()
    sortir.update_idletasks()

    source = png.Reader(filename = oldfile)
    X,Y,pixels,info = source.asDirect() # Opening image, iDAT comes to "pixels" as bytearray, to be tuple'd lated.
    Z = (info['planes'])                # PyPNG returns X,Y directly, but not Z. Z should be extracted from info
    imagedata = tuple((pixels))         # Attempt to fix all bytearrays as something solid


    # Reading image as list
    ImageAsListListList = IncSrc.Img3D(imagedata, X, Y, Z)

    # Scaling list to 3x image list
    EPXImage,newX,newY = Scale3x(ImageAsListListList, X, Y)

    # Reshaping 3x scaled 3D list into 1D list for PyPNG .write_array method
    ResultImageAsList = IncSrc.Img3Dto1D(EPXImage, newX, newY, Z)

    # Writing new image
    resultPNG = open(newfile, mode='wb')
    writer = png.Writer(newX, newY, greyscale = info['greyscale'], alpha = info['alpha'], bitdepth = info['bitdepth'])
    writer.write_array(resultPNG, ResultImageAsList)
    resultPNG.close()

# --------------------------------------------------------------
# Destroying dialog

sortir.destroy()
sortir.mainloop()

# Dialog destroyed and closed
# --------------------------------------------------------------
