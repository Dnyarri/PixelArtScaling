#!/usr/bin/env python3

"""Module contain Scale2xSFX and Scale3xSFX image rescaling functions.

Overview
----------

- `scalenxsfx.scale2x`: Scale2xSFX image scaling two times.

- `scalenxsfx.scale3x`: Scale3xSFX image scaling three times.

Installation
--------------

Either use `pip scalenx` or simply put `scalenx` module into your program folder, then

`from scalenx import scalenxsfx`

Usage
-------

Use something like:

`ScaledImage = scalenxsfx.scale3x(SourceImage)`

where both `Image` are list[list[list[int]]]. Note that `Image` X and Y sized are determined automatically, Z not used and remains unchanged.


Copyright and redistribution
-----------------------------

Python implementation developed by Ilya Razmanov (https://dnyarri.github.io/), (hereinafter referred to as "the Developer"), based on brief algorithm description at:

https://web.archive.org/web/20160527015550/https://libretro.com/forums/archive/index.php?t-1655.html

Real names of participants unknown, therefore due credits unavailable.

Current implementation may be freely used, included and modified anywhere by anyone. In case of useful modifications sharing it with the Developer is almost obligatory.

History:
----------

2025.01.16  Initial implementation of ScaleNxSFX.

"""

__author__ = 'Ilya Razmanov'
__copyright__ = '(c) 2025 Ilya Razmanov'
__credits__ = 'Ilya Razmanov'
__license__ = 'unlicense'
__version__ = '2025.01.19'
__maintainer__ = 'Ilya Razmanov'
__email__ = 'ilyarazmanov@gmail.com'
__status__ = 'Production'

""" ╔════════════════════════════════════════════╗
    ║ Scaling image nested list to 2x image list ║
    ╚════════════════════════════════════════════╝ """


def scale2x(image3d: list[list[list[int]]]) -> list[list[list[int]]]:
    """Scale2xSFX image rescale
    -

    `EPXImage = scalenxsfx.scale2x(image3d)`

    Takes `image3d` as 3D nested list (image) of lists (rows) of lists (pixels) of int (channel values), and performs Scale2xSFX rescaling, returning scaled EPXImage of similar structure.

    """

    # determining image size from list
    Y = len(image3d)
    X = len(image3d[0])

    # building new list
    EPXImage = list()

    for y in range(0, Y, 1):
        RowRez = list()
        RowDvo = list()
        for x in range(0, X, 1):
            """ Source around default pixel E
                ┌───┬───┬───┬───┬───┐
                │   │   │ J │   │   │
                ├───┼───┼───┼───┼───┤
                │   │ A │ B │ C │   │
                ├───┼───┼───┼───┼───┤
                │ K │ D │ E │ F │ L │
                ├───┼───┼───┼───┼───┤
                │   │ G │ H │ I │   │
                ├───┼───┼───┼───┼───┤
                │   │   │ M │   │   │
                └───┴───┴───┴───┴───┘
            """

            A = image3d[max(y - 1, 0)][max(x - 1, 0)]
            B = image3d[max(y - 1, 0)][x]
            C = image3d[max(y - 1, 0)][min(x + 1, X - 1)]
            D = image3d[y][max(x - 1, 0)]
            E = image3d[y][x]  # central pixel
            F = image3d[y][min(x + 1, X - 1)]
            G = image3d[min(y + 1, Y - 1)][max(x - 1, 0)]
            H = image3d[min(y + 1, Y - 1)][x]
            I = image3d[min(y + 1, Y - 1)][min(x + 1, X - 1)]
            J = image3d[max(y - 2, 0)][x]
            M = image3d[min(y + 2, Y - 1)][x]
            K = image3d[y][max(x - 2, 0)]
            L = image3d[y][min(x + 2, X - 1)]

            """ Result
                ┌────┬────┐
                │ r1 │ r2 │
                ├────┼────┤
                │ r3 │ r4 │
                └────┴────┘
            """

            r1 = r2 = r3 = r4 = E

            if (B == D and B != F and D != H and (E != A or E == C or E == G or A == J or A == K)):
                r1 = B
            if (B == F and B != D and F != H and (E != C or E == A or E == I or C == J or C == L)):
                r2 = B
            if (H == D and B != D and F != H and (E != G or E == A or E == I or G == K or G == M)):
                r3 = H
            if (H == F and B != F and D != H and (E != I or E == C or E == G or I == L or I == M)):
                r4 = H

            RowRez.extend([r1, r2])
            RowDvo.extend([r3, r4])

        EPXImage.append(RowRez)
        EPXImage.append(RowDvo)

    return EPXImage  # rescaling two times finished


