#!/usr/bin/env python3

'''Functions to read PPM and PGM files to nested 3D list of int and/or write back.

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

``X, Y, Z, maxcolors, list_3d = pnmlpnm.pnm2list(in_filename)``

for reading data from PPM/PGM, where:

- X, Y, Z   - image sizes (int);
- maxcolors - number of colors per channel for current image (int);
- list_3d   - image pixel data as list(list(list(int)));

and

``pnmlpnm.pnm = list2bin(list_3d, maxcolors)``

for writing data from list_3d nested list to 'pnm' bytes object in memory,

or 

``pnmlpnm.list2pnm(out_filename, list_3d, maxcolors)``

or

``pnmlpnm.list2pnmascii(out_filename, list_3d, maxcolors)``

for writing data from list_3d nested list to PPM/PGM file 'out_filename'.


Copyright and redistribution
-----------------------------
Written by Ilya Razmanov (https://dnyarri.github.io/) to provide working with PPM/PGM files and creating PPM data to be displayed with Tkinter 'PhotoImage' class.

May be freely used, redistributed and modified. In case of introducing useful modifications, please report to original developer.

References
-----------

Netpbm specs: https://netpbm.sourceforge.net/doc/

PyPNM at PyPI: https://pypi.org/project/PyPNM/

PyPNM at GitHub: https://github.com/Dnyarri/PyPNM/

Version history
----------------

0.11.26.0   Initial working version 26 Nov 2024.

1.12.14.1   Public release on https://pypi.org/project/PyPNM/

1.13.09.0   Complete rewriting of `pnm2list` using `re` and `array`; PPM and PGM support rewritten.

1.13.10.5   Header pattern seem to comprise all problematic cases; PBM support rewritten.

'''

__author__ = 'Ilya Razmanov'
__copyright__ = '(c) 2024 Ilya Razmanov'
__credits__ = 'Ilya Razmanov'
__license__ = 'unlicense'
__version__ = '1.13.10.7'
__maintainer__ = 'Ilya Razmanov'
__email__ = 'ilyarazmanov@gmail.com'
__status__ = 'Production'

import array
import re

''' ╔══════════╗
    ║ pnm2list ║
    ╚══════════╝ '''

