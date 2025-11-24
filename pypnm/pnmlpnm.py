#!/usr/bin/env python3

"""
=====
PyPNM
=====
--------------------------------------------------------------------------
PPM and PGM image files reading, displaying and writing for Python >=3.11.
--------------------------------------------------------------------------

Overview
--------

PyPNM module comprise a set of functions for dealing with
`PPM`_ and `PGM`_ image files, and images, represented as
Python nested lists, namely:

- **``pnm2list``**: reading binary or ASCII
RGB `PPM`_, or L `PGM`_, or ink on/off `PBM`_ file
and returning image data as nested list of int.

- **``list2bin``**: getting image data as nested list of int and
creating binary PPM (P6) or PGM (P5) data structure in memory.

    Suitable for generating data to display with Tkinter
    ``PhotoImage(data=...)`` class.

- **``list2pnmbin``**: getting image data as nested list of int
and writing binary PPM (P6) or PGM (P5) image file.

    .. note:: Bytes generations procedure is different from that
        used in ``list2bin``.

- **``list2pnmascii``**: getting image data as nested list of int
and writing ASCII PPM (P3) or PGM (P2) image file.

- **``list2pnm``**: getting image data as nested list of int
and writing either binary or ASCII PNM file depending on ``bin`` value.

- ``create_image``: creating empty nested 3D list for image representation.

Usage
-----

After ``from pypnm import pnmlpnm``, use something like::

    X, Y, Z, maxcolors, list_3d = pnmlpnm.pnm2list(in_filename)

for reading data from PPM/PGM, where:

- ``X``, ``Y``, ``Z``: image dimensions (int);
- ``maxcolors``: maximum value of color per channel for current image (int);
- ``list_3d``: image pixel data as list(list(list(int)));

and::

    pnm_bytes = pnmlpnm.list2bin(list_3d, maxcolors)

for writing data from ``list_3d`` nested list to in-memory ``pnm_bytes``
bytes object to be displayed with Tkinter ``PhotoImage(data=...)``,

or::

    pnmlpnm.list2pnm(out_filename, list_3d, maxcolors, bin)

for writing data from ``list_3d`` nested list to PPM/PGM file ``out_filename``,
where ``bin`` is a bool switch defining whether
resulting file will be binary or ASCII.

.. note:: ``maxcolors`` is either 255 for 8 bit or 65535 for 16 bit images.
    1 bit ink on/off images get promoted and inverted to 8 bit L upon import,
    i.e. PBM converted to PGM when reading (writing PBM is not planned).

References
----------

1. `Netpbm specifications`_
2. `PyPNM for Python >= 3.11`_ at GitHub
3. `PyPNM for Python >= 3.4`_ at GitHub
4. `PyPNM at PyPI`_
5. `PyPNM Documentation`_ (PDF)
6. `Changelog`_ for this version

.. _Netpbm specifications: https://netpbm.sourceforge.net/doc/

.. _PPM: https://netpbm.sourceforge.net/doc/ppm.html

.. _PGM: https://netpbm.sourceforge.net/doc/pgm.html

.. _PBM: https://netpbm.sourceforge.net/doc/pbm.html

.. _PyPNM for Python >= 3.11: https://github.com/Dnyarri/PyPNM/

.. _PyPNM for Python >= 3.4: https://github.com/Dnyarri/PyPNM/tree/py34

.. _PyPNM at PyPI: https://pypi.org/project/PyPNM/

.. _PyPNM Documentation: https://dnyarri.github.io/pypnm/pypnm.pdf

.. _Changelog: https://github.com/Dnyarri/PyPNM/blob/main/CHANGELOG.md

"""

__author__ = 'Ilya Razmanov'
__copyright__ = '(c) 2024-2025 Ilya Razmanov'
__credits__ = 'Ilya Razmanov'
__license__ = 'unlicense'
__version__ = '2.23.23.23'
__maintainer__ = 'Ilya Razmanov'
__email__ = 'ilyarazmanov@gmail.com'
__status__ = 'Production'

import array
import mmap
from re import search, sub

""" ╔══════════════════════════════╗
    ║           pnm2list           ║
    ╟──────────────────────────────╢
    ║ WARNING: internal functions  ║
    ║ do not perform format check! ║
    ╚══════════════════════════════╝ """


