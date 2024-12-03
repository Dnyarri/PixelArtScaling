#!/usr/bin/env python3

"""Functions to read PPM and PGM files to nested 3D list and write back.

Overview
----------

pnmlpnm (pnm-list-pnm) is a pack of functions for dealing with PPM and PGM image files. Functions included are:

- pnm2list  - reading binary or ascii RGB PPM or L PGM file and returning image data as ints and nested list.
- list2bin  - getting image data as ints and nested list and creating binary PPM (P6) or PGM (P5) data structure in memory. Suitable for generating data to display with Tkinter.
- list2pnm  - writing data created with list2bin to file.
- list2pnmascii - alternative function to write ASCII PPM (P3) or PGM (P2) files.
- create_image - creating empty nested 3D list for image representation. Not used within this particular module but often needed by programs this module is supposed to be used with.

Installation
--------------
Simply put module into your main program folder.

Usage
-------
After ``import pnmlpnm``, use something like

``X, Y, Z, maxcolors, image3D = pnmlpnm.pnm2list(in_filename)``

for reading data from PPM/PGM, where:

- X, Y, Z   - image sizes (int);
- maxcolors - number of colors per channel for current image (int);
- image3D   - image pixel data as list(list(list(int)));

and

``pnmlpnm.pnm = list2bin(image3D, maxcolors)``

for writing data from image3D nested list to "pnm" bytes object in memory,

or 

``pnmlpnm.list2pnm(out_filename, image3D, maxcolors)``

or

``pnmlpnm.list2pnmascii(out_filename, image3D, maxcolors)``

for writing data from image3D nested list to PPM/PGM file "out_filename".


Copyright and redistribution
-----------------------------
Written by Ilya Razmanov (https://dnyarri.github.io/) to provide working with PPM/PGM files and creating PPM data to be displayed with Tkinter "PhotoImage" class.

May be freely used and redistributed.

References
-----------------------------

Netpbm specs: https://netpbm.sourceforge.net/doc/

History:  
----------

0.11.26.0   Initial working version 26 Nov 2024.

0.11.27.3   Implemented fix for Adobe Photoshop CS6 using linebreaks in header.

0.11.28.0   Rewritten to use less arguments for output; X, Y, Z autodetected.

0.11.29.0   Added ASCII write support.

0.11.30.0   Switched to array; this allowed 16 bpc P5 and P6 files writing.

0.11.30.2   Seems like finally fixed 16 bpc P5 and P6 files reading. Looks ugly but works.

1.12.1.2   Seem to be ready for release.

"""

__author__ = 'Ilya Razmanov'
__copyright__ = '(c) 2024 Ilya Razmanov'
__credits__ = 'Ilya Razmanov'
__license__ = 'unlicense'
__version__ = '1.12.1.2'
__maintainer__ = 'Ilya Razmanov'
__email__ = 'ilyarazmanov@gmail.com'
__status__ = 'Production'

import array

''' ╔══════════╗
    ║ pnm2list ║
    ╚══════════╝ '''

def pnm2list(filename: str) -> tuple[int, int, int, int, list[list[list[int]]]]:
    """Read PGM or PPM file to nested image data list.

    Usage:

    ``X, Y, Z, maxcolors, image3D = pnmlpnm.pnm2list(in_filename)``

    for reading data from PPM/PGM, where:

    - X, Y, Z   - image sizes (int);
    - maxcolors - number of colors per channel for current image (int);
    - image3D   - image pixel data as list(list(list(int)));
    - in_filename - PPM/PGM file name (str).

    """

    with open(filename, 'rb') as file:  # Open file in binary mode
        magic = file.readline().strip().decode()

        # Passing comments by
        comment_line = file.readline().decode()
        while comment_line.startswith('#'):
            comment_line = file.readline().decode()

        # Reading dimensions. Photoshop CS6 uses EOLN as separator, GIMP, XnView etc. use space
        size_temp = comment_line.split()
        if len(size_temp) < 2:  # Part for Photoshop
            X = int(size_temp[0])
            Y = int(file.readline().decode())
        else:  # Part for most other software
            X, Y = map(int, comment_line.split())

        # Color depth
        maxcolors = int(file.readline().strip().decode())

        ''' ┌─────┐
            │ RGB │
            └────-┘ '''

        if magic == 'P6':  # RGB bin
            Z = 3
            list_3d = []
            for _ in range(Y):
                row = []
                for _ in range(X):

                    if maxcolors < 256:
                        red = int.from_bytes(file.read(1))
                        green = int.from_bytes(file.read(1))
                        blue = int.from_bytes(file.read(1))
                    else:
                        red = int.from_bytes(file.read(2))
                        green = int.from_bytes(file.read(2))
                        blue = int.from_bytes(file.read(2))

                    row.append([red, green, blue])
                list_3d.append(row)

        if magic == 'P3':  # RGB ascii
            Z = 3

            list_1d = []  # Toss everything to 1D list because linebreaks in PNM are unpredictable
            for _ in range(Y * X * Z):  # Y*X*Z most likely excessive but should cover any formatting
                pixel_data = file.readline().split()
                list_1d.extend(map(int, pixel_data))  # Extend to kill all formatting perversions.

            list_3d = [  # Now break 1D toss into component compounds, building 3D list
                [
                    [
                        list_1d[z + x * Z + y * X * Z] for z in range(Z)
                    ] for x in range(X)
                ] for y in range(Y)
            ]

        ''' ┌───┐
            │ L │
            └───┘ '''

        if magic == 'P5':  # L bin
            Z = 1
            list_3d = []
            for _ in range(Y):
                row = []
                for _ in range(X):
                    if maxcolors < 256:
                        channel = [int.from_bytes(file.read(1))]
                    else:
                        channel = [int.from_bytes(file.read(2))]
                    row.append(channel)
                list_3d.append(row)

        if magic == 'P2':  # L ascii
            Z = 1

            list_1d = []  # Toss everything to 1D list because linebreaks in ASCII PGM are unpredictable
            for _ in range(Y * X * Z):
                pixel_data = file.readline().split()
                list_1d.extend(map(int, pixel_data))

            list_3d = [  # Now break 1D toss into component compounds, building 3D list
                [
                    [
                        list_1d[z + x * Z + y * X * Z] for z in range(Z)
                    ] for x in range(X)
                ] for y in range(Y)
            ]

        return (X, Y, Z, maxcolors, list_3d)  # Output mimic that of pnglpng