def pnm2list(in_filename: str) -> tuple[int, int, int, int, list[list[list[int]]]]:
    '''Read PGM or PPM file to nested image data list.

    Usage:

    ``X, Y, Z, maxcolors, list_3d = pnmlpnm.pnm2list(in_filename)``

    for reading data from PPM/PGM, where:

    - X, Y, Z   - image sizes (int);
    - maxcolors - number of colors per channel for current image (int);
    - list_3d   - image pixel data as list(list(list(int)));
    - in_filename - PPM/PGM file name (str).

    '''

    with open(in_filename, 'rb') as file:  # Open file in binary mode
        full_bytes = file.read()

    if full_bytes.startswith((b'P6', b'P5', b'P3', b'P2')):

        ''' ┌────────────────────┐
            │ IF Continuous tone │
            └────────────────────┘ '''
        # Getting header by pattern
        header: list[bytes] = re.search(
            br'(^P\d\s(?:\s*#.*\s)*'  # last \s gives better compatibility than [\r\n]
            br'\s*(\d+)\s(?:\s*#.*\s)*'  # first \s further improves compatibility
            br'\s*(\d+)\s(?:\s*#.*\s)*'
            br'\s*(\d+)\s)',
            full_bytes,
        ).groups()

        magic, X, Y, maxcolors = header

        magic = (magic.split()[0]).decode()
        X = int(X)
        Y = int(Y)
        maxcolors = int(maxcolors)

        # Removing header by the same pattern, leaving only image data
        filtered = re.sub(
            br'(^P\d\s(?:\s*#.*\s)*'  # pattern to replace to
            br'\s*(\d+)\s(?:\s*#.*\s)*'
            br'\s*(\d+)\s(?:\s*#.*\s)*'
            br'\s*(\d+)\s)',
            b'',  # empty space to replace with
            full_bytes,
        )

        del full_bytes  # Cleanup

        if (magic == 'P6') or (magic == 'P3'):
            Z = 3
        elif (magic == 'P5') or (magic == 'P2'):
            Z = 1

        if (magic == 'P6') or (magic == 'P5'):

            ''' ┌───────────────────────────┐
                │ IF Binary continuous tone │
                └───────────────────────────┘ '''

            if maxcolors < 256:
                datatype = 'B'
            else:
                datatype = 'H'

            array_1d = array.array(datatype, filtered)

            array_1d.byteswap()  # Critical for 16 bits per channel

            list_1d = array_1d.tolist()

            list_3d = [
                        [
                            [
                                list_1d[z + x * Z + y * X * Z] for z in range(Z)
                            ] for x in range(X)
                        ] for y in range(Y)
                    ]

        if (magic == 'P3') or (magic == 'P2'):

            ''' ┌──────────────────────────┐
                │ IF ASCII continuous tone │
                └──────────────────────────┘ '''

            list_1d = filtered.split()

            list_3d = [
                        [
                            [
                                int(list_1d[z + x * Z + y * X * Z]) for z in range(Z)
                            ] for x in range(X)
                        ] for y in range(Y)
                    ]

    elif full_bytes.startswith((b'P4', b'P1')):

        ''' ┌────────────────┐
            │ IF 1 Bit/pixel │
            └────────────────┘ '''
        # Getting header by pattern. Note that for 1 bit pattern does not include maxcolors
        header: list[bytes] = re.search(
            br'(^P\d\s(?:\s*#.*\s)*'  # last \s gives better compatibility than [\r\n]
            br'\s*(\d+)\s(?:\s*#.*\s)*'  # first \s further improves compatibility
            br'\s*(\d+)\s)',
            full_bytes,
        ).groups()

        magic, X, Y = header

        magic = (magic.split()[0]).decode()
        X = int(X)
        Y = int(Y)
        Z = 1
        maxcolors = 255 # Forcing conversion to L

        # Removing header by the same pattern, leaving only image data
        filtered = re.sub(
            br'(^P\d\s(?:\s*#.*\s)*'  # pattern to replace to
            br'\s*(\d+)\s(?:\s*#.*\s)*'
            br'\s*(\d+)\s)',
            b'',  # empty space to replace with
            full_bytes,
        )

        del full_bytes  # Cleanup

        if magic == 'P4':

            ''' ┌───────────────────────┐
                │ IF Binary 1 Bit/pixel │
                └───────────────────────┘ '''

            row_width = (X + 7) // 8  # Rounded up version of width, to get whole bytes including junk at EOLNs

            list_3d = []
            for y in range(Y):
                row = []
                for x in range(row_width):
                    single_byte = filtered[(y * row_width) + x]
                    single_byte_bits = [int(bit) for bit in bin(single_byte)[2:].zfill(8)]
                    single_byte_bits_normalized = [[255 * (1 - c)] for c in single_byte_bits]  # renormalizing colors from ink on/off to L model, replacing int with [int]
                    row.extend(single_byte_bits_normalized)  # assembling row, junk included

                list_3d.append(row[0:X])  # apparently cutting junk off

        if magic == 'P1':

            ''' ┌──────────────────────┐
                │ IF ASCII 1 Bit/pixel │
                └──────────────────────┘ '''

            ''' Removing any formatting by consecutive split/join, then changing types to turn bit char into int while reshaping to 3D nested list. Probably not the fastest solution but I will think about it tomorrow. '''
            list_1d = list(str(b''.join(filtered.split())))[2:-1]  # Slicing off junk chars like 'b', "'"

            list_3d = [
                [
                    [
                        (255 * (1 - int(list_1d[z + x * Z + y * X * Z]))) for z in range(Z)
                    ] for x in range(X)
                ] for y in range(Y)
            ]

    else:
        raise ValueError(f"Unsupported format {in_filename}: {full_bytes[:32]}")

    return (X, Y, Z, maxcolors, list_3d)  # Output mimic that of pnglpng


''' ╔══════════╗
    ║ list2bin ║
    ╚══════════╝ '''