def pnm2list(in_filename: str) -> tuple[int, int, int, int, list[list[list[int]]]]:
    """Read PBM, PGM or PPM file to nested image data list.

    :param str in_filename: input file name;
    :return X, Y, Z, maxcolors, list_3d: tuple, consisting of:

    - ``X``, ``Y``, ``Z``: PNM image dimensions (int);
    - ``maxcolors``: number of colors per channel for current image (int),
    either 255, or 65535;
    - ``list_3d``: list (image) of lists (rows) of lists (pixels)
    of ints (channel values).

    """

    """ ┌───────────────────────────┐
        │ IF Binary continuous tone │
        └───────────────────────────┘ """

    def _p65(in_filename: str) -> tuple[int, int, int, int, list[list[list[int]]]]:
        """Open P6 and P5 PNM"""
        with open(in_filename, 'rb') as file:  # Open file for mmap
            with mmap.mmap(file.fileno(), 0, access=mmap.ACCESS_READ) as full_bytes_mmap:
                # ↓ Getting header by pattern
                header = search(
                    rb'(^P\d\s(?:\s*#.*\s)*'  # last \s gives better compatibility than [\r\n]
                    rb'\s*(\d+)\s(?:\s*#.*\s)*'  # first \s further improves compatibility
                    rb'\s*(\d+)\s(?:\s*#.*\s)*'
                    rb'\s*(\d+)\s)',
                    full_bytes_mmap,
                ).groups()

                # ↓ Splitting header into image properties values
                magic, X, Y, maxcolors = header
                magic = (magic.split()[0]).decode('ascii')
                X = int(X)
                Y = int(Y)
                Z = 3 if magic == 'P6' else 1  # assuming P5 is the only alternative to P6
                maxcolors = int(maxcolors)

                # ↓ Removing header by the same pattern, leaving only image data
                filtered_bytes = sub(
                    rb'(^P\d\s(?:\s*#.*\s)*'  # pattern to replace to
                    rb'\s*(\d+)\s(?:\s*#.*\s)*'
                    rb'\s*(\d+)\s(?:\s*#.*\s)*'
                    rb'\s*(\d+)\s)',
                    b'',  # empty space to replace pattern with
                    full_bytes_mmap,
                )
        # ↑ got copy of file without header as `filtered_bytes` bytes

        # ↓ Converting bytes to array
        if maxcolors < 256:
            array_1d = array.array('B', filtered_bytes)
        else:
            array_1d = array.array('H', filtered_bytes)
            array_1d.byteswap()  # Critical for 16 bits per channel
        del filtered_bytes  # Cleanup

        # ↓ Converting array to list
        list_1d = array_1d.tolist()
        del array_1d  # Cleanup

        # ↓ Reshaping flat 1D list to 3Dlist
        list_3d = [[[list_1d[z + x * Z + y * X * Z] for z in range(Z)] for x in range(X)] for y in range(Y)]
        del list_1d  # Cleanup

        return (X, Y, Z, maxcolors, list_3d)

    """ ┌──────────────────────────┐
        │ IF ASCII continuous tone │
        └──────────────────────────┘ """

    def _p32(in_filename: str) -> tuple[int, int, int, int, list[list[list[int]]]]:
        """Open P3 and P5 PNM"""
        with open(in_filename, 'r') as file:  # Open file for mmap
            with mmap.mmap(file.fileno(), 0, access=mmap.ACCESS_READ) as full_bytes_mmap:
                # ↓ Getting header by pattern
                header = search(
                    rb'(^P\d\s(?:\s*#.*\s)*'  # last \s gives better compatibility than [\r\n]
                    rb'\s*(\d+)\s(?:\s*#.*\s)*'  # first \s further improves compatibility
                    rb'\s*(\d+)\s(?:\s*#.*\s)*'
                    rb'\s*(\d+)\s)',
                    full_bytes_mmap,
                ).groups()

                # ↓ Splitting header into image properties values
                magic, X, Y, maxcolors = header
                magic = (magic.split()[0]).decode('ascii')
                X = int(X)
                Y = int(Y)
                Z = 3 if (magic == 'P3') else 1  # assuming P2 is the only alternative to P3
                maxcolors = int(maxcolors)

                # ↓ Removing header by the same pattern, leaving only image data
                filtered_chars = sub(
                    rb'(^P\d\s(?:\s*#.*\s)*'  # pattern to replace to
                    rb'\s*(\d+)\s(?:\s*#.*\s)*'
                    rb'\s*(\d+)\s(?:\s*#.*\s)*'
                    rb'\s*(\d+)\s)',
                    b'',  # empty space to replace pattern with
                    full_bytes_mmap,
                ).decode('ascii')
        # ↑ got copy of file without header as `filtered_chars` str

        # ↓ Converting to 1D list of strings, ignoring any formatting
        list_1d = filtered_chars.split()
        del filtered_chars  # Cleanup

        # ↓ Converting 1D list of strings to 3D list of int
        list_3d = [[[int(list_1d[z + x * Z + y * X * Z]) for z in range(Z)] for x in range(X)] for y in range(Y)]
        del list_1d  # Cleanup

        return (X, Y, Z, maxcolors, list_3d)

    """ ┌───────────────────────┐
        │ IF Binary 1 Bit/pixel │
        └───────────────────────┘ """

    def _p4(in_filename: str) -> tuple[int, int, int, int, list[list[list[int]]]]:
        """Open P4 PNM"""
        with open(in_filename, 'rb') as file:  # Open file for mmap
            with mmap.mmap(file.fileno(), 0, access=mmap.ACCESS_READ) as full_bytes_mmap:
                # ↓ Getting header by pattern. Note that for 1 bit pattern does not include maxcolors
                header = search(
                    rb'(^P\d\s(?:\s*#.*\s)*'  # last \s gives better compatibility than [\r\n]
                    rb'\s*(\d+)\s(?:\s*#.*\s)*'  # first \s further improves compatibility
                    rb'\s*(\d+)\s)',
                    full_bytes_mmap,
                ).groups()

                # ↓ Splitting header into image properties values
                magic, X, Y = header
                magic = (magic.split()[0]).decode('ascii')
                X = int(X)
                Y = int(Y)
                Z = 1
                maxcolors = 255  # Forcing conversion to 8 bit L

                # ↓ Removing header by the same pattern, leaving only image data
                filtered_bytes = sub(
                    rb'(^P\d\s(?:\s*#.*\s)*'  # pattern to replace to
                    rb'\s*(\d+)\s(?:\s*#.*\s)*'
                    rb'\s*(\d+)\s)',
                    b'',  # empty space to replace pattern with
                    full_bytes_mmap,
                )
        # ↑ got copy of file without header as `filtered_bytes` bytes

        # ↓ Converting packed bits from bytes to 3D list of int, inverting values,
        #   and multiplying by maxcolor to obtain 8 bit L.
        row_width = (X + 7) // 8  # Rounded up version of width, to get whole bytes including junk at EOLNs
        list_3d = []
        for y in range(Y):
            row = []
            for x in range(row_width):
                single_byte = filtered_bytes[(y * row_width) + x]
                # ↓ Unpacking bytes to int(bits), including artificial junk in a last one in a row
                single_byte_bits = [int(bit) for bit in bin(single_byte)[2:].zfill(8)]
                # ↓ renormalizing colors from ink on/off to L model, replacing int with [int]
                single_byte_bits_normalized = [[maxcolors * (1 - c)] for c in single_byte_bits]
                # ↓ assembling row, junk at the end included
                row.extend(single_byte_bits_normalized)
            # ↓ Assembling image from rows, cutting junk off in the process
            list_3d.append(row[0:X])

        return (X, Y, Z, maxcolors, list_3d)

    """ ┌──────────────────────┐
        │ IF ASCII 1 Bit/pixel │
        └──────────────────────┘ """

    def _p1(in_filename: str) -> tuple[int, int, int, int, list[list[list[int]]]]:
        """Open P1 PNM"""
        with open(in_filename, 'r') as file:  # Open file for mmap
            with mmap.mmap(file.fileno(), 0, access=mmap.ACCESS_READ) as full_bytes_mmap:
                # ↓ Getting header by pattern. Note that for 1 bit pattern does not include maxcolors
                header = search(
                    rb'(^P\d\s(?:\s*#.*\s)*'  # last \s gives better compatibility than [\r\n]
                    rb'\s*(\d+)\s(?:\s*#.*\s)*'  # first \s further improves compatibility
                    rb'\s*(\d+)\s)',
                    full_bytes_mmap,
                ).groups()

                # ↓ Splitting header into image properties values
                magic, X, Y = header
                magic = magic.split()[0].decode('ascii')
                X = int(X)
                Y = int(Y)
                Z = 1
                maxcolors = 255  # Forcing conversion to 8 bit L

                # ↓ Removing header by the same pattern, leaving only image data
                filtered_chars = sub(
                    rb'(^P\d\s(?:\s*#.*\s)*'  # pattern to replace to
                    rb'\s*(\d+)\s(?:\s*#.*\s)*'
                    rb'\s*(\d+)\s)',
                    b'',  # empty space to replace pattern with
                    full_bytes_mmap,
                ).decode('ascii')
        # ↑ got copy of file without header as `filtered_chars` str

        # ↓ Converting to single str, removing any formatting
        str_1d = ''.join(filtered_chars.split())
        del filtered_chars  # Cleanup

        # ↓ Converting str to 3D list of int,
        #   inverting values and multiplying by maxcolor to obtain 8 bit L.
        list_3d = [[[maxcolors * (1 - int(str_1d[x + y * X]))] for x in range(X)] for y in range(Y)]
        del str_1d  # Cleanup

        return (X, Y, Z, maxcolors, list_3d)

    """ ┌─────────────────────────┐
        │ PNM header type switch. │
        │   Format check ensued.  │
        └─────────────────────────┘ """
    with open(in_filename, 'rb') as file:  # Open file in binary mode
        beginnings = file.read(2)  # Read first two bytes 'Pn' and close file

    if beginnings.startswith(b'P6'):  # Binary PPM
        return _p65(in_filename)
    elif beginnings.startswith(b'P5'):  # Binary PGM
        return _p65(in_filename)
    elif beginnings.startswith(b'P4'):  # Binary PBM
        return _p4(in_filename)
    elif beginnings.startswith(b'P3'):  # ASCII PPM
        return _p32(in_filename)
    elif beginnings.startswith(b'P2'):  # ASCII PGM
        return _p32(in_filename)
    elif beginnings.startswith(b'P1'):  # ASCII PBM
        return _p1(in_filename)
    else:
        raise ValueError(f'Header {beginnings} is not in P1:P6 range')


