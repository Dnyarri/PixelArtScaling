# Batch processing a directory to rescale all PNG files using
# Scale3x aka AdvMAME3x method
# Created by Ilyich the Toad (mailto: amphisoft@gmail.com)
# Versions:
# 01.000    Seem to work

from tkinter import filedialog
from glob import glob
import png  # PNG reading: PyPNG from: https://gitlab.com/drj11/pypng
import IncSrc
from IncScaleNx import Scale3x

# Open source dir
sourcedir = filedialog.askdirectory(title='Open DIR to resize PNG images')
if (sourcedir == ''):
    quit()

# Process file list
for runningfilename in glob(sourcedir + "/**/*.png", recursive=True):   # select all PNG files in all subfolders

    oldfile = runningfilename
    newfile = oldfile + '.3x.png'       # If you wish originals to be replaced, set newfile = oldfile

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
