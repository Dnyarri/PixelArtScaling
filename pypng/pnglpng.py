#!/usr/bin/env python3

"""Joint between PyPNG module and 3D nested list data structures.

Overview
---------

`pnglpng` (png-list-png) is a suitable joint between PyPNG and other Python programs, providing data conversion from/to used by PyPNG to/from understandable by ordinary average human.

- `png2list`: reading PNG file and returning all data.
- `list2png`: getting data and writing PNG file.
- `create_image`: creating empty nested 3D list for image representation.

Installation
-------------
Should be kept together with png.py module. See `import` for detail.

Usage
------
After `import pnglpng`, use something like:

    `X, Y, Z, maxcolors, list_3d, info = pnglpng.png2list(in_filename)`

for reading data from `in_filename` PNG, where:

- `X`, `Y`, `Z`   - image dimensions (int);
- `maxcolors` - number of colors per channel for current image (int);
- `list_3d`   - image pixel data as list(list(list(int)));
- `info`      - PNG chunks like resolution etc (dictionary);

and:

    `pnglpng.list2png(out_filename, list_3d, info)`

for writing data to `out_filename` PNG.

Copyright and redistribution
-----------------------------
Written by `Ilya Razmanov <https://dnyarri.github.io/>`_ to simplify working with PyPNG module.
May be freely used and redistributed.

Prerequisites and References
-----------------------------
`PyPNG download <https://gitlab.com/drj11/pypng>`_

`PyPNG docs <https://drj11.gitlab.io/pypng>`_

History
--------

24.07.25    Initial version.

24.07.26    Fixed missing Z autodetection for `info` generation.

24.10.01    Internal restructure, incompatible with previous version.

25.01.08    `list2png` - force rewrite more `info` parameters with those detected from 3D list;
force remove `palette` due to accumulating problems with images promoted to full color,
and `background` due to rare problems with changing color mode.

25.02.06    PNG `write_array` replaced with `write` to replace flattening to 1D list
with 2D rows generator, thus reducing RAM usage and eliminating memory errors on huge files.
Fixed missing `maxcolors` for 1-bit images.

25.03.01    Improved robustness, `list2png` is skipping any possible input channel above 4-th.

"""

__author__ = 'Ilya Razmanov'
__copyright__ = '(c) 2024-2025 Ilya Razmanov'
__credits__ = 'Ilya Razmanov'
__license__ = 'unlicense'
__version__ = '25.03.01'
__maintainer__ = 'Ilya Razmanov'
__email__ = 'ilyarazmanov@gmail.com'
__status__ = 'Production'

from . import png  # PNG I/O: PyPNG from: https://gitlab.com/drj11/pypng

""" ┌──────────┐
    │ png2list │
    └──────────┘ """


def png2list(in_filename: str) -> tuple[int, int, int, int, list[list[list[int]]], dict]:
    """Take PNG filename and return PNG data in a human-friendly form.

    Usage
    ------

    `X, Y, Z, maxcolors, list_3d, info = pnglpng.png2list(in_filename)`

    Takes PNG filename `in_filename` and returns the following tuple:

    - `X`, `Y`, `Z`: PNG image dimensions (int);
    - `maxcolors`: number of colors per channel for current image (int),
    either 255 or 65535, for 8 bpc and 16 bpc PNG respectively;
    - `list_3d`: Y * X * Z list (image) of lists (rows) of lists (pixels) of ints (channels), from PNG iDAT;
    - `info`: dictionary from PNG chunks like resolution etc. as they are accessible by PyPNG.

    """

    source = png.Reader(in_filename)

    X, Y, pixels, info = source.asDirect()  # Opening image, iDAT comes to "pixels"

    Z = info['planes']  # Channels number
    if info['bitdepth'] == 1:
        maxcolors = 1  # Maximal value of a color for 1-bit / channel
    if info['bitdepth'] == 8:
        maxcolors = 255  # Maximal value of a color for 8-bit / channel
    if info['bitdepth'] == 16:
        maxcolors = 65535  # Maximal value of a color for 16-bit / channel

    imagedata = tuple(pixels)  # Freezes tuple of bytes or whatever "pixels" generator returns

    # Forcedly create 3D list of int out of "imagedata" tuple of hell knows what
    list_3d = [
                [
                    [
                        int((imagedata[y])[(x * Z) + z]) for z in range(Z)
                    ] for x in range(X)
                ] for y in range(Y)
            ]

    return (X, Y, Z, maxcolors, list_3d, info)


""" ┌──────────┐
    │ list2png │
    └──────────┘ """


def list2png(out_filename: str, list_3d: list[list[list[int]]], info: dict) -> None:
    """Take filename and image data, and create PNG file.

    Usage
    ------

    `pnglpng.list2png(out_filename, list_3d, info)`

    Takes data described below and writes PNG file `out_filename` out of it:

    - `list_3d`: Y * X * Z list (image) of lists (rows) of lists (pixels) of ints (channels);
    - `info`: dictionary, chunks like resolution etc. as you want them to be present in PNG.

    """

    # Determining list dimensions
    Y = len(list_3d)
    X = len(list_3d[0])
    Z = len(list_3d[0][0])

    Z = min(Z, 4)  # Skipping any possible list channels above 4-th.

    # Overwriting "info" properties with ones determined from the list
    info['size'] = (X, Y)
    info['planes'] = Z
    if 'palette' in info:
        del info['palette']  # images get promoted to smooth color when editing
    if 'background' in info:
        # as image tend to get promoted to smooth color when editing,
        # background must either be rebuilt to match channels structure every time,
        # or be deleted.
        # info['background'] = (0,) * (Z - 1 + Z % 2)  # black for any color mode
        del info['background']  # Destroy is better than rebuild ;-)
    if (Z % 2) == 1:
        info['alpha'] = False
    else:
        info['alpha'] = True
    if Z < 3:
        info['greyscale'] = True
    else:
        info['greyscale'] = False

    # Flattening 3D list to 2D list of rows for PNG `.write` method
    def flatten_2d(list_3d: list[list[list[int]]]):
        """Flatten `list_3d` to 2D list of rows, yield generator."""

        yield from (
                        [list_3d[y][x][z]
                            for x in range(X)
                                for z in range(Z)
                        ] for y in range(Y)
                    ) 

    # Writing PNG with `.write` method (row by row), using `flatten_2d` generator to save memory
    writer = png.Writer(X, Y, **info)
    with open(out_filename, 'wb') as result_png:
        writer.write(result_png, flatten_2d(list_3d))

    return None


""" ┌────────────────────┐
    │ Create empty image │
    └────────────────────┘ """

def create_image(X: int, Y: int, Z: int) -> list[list[list[int]]]:
    """Create empty 3D nested list of X * Y * Z size."""

    new_image = [
                    [
                        [0 for z in range(Z)] for x in range(X)
                    ] for y in range(Y)
                ]

    return new_image


# --------------------------------------------------------------

if __name__ == '__main__':
    print('Module to be imported, not run as standalone')