# ↑ End of pnm2list PNM reading function


""" ╔══════════╗
    ║ list2bin ║
    ╚══════════╝ """


def list2bin(list_3d: list[list[list[int]]], maxcolors: int, show_chessboard: bool = False) -> bytes:
    """Convert nested image data list to PGM P5 or PPM P6 bytes in memory.

    :param list_3d: image as list (image) of lists (rows) of lists (pixels)
    of ints (channels);
    :type list_3d: list[list[list[int]]]
    :param int maxcolors: number of colors per channel for current image,
    either 255, or 65535;
    :param bool show_chessboard: if set ``True`` and alpha channel exist,
    render preview against chessboard, otherwise skip alpha;
    :return: PNM-like object in memory.
    :rtype: bytes

    """

    def _chess(x: int, y: int) -> int:
        """Chessboard pattern, size and color match Photoshop 7.0 Light Medium.

        Photoshop chess pattern preset parameters:
        - Small: 4 px | Medium: 8 px | Large: 16 px;
        - Light: (0.8, 1.0) | Medium: (0.4, 0.6) | Dark: (0.2, 0.4) of ``maxcolors``.

        """
        return int(maxcolors * 0.8) if ((y // 8) % 2) == ((x // 8) % 2) else maxcolors

    # ↓ Image X, Y, Z sizes
    Y = len(list_3d)
    X = len(list_3d[0])
    Z = len(list_3d[0][0])

    magic = 'P5' if Z < 3 else 'P6'  # PGM or PPM

    if Z == 3 or Z == 1:  # Source has no alpha
        Z_READ = Z  # Number of color channels
        # ↓ Generator: Flattening 3D list to 1D list
        list_1d = (list_3d[y][x][z] for y in range(Y) for x in range(X) for z in range(Z_READ))
    else:  # Source has alpha
        Z_READ = min(Z, 4) - 1  # Number of color channels without alpha; clipping anything above RGB off

        if show_chessboard:
            # ↓ Generator: Flattening 3D list to 1D list, mixing with chessboard
            list_1d = ((((list_3d[y][x][z] * list_3d[y][x][Z_READ]) + (_chess(x, y) * (maxcolors - list_3d[y][x][Z_READ]))) // maxcolors) for y in range(Y) for x in range(X) for z in range(Z_READ))
        else:
            # ↓ Generator: Flattening 3D list to 1D list, skipping alpha
            list_1d = (list_3d[y][x][z] for y in range(Y) for x in range(X) for z in range(Z_READ))

    if maxcolors < 256:
        content = array.array('B', list_1d)  # Bytes
    else:
        content = array.array('H', list_1d)  # Doubles
        content.byteswap()  # Critical for 16 bits per channel

    return b''.join((f'{magic}\n{X} {Y}\n{maxcolors}\n'.encode('ascii'), content.tobytes()))


# ↑ End of 'list2bin' list to in-memory PNM conversion function


""" ╔═════════════╗
    ║ list2pnmbin ║
    ╚═════════════╝ """


def list2pnmbin(out_filename: str, list_3d: list[list[list[int]]], maxcolors: int) -> None:
    """Write binary PNM ``out_filename`` file; writing performed per row to reduce RAM usage.

    :param str out_filename: name of the PNM file to be written;
    :param list_3d: image as list (image) of lists (rows) of lists (pixels)
    of ints (channels);
    :type list_3d: list[list[list[int]]]
    :param int maxcolors: number of colors per channel for current image,
    either 255, or 65535.
    :return: None

    """

    # ↓ Image X, Y, Z sizes
    Y = len(list_3d)
    X = len(list_3d[0])
    Z = len(list_3d[0][0])

    magic = 'P5' if Z < 3 else 'P6'  # PGM or PPM
    Z_READ = Z if Z == 3 or Z == 1 else min(Z, 4) - 1  # To skip alpha later; clipping anything above RGB off
    datatype = 'B' if maxcolors < 256 else 'H'

    with open(out_filename, 'wb') as file_pnm:
        file_pnm.write(f'{magic}\n{X} {Y}\n{maxcolors}\n'.encode('ascii'))  # Writing PNM header to file
        for y in range(Y):
            # ↓ Generator: Flattening one row
            row_1d = (list_3d[y][x][z] for x in range(X) for z in range(Z_READ))
            row_array = array.array(datatype, row_1d)  # list[int] to array
            if maxcolors > 255:
                row_array.byteswap()  # Critical for 16 bits per channel
            file_pnm.write(row_array)  # Writing row bytes array to file

    return None


# ↑ End of 'list2pnmbin' function writing binary PPM/PGM file


""" ╔═══════════════╗
    ║ list2pnmascii ║
    ╚═══════════════╝ """


def list2pnmascii(out_filename: str, list_3d: list[list[list[int]]], maxcolors: int) -> None:
    """Write ASCII PNM ``out_filename`` file; writing performed per sample to reduce RAM usage.

    :param str out_filename: name of the PNM file to be written;
    :param list_3d: image as list (image) of lists (rows) of lists (pixels)
    of ints (channels);
    :type list_3d: list[list[list[int]]]
    :param int maxcolors: number of colors per channel for current image,
    either 255, or 65535.
    :return: None

    """

    # ↓ Image X, Y, Z sizes
    Y = len(list_3d)
    X = len(list_3d[0])
    Z = len(list_3d[0][0])

    if Z < 3:  # L or LA image
        magic = 'P2'
        Z_READ = 1
    else:  # RGB or RGBA image
        magic = 'P3'
        Z_READ = 3

    with open(out_filename, 'w') as file_pnm:
        file_pnm.write(f'{magic}\n{X} {Y}\n{maxcolors}\n')  # Writing PNM header to file
        sample_count = 0  # Start counting samples to break line <= 60 char
        for y in range(Y):
            for x in range(X):
                for z in range(Z_READ):
                    sample_count += 1
                    if (sample_count % 3) == 0:  # 3 must fit any specs for line length
                        file_pnm.write('\n')  # Writing break to fulfill specs line <= 60 char
                    file_pnm.write(f'{list_3d[y][x][z]} ')  # Writing channel value to file

    return None


# ↑ End of 'list2pnmascii' function writing ASCII PPM/PGM file


""" ╔══════════╗
    ║ list2pnm ║
    ╚══════════╝ """


def list2pnm(out_filename: str, list_3d: list[list[list[int]]], maxcolors: int, bin: bool = True) -> None:
    """Write PNM file using either ``list2pnmbin`` or ``list2pnmascii`` depending on ``bin`` switch.

    :param str out_filename: name of the PNM file to be written;
    :param list_3d: image as list (image) of lists (rows) of lists (pixels)
    of ints (channels);
    :type list_3d: list[list[list[int]]]
    :param int maxcolors: number of colors per channel for current image,
    either 255, or 65535;
    :param bool bin: whether written file will be binary or ASCII.
    :return: None

    """

    if bin:
        list2pnmbin(out_filename, list_3d, maxcolors)
    else:
        list2pnmascii(out_filename, list_3d, maxcolors)

    return None


# ↑ End of 'list2pnm' switch function writing any type of PPM/PGM file


""" ╔════════════════════╗
    ║ Create empty image ║
    ╚════════════════════╝ """


def create_image(X: int, Y: int, Z: int) -> list[list[list[int]]]:
    """Create 3D nested list of X * Y * Z size filled with zeroes."""

    new_image = [[[0 for z in range(Z)] for x in range(X)] for y in range(Y)]

    return new_image


# ↑ End of 'create_image' empty nested 3D list creation

# ↓ Dummy stub for standalone execution attempt
if __name__ == '__main__':
    print('Module to be imported, not run as standalone.')
    need_help = input('Would you like to read some help (y/n)?')
    if need_help.startswith(('y', 'Y')):
        import pnmlpnm

        help(pnmlpnm)
