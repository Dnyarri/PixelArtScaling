#!/usr/bin/env python3

'''
Content
--------

- IncSrc.src            - src(x,y,z) a-la FilterMeister 
- IncSrc.srcL           - srcL(x,y,z) similar to src(x,y,z) but performs bilinear interpolation 
- IncSrc.Img3D          - representation of image as 3D list (image) of lists (rows) of lists (pixels) of integers (channel values)
- IncSrc.Img3Dto1D      - conversion of .Img3D output into single row list for easy output with PyPNG writer.write_array method

Installation
--------------
Simply put module into your program folder

Usage
-------

Intended to work together with PyPNG from https://gitlab.com/drj11/pypng.
Main programs should contain something like this:

``source = png.Reader(filename = "address and name of file.png")``

``X,Y,pixels,info = source.asDirect()``

``imagedata = tuple((pixels))``

``Z = (info['planes'])``

Opening image, iDAT comes to "pixels" as bytearray, then tuple'd. 
Image should be opened as "imagedata" tuple and X, Y, Z set as int by main program.

After that you may use forementioned functions like:

``ImageAsListListList = IncSrc.Img3D(imagedata, X, Y, Z)``

(then doing something with that image, changing not only ImageAsListListList but probably X, Y, Z as well. Then)

``ResultImageAsList = IncSrc.Img3Dto1D(ImageAsListListList)``

(and then writing ResultImageAsList via PyPNG .write_array)

Copyright and redistribution
-----------------------------

Developed by Ilya Razmanov (https://dnyarri.github.io/)  
May be freely used and included anywhere by anyone who found it useful.  

Versions:
----------

2024.05.14  Complete rewriting. Image .append within for loops replaced with comprehension list generator and comprehension list reshaper.

WARNING:
----------

Img3Dto1D input format changed, only image list required. Image size variables removed from positional arguments, making this version incompatible with versions 2024.03.20 and below.

'''

__author__ = 'Ilya Razmanov'
__copyright__ = '(c) 2024 Ilya Razmanov'
__credits__ = 'Ilya Razmanov'
__license__ = 'unlicense'
__version__ = '2024.05.14'
__maintainer__ = 'Ilya Razmanov'
__email__ = 'ilyarazmanov@gmail.com'
__status__ = 'Production'

# --------------------------------------------------------------
# src function. Analog of src from FilterMeister, force repeat edge instead of going out of range, with
# NEAREST NEIGHBOUR interpolation
#

def src(imagedata, X, Y, Z, x, y, z):
    '''Image src, nearest neighbour

    imagedata is image data tuple from png.py output

    X, Y, Z - int constants for image size

    x, y, z - int coordinates to read x, y pixel, z channel value at

    '''

    cx = int(x); cy = int(y)            # Converts float input request to int.
                                        # Actually it does nearest neighbour
    cx = max(0,cx); cx = min((X-1),cx)  # Repeat edge extrapolation a-la Photoshop
    cy = max(0,cy); cy = min((Y-1),cy)  # Repeat edge extrapolation a-la Photoshop

    position = (cx*Z) + z   # Here the main magic of turning two x, z into one array position ensues
    channelvalue = int(((imagedata[cy])[position]))

    return channelvalue
#
# end of src function. Returned int channel value of coordinates x,y,z
# --------------------------------------------------------------


# --------------------------------------------------------------
# srcL function. Analog of src above, based on src above, but doing
# BILINEAR interpolation
#

def srcL(imagedata, X, Y, Z, x, y, z):
    ''' Image src, bilinear interpolation

        imagedata is image data tuple from png.py output

        X, Y, Z - int constants for image size

        x, y - float coordinates to read x, y pixel at
        
        z - int channel number

    '''

    fx = float(x); fy = float(y)        # Uses float input coordinates for interpolation
    fx = max(0,fx); fx = min((X-1),fx)  # Repeat edge extrapolation a-la Photoshop
    fy = max(0,fy); fy = min((Y-1),fy)  # Repeat edge extrapolation a-la Photoshop

    # Neighbour pixels coordinates (square corners x0,y0; x1,y0; x0,y1; x1,y1)
    x0 = int(x); x1 = x0 + 1
    y0 = int(y); y1 = y0 + 1

    # Reading corners src (see scr above) and interpolating
    channelvalue = (
        src(imagedata, X, Y, Z, x0, y0, z) * (x1 - fx) * (y1 - fy)
        + src(imagedata, X, Y, Z, x0, y1, z) * (x1 - fx) * (fy - y0)
        + src(imagedata, X, Y, Z, x1, y0, z) * (fx - x0) * (y1 - fy)
        + src(imagedata, X, Y, Z, x1, y1, z) * (fx - x0) * (fy - y0)
    )

    return int(channelvalue)
#
# end of srcL function. Returned int channel value of coordinates x,y,z
# --------------------------------------------------------------


# --------------------------------------------------------------
# Img3D function. Creating image as list (image) of lists (rows) of lists (pixels) of int (channel values)
#

def Img3D(imagedata, X, Y, Z):
    ''' ``imagedata`` is image data tuple from png.py output

        X, Y, Z - constants for image size

        Function constructs image as as list (image) of lists (rows) of lists (pixels) of int (channel values) from raw png.py output

    '''

    ImageAsListListList = [
        [
            [
                src(imagedata, X, Y, Z, x, y, z) for z in range(Z)
            ] for x in range(X)
        ] for y in range(Y)
    ]

    return ImageAsListListList
#
# end of Img3D function. Returned ImageAsListListList is 3D list of signals of coordinates x,y,z
# --------------------------------------------------------------


# --------------------------------------------------------------
# Img3Dto1D function. Takes gotImage as 3D
# list (image) of lists (rows) of lists (pixels) of int (channel values)
# and reshapes into single row list for easy output with PyPNG png.Writer writer.write_array method.
#

def Img3Dto1D(gotImage):
    ''' Takes ``gotImage`` as 3D list (image) of lists (rows) of lists (pixels) of int (channel values) 
        and reshapes into single row list of int for easy output with PyPNG ``png.Writer`` ``.write_array`` method
        
    '''

    ResultImageAsList = [
        channel
            for row in gotImage
                for px in row
                    for channel in px
    ]

    return ResultImageAsList
#
# end of Img3Dto1D function. Returned ResultImageAsList is 1D list suitable for PyPNG .write_array
# --------------------------------------------------------------


if __name__ == '__main__':
    print('Module to be imported, not run as standalone')
