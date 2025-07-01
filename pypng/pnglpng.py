#!/usr/bin/env python3

"""PNG-list-PNG joint between PyPNG module and 3D nested list data structures.
-------------------------------------------------------------------------------

Overview
---------

`pnglpng` (png-list-png) is a suitable joint between `PyPNG<https://gitlab.com/drj11/pypng>`_
and other Python programs, providing data conversion from/to used by PyPNG
to/from understandable by ordinary average human.

Functions included are:

- `png2list`: reading PNG file and returning all data;
- `list2png`: getting data and writing PNG file;
- `create_image`: creating empty nested 3D list for image representation.

Installation
-------------

Should be kept together with png.py module. See `import` for detail.

Usage
------

After `import pnglpng`, use something like:

    `X, Y, Z, maxcolors, list_3d, info = pnglpng.png2list(in_filename)`

for reading data from `in_filename` PNG, where:

- `X`, `Y`, `Z` - image dimensions (int);
- `maxcolors`   - number of colors per channel for current image (int);
- `list_3d`     - image pixel data as list(list(list(int)));
- `info`        - PNG chunks like resolution etc (dictionary);

and:

    `pnglpng.list2png(out_filename, list_3d, info)`

for writing data to `out_filename` PNG.

Prerequisites and References
-----------------------------

1. `PyPNG download <https://gitlab.com/drj11/pypng>`_
2. `PyPNG docs <https://drj11.gitlab.io/pypng>`_

"""

__author__ = 'Ilya Razmanov'
__copyright__ = '(c) 2024-2025 Ilya Razmanov'
__credits__ = 'Ilya Razmanov'
__license__ = 'unlicense'
__version__ = '25.07.01'
__maintainer__ = 'Ilya Razmanov'
__email__ = 'ilyarazmanov@gmail.com'
__status__ = 'Production'

from . import png  # PNG I/O: PyPNG from: https://gitlab.com/drj11/pypng

""" ┌──────────┐
    │ png2list │
    └──────────┘ """


def png2list(in_filename: str) -> tuple[int, int, int, int, list[list[list[int]]], dict[str, int | bool | tuple | list[tuple]]]:
    """Take PNG filename and return PNG data in a human-friendly form.

    Usage:

        `X, Y, Z, maxcolors, list_3d, info = pnglpng.png2list(in_filename)`

    Take PNG filename `in_filename` and return the following tuple:

        - `X`, `Y`, `Z`: PNG image dimensions (int);
        - `maxcolors`: number of colors per channel for current image (int),
        either 1, or 255, or 65535, for 1 bpc, 8 bpc and 16 bpc PNG respectively;
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


def list2png(out_filename: str, list_3d: list[list[list[int]]], info: dict[str, int | bool | tuple | list[tuple]]) -> None:
    """Take filename and image data, and create PNG file.

    Usage:

        `pnglpng.list2png(out_filename, list_3d, info)`

    Take data described below and write PNG file `out_filename` out of it:

        - `list_3d`: Y * X * Z list (image) of lists (rows) of lists (pixels) of ints (channels);
        - `info`: dictionary, chunks like resolution etc. as you want them to be present in PNG.

    Note that `X`, `Y` and `Z` detected from the list structure override those set in `info`.

    """

    # Determining list dimensions
    Y = len(list_3d)
    X = len(list_3d[0])
    Z = len(list_3d[0][0])
    # Ignoring any possible list channels above 4-th.
    Z = min(Z, 4)

    # Overwriting "info" properties with ones determined from the list.
    # Necessary when image is edited.
    info['size'] = (X, Y)
    info['planes'] = Z
    if 'palette' in info:
        del info['palette']  # images get promoted to smooth color when editing.
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
    """Create zero-filled 3D nested list of X * Y * Z size."""

    new_image = [
                    [
                        [0 for z in range(Z)] for x in range(X)
                    ] for y in range(Y)
                ]

    return new_image


# --------------------------------------------------------------

if __name__ == '__main__':
    print('Module to be imported, not run as standalone')
