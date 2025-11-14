#!/usr/bin/env python3

"""
============
PNG-list-PNG
============
--------------------------------------
Joint between PyPNG and other programs
--------------------------------------

Overview
---------

**pnglpng** (png-list-png) is a suitable joint between `PyPNG`_
and other Python programs, providing data conversion from/to used by PyPNG
to/from understandable by ordinary average human.

Functions included are:

- `png2list`: reading PNG file and returning all data;
- `list2png`: getting data and writing PNG file;
- `create_image`: creating empty nested 3D list for image representation.

Installation
-------------

Should be kept together with ``png.py`` module. See ``import`` for detail.

Usage
------

After ``import pnglpng``, use something like::

    X, Y, Z, maxcolors, list_3d, info = pnglpng.png2list(in_filename)

where:

:param str in_filename: file name;
:return X: image width, pixels;
:return Y: image height, pixels;
:return Z: number of image channels (1..4);
:return maxcolors: number of colors per channel for current image;
:return list_3d: image pixel data as list(list(list(int)));
:return info: PNG chunks like resolution etc (dictionary);

and ::

    pnglpng.list2png(out_filename, list_3d, info)

for writing data as listed above to ``out_filename`` PNG.

Prerequisites and References
----------------------------

1. `PyPNG`_
2. `PyPNG docs`_

.. _PyPNG: https://gitlab.com/drj11/pypng

.. _PyPNG docs: https://drj11.gitlab.io/pypng

"""

__author__ = 'Ilya Razmanov'
__copyright__ = '(c) 2024-2025 Ilya Razmanov'
__credits__ = 'Ilya Razmanov'
__license__ = 'unlicense'
__version__ = '25.11.11.11'
__maintainer__ = 'Ilya Razmanov'
__email__ = 'ilyarazmanov@gmail.com'
__status__ = 'Production'

from . import png

""" ┌──────────┐
    │ png2list │
    └──────────┘ """


def png2list(in_filename: str) -> tuple[int, int, int, int, list[list[list[int]]], dict[str, int | bool | tuple | list[tuple]]]:
    """Take PNG filename and return PNG data in a human-friendly form.

    .. function:: png2list(in_filename)
    :param str in_filename: input file name;
    :return X, Y, Z, maxcolors, list_3d, info: tuple, consisting of:

    - ``X, Y, Z``: PNG image dimensions (int);
    - ``maxcolors``: number of colors per channel for current image (int), either 1, or 255, or 65535, for 1 bpc, 8 bpc and 16 bpc PNG respectively;
    - ``list_3d``: Y * X * Z list (image) of lists (rows) of lists (pixels) of ints (channels), from PNG iDAT;
    - ``info``: dictionary from PNG chunks like resolution etc. as they are accessible by PyPNG.

    """

    source = png.Reader(in_filename)

    # ↓ Opening image, iDAT comes to "pixels" generator
    X, Y, pixels, info = source.asDirect()

    Z = info['planes']  # Channels number
    if info['bitdepth'] == 1:
        maxcolors = 1  # Maximal value of a color for 1-bit / channel
    elif info['bitdepth'] == 8:
        maxcolors = 255  # Maximal value of a color for 8-bit / channel
    elif info['bitdepth'] == 16:
        maxcolors = 65535  # Maximal value of a color for 16-bit / channel

    # ↓ Freezing tuple of bytes or whatever "pixels" generator returns
    imagedata = tuple(pixels)

    # ↓ Forcedly create 3D list of int out of "imagedata" tuple of hell knows what
    list_3d = [[[int((imagedata[y])[(x * Z) + z]) for z in range(Z)] for x in range(X)] for y in range(Y)]

    return (X, Y, Z, maxcolors, list_3d, info)


""" ┌──────────┐
    │ list2png │
    └──────────┘ """


def list2png(out_filename: str, list_3d: list[list[list[int]]], info: dict[str, int | bool | tuple | list[tuple]]) -> None:
    """Take filename and image data, and create PNG file.

    .. function:: list2png(out_filename, list_3d, info)
    :param list_3d: Y * X * Z list (image) of lists (rows) of lists (pixels) of ints (channels);
    :param info: dictionary, chunks like resolution etc. as you want them to be present in PNG;
    :param str out_filename: output PNG file name (str).

    .. note:: ``X``, ``Y`` and ``Z`` detected from the list structure override those set in ``info``.
    .. warning:: Correct ``info['bitdepth']`` is **critical** because it cannot be detected from the list structure.

    """

    # ↓ Determining list dimensions
    Y = len(list_3d)
    X = len(list_3d[0])
    Z = len(list_3d[0][0])
    # ↓ Ignoring any possible list channels above 4-th.
    Z = min(Z, 4)

    # ↓ Overwriting "info" properties with ones determined from the list.
    #   Necessary when image is edited.
    info['size'] = (X, Y)
    info['planes'] = Z
    if 'palette' in info:
        del info['palette']  # images get promoted to smooth color when editing.
    if 'background' in info:
        # ↓ as image tend to get promoted to smooth color when editing,
        #   background must either be rebuilt to match channels structure every time,
        #   or be deleted.
        #   info['background'] = (0,) * (Z - 1 + Z % 2)  # black for any color mode
        del info['background']  # Destroy is better than rebuild ;-)
    if (Z % 2) == 1:
        info['alpha'] = False
    else:
        info['alpha'] = True
    if Z < 3:
        info['greyscale'] = True
    else:
        info['greyscale'] = False

    # ↓ Flattening 3D list to 2D list of rows for PNG `.write` method
    def flatten_2d(list_3d: list[list[list[int]]]):
        """Flatten `list_3d` to 2D list of rows, yield generator."""

        yield from ([list_3d[y][x][z] for x in range(X) for z in range(Z)] for y in range(Y))

    # ↓ Writing PNG with `.write` method (row by row),
    #   using `flatten_2d` generator to save memory
    writer = png.Writer(X, Y, **info)
    with open(out_filename, 'wb') as result_png:
        writer.write(result_png, flatten_2d(list_3d))

    return None


""" ┌────────────────────┐
    │ Create empty image │
    └────────────────────┘ """


def create_image(X: int, Y: int, Z: int) -> list[list[list[int]]]:
    """Create zero-filled 3D nested list of X * Y * Z size."""

    new_image = [[[0 for z in range(Z)] for x in range(X)] for y in range(Y)]

    return new_image


# ↓ Dummy stub for standalone execution attempt
if __name__ == '__main__':
    print('Module to be imported, not run as standalone')