""" ╔════════════════════════════════════════════╗
    ║ Scaling image nested list to 3x image list ║
    ╚════════════════════════════════════════════╝ """


def scale3x(image3d: list[list[list[int]]]) -> list[list[list[int]]]:
    """Scale3xSFX image rescale
    -

    `EPXImage = scalenxsfx.scale3x(image3d)`

    Takes `image3d` as 3D nested list (image) of lists (rows) of lists (pixels) of int (channel values), and performs Scale3xSFX rescaling, returning scaled EPXImage of similar structure.

    """

    # determining image size from list
    Y = len(image3d)
    X = len(image3d[0])

    # building new list
    EPXImage = list()

    for y in range(0, Y, 1):
        RowRez = list()
        RowDvo = list()
        RowTre = list()
        for x in range(0, X, 1):
            """ Source around default pixel E
                ┌───┬───┬───┬───┬───┐
                │   │   │ J │   │   │
                ├───┼───┼───┼───┼───┤
                │   │ A │ B │ C │   │
                ├───┼───┼───┼───┼───┤
                │ K │ D │ E │ F │ L │
                ├───┼───┼───┼───┼───┤
                │   │ G │ H │ I │   │
                ├───┼───┼───┼───┼───┤
                │   │   │ M │   │   │
                └───┴───┴───┴───┴───┘
            """

            A = image3d[max(y - 1, 0)][max(x - 1, 0)]
            B = image3d[max(y - 1, 0)][x]
            C = image3d[max(y - 1, 0)][min(x + 1, X - 1)]
            D = image3d[y][max(x - 1, 0)]
            E = image3d[y][x]  # central pixel
            F = image3d[y][min(x + 1, X - 1)]
            G = image3d[min(y + 1, Y - 1)][max(x - 1, 0)]
            H = image3d[min(y + 1, Y - 1)][x]
            I = image3d[min(y + 1, Y - 1)][min(x + 1, X - 1)]
            J = image3d[max(y - 2, 0)][x]
            M = image3d[min(y + 2, Y - 1)][x]
            K = image3d[y][max(x - 2, 0)]
            L = image3d[y][min(x + 2, X - 1)]

            """ Result
                ┌────┬────┬────┐
                │ r1 │ r2 │ r3 │
                ├────┼────┼────┤
                │ r4 │ r5 │ r6 │
                ├────┼────┼────┤
                │ r7 │ r8 │ r9 │
                └────┴────┴────┘
            """
            r1 = r2 = r3 = r4 = r5 = r6 = r7 = r8 = r9 = E

            if (B == D and B != F and D != H and (E != A or E == C or E == G or A == J or A == K)) or (B == D and C == E and C != J and A != E) or (B == D and E == G and A != E and G != K):
                r1 = B
            if (B == F and B != D and F != H and (E != C or E == A or E == I or C == J or C == L)) or (B == F and A == E and A != J and C != E) or (B == F and E == I and C != E and I != L):
                r3 = B
            if (H == D and B != D and F != H and (E != G or E == A or E == I or G == K or G == M)) or (D == H and A == E and A != K and E != G) or (D == H and E == I and E != G and I != M):
                r7 = H
            if (H == F and B != F and D != H and (E != I or E == C or E == G or I == L or I == M)) or (F == H and C == E and C != L and E != I) or (F == H and E == G and E != I and G != M):
                r9 = H

            if (B == D and B != F and D != H and (E != A or E == C or E == G or A == J or A == K) and E != C) or (B == F and B != D and F != H and (E != C or E == A or E == I or C == J or C == L) and E != A):
                r2 = B
            if (B == D and B != F and D != H and (E != A or E == C or E == G or A == J or A == K) and E != G) or (D == H and B != D and F != H and (E != G or E == A or E == I or G == K or G == M) and E != A):
                r4 = D
            if (F == H and B != F and D != H and (E != I or E == C or E == G or I == L or I == M) and E != C) or (B == F and B != D and F != H and (E != C or E == A or E == I or C == J or C == L) and E != I):
                r6 = F
            if (F == H and B != F and D != H and (E != I or E == C or E == G or I == L or I == M) and E != G) or (D == H and B != D and F != H and (E != G or E == A or E == I or G == K or G == M) and E != I):
                r8 = H

            RowRez.extend([r1, r2, r3])
            RowDvo.extend([r4, r5, r6])
            RowTre.extend([r7, r8, r9])

        EPXImage.append(RowRez)
        EPXImage.append(RowDvo)
        EPXImage.append(RowTre)

    return EPXImage  # rescaling three times finished


# --------------------------------------------------------------


if __name__ == '__main__':
    print('Module to be imported, not run as standalone')
