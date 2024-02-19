'''
Content
--------

- IncSrc.src            - src(x,y,z) a-la FilterMeister 
- IncSrc.Img3D          - representation of image as 3D list (image) of lists (rows) of lists (pixels) of integers (channel values)
- IncSrc.Img3Dto1D      - conversion of .Img3D output into single row list for easy output with PyPNG writer.write_array method

Usage
------

Intended to work together with PyPNG from https://gitlab.com/drj11/pypng.
Main programs should contain something like this:

``source = png.Reader(filename = "address and name of file.png")``

``X,Y,pixels,info = source.asDirect()``

``imagedata = tuple((pixels))``

``Z = (info['planes'])``

Opening image, iDAT comes to "pixels" as bytearray, then tuple'd. 
Image should be opened as "imagedata" tuple and X, Y, Z set as int by main program/

After that you may use forementioned functions like:

``ImageAsListListList = IncSrc.Img3D(imagedata, X, Y, Z)``

(then doing something with that image, changing not only ImageAsListListList but probably X, Y, Z as well. Then)

``ResultImageAsList = IncSrc.Img3Dto1D(ImageAsListListList, X, Y, Z)``

(and then writing ResultImageAsList via PyPNG .write_array)

Copyright and redistribution
-----------------------------

Deleloped by Ilya Razmanov (https://github.com/Dnyarri/)

Last modified 18.02.2024

May be freely used and included anywhere by anyone who found it useful.

'''

# --------------------------------------------------------------
# src function. Analog of src from FilterMeister, force repeate edge instead of going out of range
#

def src(imagedata, X, Y, Z, x, y, z):

    cx = int(x); cy = int(y)
    cx = max(0,cx); cx = min((X-1),cx)
    cy = max(0,cy); cy = min((Y-1),cy)

    position = (cx*Z) + z   # Here is the main magic of turning two x, z into one array position
    channelvalue = int(((imagedata[cy])[position]))
    
    return channelvalue

#
# end of src function. Returned int channel value of coordinates x,y,z
# --------------------------------------------------------------


# --------------------------------------------------------------
# Img3D function. Creating image as list (image) of lists (rows) of lists (pixels) of int (channel values)
#

def Img3D(imagedata, X, Y, Z):
    ImageAsListListList = list()
    for y in range(0, Y, 1):
        RowAsListList = list()
        for x in range(0, X, 1):
            PixelAsList = list()
            for z in range(0, Z, 1):
                signal = src(imagedata, X, Y, Z, x,y,z)
                PixelAsList.append(signal)
            RowAsListList.append(PixelAsList)
        ImageAsListListList.append(RowAsListList)
    return ImageAsListListList

#
# end of Img3D function. Returned ImageAsListListList is 3D list of signals of coordinates x,y,z
# --------------------------------------------------------------


# --------------------------------------------------------------
# Img3Dto1D function. Takes gotImage as 3D list (image) of lists (rows) of lists (pixels) of int (channel values)
# and reshapes into single row list for easy output with PyPNG png.Writer writer.write_array method.
#

def Img3Dto1D(gotImage, gotX, gotY, Z):
    
    ResultImageAsList = list()
    for y in range(0, gotY, 1):
        for x in range(0, gotX, 1):
            for z in range(0, Z, 1):
                signal = gotImage[y][x][z]
                ResultImageAsList.append(signal)
    return ResultImageAsList

#
# end of Img3Dto1D function. Returned ResultImageAsList is 1D list suitable for PyPNG .write_array
# --------------------------------------------------------------


if __name__ == "__main__":
    print('Module to be imported, not run as standalone')