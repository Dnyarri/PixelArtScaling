"""Multithreading patch for ``list2bin`` function of `PyPNM`_.

.. _PyPNM: https://pypi.org/project/PyPNM/"""

import array
from concurrent.futures import ThreadPoolExecutor


def list2bin(list_3d, maxcolors, show_chessboard=False):
    """Convert nested image data list to PGM P5 or PPM P6 bytes in memory.

    :param list_3d: image as list (image) of lists (rows) of lists (pixels)
        of ints (channels);
    :type list_3d: list[list[list[int]]]
    :param int maxcolors: maximal color value per channel for current image,
        either 255, or 65535;
    :param bool show_chessboard: if set ``True`` and alpha channel exist,
        render preview against chessboard, otherwise skip alpha;
    :return: PNM-like object in memory.
    :rtype: bytes

    """

    # ↓ Image X, Y, Z sizes
    Y, X, Z = (len(list_3d), len(list_3d[0]), len(list_3d[0][0]))

    def _chess(x, y):
        """Chessboard pattern, size and color match Photoshop 7.0.

        Photoshop chess pattern preset parameters:
        - Small: 4 px | Medium: 8 px | Large: 16 px;
        - Light: (0.8, 1.0) | Medium: (0.4, 0.6) | Dark: (0.2, 0.4) of ``maxcolors``.

        """

        if X < 65 or Y < 65:
            chess_size = 4
        elif X > 512 or Y > 512:
            chess_size = 16
        else:
            chess_size = 8
        return int(maxcolors * 0.8) if ((y // chess_size) % 2) == ((x // chess_size) % 2) else maxcolors

    magic = 'P5' if Z < 3 else 'P6'  # PGM or PPM header

    if Z == 3 or Z == 1:  # No alpha
        Z_READ = Z  # Number of channels if source has no alpha

        def _row(y):
            """Flatten channels in a pixel row, and convert to bytearray."""
            list_2d = [list_3d[y][x][z] for x in range(X) for z in range(Z_READ)]
            # ↑ NOTE: List seem to work faster than generator.
            if maxcolors < 256:
                return array.array('B', list_2d)
            else:
                array_2d = array.array('H', list_2d)
                array_2d.byteswap()
                return array_2d
    else:  # Yes alpha
        Z_READ = min(Z, 4) - 1  # Number of channels without alpha
        if show_chessboard:

            def _row(y):
                """Add chessboard to each channel, flatten channels in a pixel row,
                and convert to bytearray."""
                list_2d = [(((list_3d[y][x][z] * list_3d[y][x][Z_READ]) + (_chess(x, y) * (maxcolors - list_3d[y][x][Z_READ]))) // maxcolors) for x in range(X) for z in range(Z_READ)]
                if maxcolors < 256:
                    return array.array('B', list_2d)
                else:
                    array_2d = array.array('H', list_2d)
                    array_2d.byteswap()
                    return array_2d
        else:

            def _row(y):
                """Flatten channels in a pixel row, and convert to bytearray."""
                list_2d = [list_3d[y][x][z] for x in range(X) for z in range(Z_READ)]
                if maxcolors < 256:
                    return array.array('B', list_2d)
                else:
                    array_2d = array.array('H', list_2d)
                    array_2d.byteswap()
                    return array_2d

    """ ╒═ Running and merging generators together ═══════╕
        │ Single-threaded analog would be                 │
        │ content = b''.join([_row(y) for y in range(Y)]) │
        ╰─────────────────────────────────────────────────╯ """
    with ThreadPoolExecutor() as row_executor:
        merge = row_executor.map(_row, range(Y))

    content = b''.join(merge)

    header = '{file_type}\n{width} {height}\n{colors}\n'.format(file_type=magic, width=X, height=Y, colors=maxcolors)  # noqa: UP032
    return b''.join((header.encode('ascii'), content))
