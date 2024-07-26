#!/usr/bin/env python3

'''
Overview
----------

pnglpng (png-list-png) is a suitable joint between PyPNG and other Python programs, providing data conversion from/to used by PyPNG and understandable by ordinary average human.

- png2list  - reading PNG file and returning all data
- list2png  - getting data and writing PNG file

Installation
--------------
Simply put module into your main program folder

Usage
-------
After ``import pnglpng``, use something like

``image3D, X, Y, Z, maxcolors, info = pnglpng.png2list(in_filename)``

for PNG to data tuple reading, and 

``pnglpng.list2png(out_filename, image3D, info)``

for writing data to PNG.


Copyright and redistribution
-----------------------------
Written by Ilya Razmanov (https://dnyarri.github.io/) to simplify working with PyPNG module.
May be freely used and redistributed.

Prerequisites and References
-----------------------------

PyPNG download: https://gitlab.com/drj11/pypng
PyPNG docs: https://drj11.gitlab.io/pypng

Versions:  
----------

24.07.25    Initial version.

24.07.26    Fixed missing Z autodetection for "info" generation.

'''

__author__ = 'Ilya Razmanov'
__copyright__ = '(c) 2024 Ilya Razmanov'
__credits__ = 'Ilya Razmanov'
__license__ = 'unlicense'
__version__ = '24.07.26'
__maintainer__ = 'Ilya Razmanov'
__email__ = 'ilyarazmanov@gmail.com'
__status__ = 'Development'

import png  # PNG I/O: PyPNG from: https://gitlab.com/drj11/pypng

def png2list(in_filename):
    '''
    Usage:
    -------

    ``image3D, X, Y, Z, maxcolors, info = pnglpng.png2list(in_filename)``

    Takes PNG filename ``in_filename`` and returns the following tuple:
    
    ``image3D`` - Y*X*Z list (image) of lists (rows) of lists (pixels) of ints (channels), from PNG iDAT
    
    ``X, Y, Z`` - int, PNG image sizes
    
    ``maxcolors`` - int, value maximum per channel, either 255 or 65535, for 8 bpc and 16 bpc PNG respectively
    
    ``info`` - dictionary, chunks like resolution etc. as they are accessible by PyPNG
    '''

    source = png.Reader(in_filename)

    X, Y, pixels, info = source.asDirect()  # Opening image, iDAT comes to "pixels" as bytearray
    Z = info['planes']      # Channels number
    if info['bitdepth'] == 8:
        maxcolors = 255     # Maximal value for 8-bit channel
    if info['bitdepth'] == 16:
        maxcolors = 65535   # Maximal value for 16-bit channel

    imagedata = tuple((pixels))  # Creates tuple of bytes or whatever "pixels" generator returns

    # Next part forcedly creates 3D list of int out of "imagedata" tuple of hell knows what
    image3D = [
        [
            [
                int(((imagedata[y])[(x*Z) + z])) for z in range(Z)
            ] for x in range(X)
        ] for y in range(Y)
    ]
    # List (image) of lists (rows) of lists (pixels) of ints (channels) created

    return (image3D, X, Y, Z, maxcolors, info)

def list2png (out_filename, image3D, info):
    '''
    Usage:
    -------
    
    ``pnglpng.list2png(out_filename, image3D, info)``

    Takes data described below and writes PNG file ``out_filename`` out of it:

    ``image3D`` - Y*X*Z list (image) of lists (rows) of lists (pixels) of ints (channels)

    ``info`` - dictionary, chunks like resolution etc. as you want them to be present in PNG
    '''

    # Determining list sizes
    Y = len(image3D)
    X = len(image3D[0])
    Z = len(image3D[0][0])

    # Duplicate image size in header with image size in "info"
    info['size'] = (X, Y)
    info['planes'] = Z

    # flattening 3D list to 1D list for PNG .write_array method
    image1D = [
        c 
            for row in image3D
                for px in row
                    for c in px
    ]

    # Writing PNG
    resultPNG = open(out_filename, mode='wb')
    writer = png.Writer(X, Y, **info)
    writer.write_array(resultPNG, image1D)
    resultPNG.close()  # Close output

    return None

# Stub

if __name__ == '__main__':
    print('Module to be imported, not run as standalone')