def list2bin(list_3d: list[list[list[int]]], maxcolors: int) -> bytes:
    '''Convert nested image data list to PGM P5 or PPM P6 (binary) data structure in memory.

    Based on Netpbm specs at https://netpbm.sourceforge.net/doc/

    For LA and RGBA images A channel is deleted.

    Usage:

    ``image_bytes = pnmlpnm.list2bin(list_3d, maxcolors)`` where:

    - ``list_3d``   - Y*X*Z list (image) of lists (rows) of lists (pixels) of ints (channels);
    - ``maxcolors`` - number of colors per channel for current image (int).

    Output:

    - ``image_bytes`` - PNM-structured binary data.

    '''

    # Determining list sizes
    Y = len(list_3d)
    X = len(list_3d[0])
    Z = len(list_3d[0][0])

    # Flattening 3D list to 1D list
    list_1d = [c for row in list_3d for px in row for c in px]

    if Z == 1:  # L image
        magic = 'P5'

    if Z == 2:  # LA image
        magic = 'P5'
        del list_1d[1::2]  # Deleting A channel

    if Z == 3:  # RGB image
        magic = 'P6'

    if Z == 4:  # RGBA image
        magic = 'P6'
        del list_1d[3::4]  # Deleting A channel

    if maxcolors < 256:
        datatype = 'B'
    else:
        datatype = 'H'

    header = array.array('B', f'{magic}\n{X} {Y}\n{maxcolors}\n'.encode())
    content = array.array(datatype, list_1d)

    content.byteswap()  # Critical for 16 bits per channel

    pnm = header.tobytes() + content.tobytes()

    return pnm  # End of 'list2bin' list to PNM conversion function


''' ╔══════════╗
    ║ list2pnm ║
    ╚══════════╝ '''

def list2pnm(out_filename: str, list_3d: list[list[list[int]]], maxcolors: int) -> None:
    '''Write PNM data structure as produced with ``list2bin`` to ``out_filename`` file.

    Usage:

    ``pnmlpnm.list2pnm(out_filename, list_3d, maxcolors)`` where:

    - ``list_3d``   - Y*X*Z list (image) of lists (rows) of lists (pixels) of ints (channels);
    - ``maxcolors`` - number of colors per channel for current image (int).

    Output:

    - ``out_filename`` - PNM file name.


    '''

    pnm = list2bin(list_3d, maxcolors)

    with open(out_filename, 'wb') as file_pnm:  # write pnm bin structure obtained above to file
        file_pnm.write(pnm)

    return None  # End of 'list2pnm' function for writing 'list2bin' output as file


''' ╔═══════════════╗
    ║ list2pnmascii ║
    ╚═══════════════╝ '''

def list2pnmascii(out_filename: str, list_3d: list[list[list[int]]], maxcolors: int) -> None:
    '''Write ASCII PNM ``out_filename`` file.

    Usage:

    ``pnmlpnm.list2pnmascii(out_filename, list_3d, maxcolors)`` where:

    - ``list_3d``   - Y*X*Z list (image) of lists (rows) of lists (pixels) of ints (channels);
    - ``maxcolors`` - number of colors per channel for current image (int).

    Output:

    - ``out_filename`` - PNM file name.

    '''

    # Determining list sizes
    Y = len(list_3d)
    X = len(list_3d[0])
    Z = len(list_3d[0][0])

    # Flattening 3D list to 1D list
    list_1d = [c for row in list_3d for px in row for c in px]

    if Z == 1:  # L image
        magic = 'P2'

    if Z == 2:  # LA image
        magic = 'P2'
        del list_1d[1::2]  # Deleting A channel

    if Z == 3:  # RGB image
        magic = 'P3'

    if Z == 4:  # RGBA image
        magic = 'P3'
        del list_1d[3::4]  # Deleting A channel

    in_str_1d = ' '.join([str(c) for c in list_1d])  # Turning list to string

    with open(out_filename, 'w') as file_pnm:  # write pnm string structure obtained above to file
        file_pnm.write(f'{magic}\n{X} {Y}\n{maxcolors}\n')
        file_pnm.write(in_str_1d)

    return None  # End of 'list2pnmascii' function for writing ASCII PPM/PGM file


''' ╔════════════════════╗
    ║ Create empty image ║
    ╚════════════════════╝ '''

def create_image(X: int, Y: int, Z: int) -> list[list[list[int]]]:
    '''Create empty 3D nested list of X*Y*Z sizes.'''

    new_image = [
        [
            [
                0 for z in range(Z)
            ] for x in range(X)
        ] for y in range(Y)
    ]

    return new_image  # End of 'create_image' empty nested 3D list creation


# --------------------------------------------------------------

if __name__ == '__main__':
    print('Module to be imported, not run as standalone')