''' ╔══════════╗
    ║ list2bin ║
    ╚══════════╝ '''

def list2bin(in_list_3d: list[list[list[int]]], maxcolors: int) -> bytes:
    """Convert PNG to PGM P5 or PPM P6 (binary) data structure in memory.

    Based on Netpbm specs at https://netpbm.sourceforge.net/doc/

    For LA and RGBA images A channel is deleted.

    Usage:

    ``image_bytes = pnmlpnm.list2bin(image3D, maxcolors)`` where:

    - ``image3D``   - Y*X*Z list (image) of lists (rows) of lists (pixels) of ints (channels);
    - ``maxcolors`` - number of colors per channel for current image (int).

    Output:

    - ``image_bytes`` - PNM-structured binary data.

    """

    # Determining list sizes
    Y = len(in_list_3d)
    X = len(in_list_3d[0])
    Z = len(in_list_3d[0][0])

    # Flattening 3D list to 1D list
    in_list_1d = [c for row in in_list_3d for px in row for c in px]

    if Z == 1:  # L image
        magic = 'P5'

    if Z == 2:  # LA image
        magic = 'P5'
        del in_list_1d[1::2]  # Deleting A channel

    if Z == 3:  # RGB image
        magic = 'P6'

    if Z == 4:  # RGBA image
        magic = 'P6'
        del in_list_1d[3::4]  # Deleting A channel

    if maxcolors < 256:
        datatype = 'B'
    else:
        datatype = 'H'

    header = array.array('B', f'{magic}\n{X} {Y}\n{maxcolors}\n'.encode())
    content = array.array(datatype, in_list_1d)

    content.byteswap()  # Critical!

    pnm = header.tobytes() + content.tobytes()

    return pnm  # End of "list2bin" list to PNM conversion function


''' ╔══════════╗
    ║ list2pnm ║
    ╚══════════╝ '''

def list2pnm(out_filename: str, in_list_3d: list[list[list[int]]], maxcolors: int) -> None:
    """Write PNM data structure as produced with ``list2bin`` to ``out_filename`` file.

    Usage:

    ``pnmlpnm.list2pnm(out_filename, image3D, maxcolors)`` where:

    - ``image3D``   - Y*X*Z list (image) of lists (rows) of lists (pixels) of ints (channels);
    - ``maxcolors`` - number of colors per channel for current image (int).

    Output:

    - ``out_filename`` - PNM file.


    """

    pnm = list2bin(in_list_3d, maxcolors)

    with open(out_filename, 'wb') as file_pnm:  # write pnm bin structure obtained above to file
        file_pnm.write(pnm)

    return None  # End of "list2pnm" function for writing "list2bin" output as file


''' ╔═══════════════╗
    ║ list2pnmascii ║
    ╚═══════════════╝ '''

def list2pnmascii(out_filename: str, in_list_3d: list[list[list[int]]], maxcolors: int) -> None:
    """Write ASCII PNM ``out_filename`` file.

    Usage:

    ``pnmlpnm.list2pnmascii(out_filename, image3D, maxcolors)`` where:

    - ``image3D``   - Y*X*Z list (image) of lists (rows) of lists (pixels) of ints (channels);
    - ``maxcolors`` - number of colors per channel for current image (int).

    Output:

    - ``out_filename`` - PNM file.

    """

    # Determining list sizes
    Y = len(in_list_3d)
    X = len(in_list_3d[0])
    Z = len(in_list_3d[0][0])

    # Flattening 3D list to 1D list
    in_list_1d = [c for row in in_list_3d for px in row for c in px]

    if Z == 1:  # L image
        magic = 'P2'

    if Z == 2:  # LA image
        magic = 'P2'
        del in_list_1d[1::2]  # Deleting A channel

    if Z == 3:  # RGB image
        magic = 'P3'

    if Z == 4:  # RGBA image
        magic = 'P3'
        del in_list_1d[3::4]  # Deleting A channel

    in_str_1d = ' '.join([str(c) for c in in_list_1d])  # Turning list to string

    with open(out_filename, 'w') as file_pnm:  # write pnm string structure obtained above to file
        file_pnm.write(f'{magic}\n{X} {Y}\n{maxcolors}\n')
        file_pnm.write(in_str_1d)

    return None  # End of "list2pnmascii" function for writing ASCII PPM/PGM file


''' ╔════════════════════╗
    ║ Create empty image ║
    ╚════════════════════╝ '''

def create_image(X: int, Y: int, Z: int) -> list[list[list[int]]]:
    """Create empty 3D nested list of X*Y*Z sizes."""

    new_image = [
        [
            [
                0 for z in range(Z)
            ] for x in range(X)
        ] for y in range(Y)
    ]

    return new_image  # End of "create_image" empty nested 3D list creation


# --------------------------------------------------------------

if __name__ == '__main__':
    print('Module to be imported, not run as standalone')
