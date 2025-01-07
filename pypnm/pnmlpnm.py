#!/usr/bin/env python3

"""Functions to read PPM and PGM files to nested 3D list of int and/or write back.

Overview
----------

pnmlpnm (pnm-list-pnm) is a pack of functions for dealing with PPM and PGM image files. Functions included are:

- pnm2list  - reading binary or ascii RGB PPM or L PGM file and returning image data as nested list of int.
- list2bin  - getting image data as nested list of int and creating binary PPM (P6) or PGM (P5) data structure in memory. Suitable for generating data to display with Tkinter `PhotoImage(data=...)` class.
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

May be freely used, redistributed and modified. In case of introducing useful modifications, please report to original developer.

References
-----------

Netpbm specs: https://netpbm.sourceforge.net/doc/

PyPNM at PyPI: https://pypi.org/project/PyPNM/

PyPNM at GitHub: https://github.com/Dnyarri/PyPNM/

Version history
----------------

0.11.26.0   Initial working version 26 Nov 2024.

0.11.27.3   Implemented fix for Adobe Photoshop CS6 using linebreaks instead of spaces in header.

0.11.28.0   Rewritten to use less arguments for output; X, Y, Z autodetected.

0.11.29.0   Added ASCII write support.

0.11.30.0   Switched to array, thus allowing 16 bpc P5 and P6 files writing.

0.11.30.2   Fixed 16 bpc P5 and P6 files reading. Solution looks ugly but works.

1.12.1.2    Initial public release.

1.12.12.1   PBM read support added. PBM write is not planned.

1.12.14.1   Reoptimized to comprehensions.

"""

__author__ = 'Ilya Razmanov'
__copyright__ = '(c) 2024 Ilya Razmanov'
__credits__ = 'Ilya Razmanov'
__license__ = 'unlicense'
__version__ = '1.12.14.1'
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

    magic_list = ['P6', 'P3', 'P5', 'P2', 'P4', 'P1']

    with open(filename, 'rb') as file:  # Open file in binary mode
        magic = file.readline().strip().decode()

        if magic not in magic_list:
            raise ValueError(f"Unsupported format {filename}: {magic[:32]}")

        # Passing comments by
        comment_line = file.readline().decode()
        while comment_line.startswith('#'):
            comment_line = file.readline().decode()

        ''' ┌─────┐
            │ RGB │
            └────-┘ '''

        if magic == 'P6':  # RGB bin

            # Reading dimensions. Photoshop CS6 uses EOLN as separator, GIMP, XnView etc. use space
            size_temp = comment_line.split()
            if len(size_temp) < 2:  # Part for Photoshop
                X = int(size_temp[0])
                Y = int(file.readline().decode())
            else:  # Part for most other software
                X, Y = map(int, comment_line.split())

            # Color depth
            maxcolors = int(file.readline().strip().decode())

            # Channel number
            Z = 3

            # Building 3D list of ints, converted from bytes
            list_3d = [
                [
                    [int.from_bytes(file.read(1)), int.from_bytes(file.read(1)), int.from_bytes(file.read(1))] if (maxcolors < 256) else [int.from_bytes(file.read(2)), int.from_bytes(file.read(2)), int.from_bytes(file.read(2))]  # Consecutive reading of R, G, B
                    for x in range(X)
                ] for y in range(Y)
            ]

        if magic == 'P3':  # RGB ASCII

            # Reading dimensions. Photoshop CS6 uses EOLN as separator, GIMP, XnView etc. use space
            size_temp = comment_line.split()
            if len(size_temp) < 2:  # Part for Photoshop
                X = int(size_temp[0])
                Y = int(file.readline().decode())
            else:  # Part for most other software
                X, Y = map(int, comment_line.split())

            # Color depth
            maxcolors = int(file.readline().strip().decode())

            # Channel number
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

            # Reading dimensions. Photoshop CS6 uses EOLN as separator, GIMP, XnView etc. use space
            size_temp = comment_line.split()
            if len(size_temp) < 2:  # Part for Photoshop
                X = int(size_temp[0])
                Y = int(file.readline().decode())
            else:  # Part for most other software
                X, Y = map(int, comment_line.split())

            # Color depth
            maxcolors = int(file.readline().strip().decode())

            # Channel number
            Z = 1
            # Building 3D list of ints, converted from bytes
            list_3d = [
                [
                    [
                        int.from_bytes(file.read(1)) if (maxcolors < 256) else int.from_bytes(file.read(2))
                    ] for x in range(X)
                ] for y in range(Y)
            ]

        if magic == 'P2':  # L ASCII

            # Reading dimensions. Photoshop CS6 uses EOLN as separator, GIMP, XnView etc. use space
            size_temp = comment_line.split()
            if len(size_temp) < 2:  # Part for Photoshop
                X = int(size_temp[0])
                Y = int(file.readline().decode())
            else:  # Part for most other software
                X, Y = map(int, comment_line.split())

            # Color depth
            maxcolors = int(file.readline().strip().decode())

            # Channel number
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


        ''' ┌─────┐
            │ Bit │
            └────-┘ '''

        if magic == 'P4':  # Bit bin
            # Reading dimensions. Photoshop CS6 uses EOLN as separator, GIMP, XnView etc. use space
            size_temp = comment_line.split()
            if len(size_temp) < 2:  # Part for Photoshop
                X = int(size_temp[0])
                Y = int(file.readline().decode())
            else:  # Part for most other software
                X, Y = map(int, comment_line.split())

            # Color depth
            maxcolors = 255  # Force conversion from bit to L

            # Channel number
            Z = 1

            raw_data = file.read()  # Reading the rest of file

            row_width = (X + 7) // 8  # Rounded up version of width, to get whole bytes included junk at EOLNs

            list_3d = []
            for y in range(Y):
                row = []
                for x in range(row_width):
                    single_byte = raw_data[(y * row_width) + x]
                    single_byte_bits = [int(bit) for bit in bin(single_byte)[2:].zfill(8)]
                    single_byte_bits_normalized = [[255 * (1 - c)] for c in single_byte_bits]  # renormalizing colors from ink on/off to L model, replacing int with [int]
                    row.extend(single_byte_bits_normalized)  # assembling row, junk included

                list_3d.append(row[0:X])  # apparently cutting junk off

        if magic == 'P1':  # Bit ASCII

            # Reading dimensions. Photoshop CS6 uses EOLN as separator, GIMP, XnView etc. use space
            size_temp = comment_line.split()
            if len(size_temp) < 2:  # Part for Photoshop
                X = int(size_temp[0])
                Y = int(file.readline().decode())
            else:  # Part for most other software
                X, Y = map(int, comment_line.split())

            # Color depth
            maxcolors = 255  # Force conversion from bit to L

            # Channel number
            Z = 1

            list_1d = []  # Toss everything to 1D list because linebreaks in ASCII PBM are unpredictable
            for y in file:
                row_data = y.strip()
                bits = [(255 * (1 - int(row_data[i : i + 1]))) for i in range(0, len(row_data), 1)]
                list_1d.extend(bits)

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
    """Convert nested image data list to PGM P5 or PPM P6 (binary) data structure in memory.

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

    content.byteswap()  # Critical for 16 bits per channel

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

    - ``out_filename`` - PNM file name.


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

    - ``out_filename`` - PNM file name.

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
