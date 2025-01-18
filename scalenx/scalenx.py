#!/usr/bin/env python3

"""Module contain Scale2x and Scale3x image rescaling functions.

Overview
----------

- ``scalenx.scale2x``   - Scale2x aka AdvMAME2x image scaling up two times.

- ``scalenx.scale3x``   - Scale3x aka AdvMAME3x image scaling up three times.

Installation
--------------

Simply put module into your program folder.

Usage
-------

After ``import scalenx``, use something like:

``ScaledImage = scalenx.scale3x(SourceImage)``

where both ``Image`` are lists. Note that ``Image`` X and Y sized are determined automatically, Z not used and remains unchanged.


Copyright and redistribution
-----------------------------

Python implementation developed by Ilya Razmanov (https://dnyarri.github.io/), (hereinafter referred to as "the Developer"), based on brief algorithm description by Andrea Mazzoleni (https://www.scale2x.it/) (hereinafter referred to as "the Inventor").

May be freely used, included and modified anywhere by anyone. In case of useful modifications sharing it with the Developer is almost obligatory.

History:
----------

2024.02.24  Release as shared module, versioning changed to YYYY.MM.DD.

2024.05.14  Arguments and return format changed. Incompatible with previous versions!

2024.07.03  Small improvements, one more retest with new test corpse, as you were, corpus.

2024.10.01  Internal restructure, imports change, maintenance release.

2024.11.24  Improved documentation.

2025.01.15  Substantial change in "if" tree. Some appends replaced with extends. Scale2x boost ca. 12%, Scale3x ca. 15%.

"""

__author__ = 'Ilya Razmanov'
__copyright__ = '(c) 2024-2025 Ilya Razmanov'
__credits__ = ['Ilya Razmanov', 'Andrea Mazzoleni']
__license__ = 'unlicense'
__version__ = '2025.01.15'
__maintainer__ = 'Ilya Razmanov'
__email__ = 'ilyarazmanov@gmail.com'
__status__ = 'Production'

""" ╔════════════════════════════════════════════╗
    ║ Scaling image nested list to 2x image list ║
    ╚════════════════════════════════════════════╝ """


def scale2x(image3d: list[list[list[int]]]) -> list[list[list[int]]]:
    """Scale2x image rescale
    -

    ``EPXImage = scale2x(image3d)``

    Takes ``image3d`` as 3D nested list (image) of lists (rows) of lists (pixels) of int (channel values), and performs Scale2x rescaling, returning scaled EPXImage of similar structure.

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
                ┌───┬───┬───┐
                │   │ A │   │
                ├───┼───┼───┤
                │ C │ E │ B │
                ├───┼───┼───┤
                │   │ D │   │
                └───┴───┴───┘
            """

            E = image3d[y][x]
            A = image3d[max(y - 1, 0)][x]
            B = image3d[y][min(x + 1, X - 1)]
            C = image3d[y][max(x - 1, 0)]
            D = image3d[min(y + 1, Y - 1)][x]

            """ Result
                ┌────┬────┐
                │ r1 │ r2 │
                ├────┼────┤
                │ r3 │ r4 │
                └────┴────┘
            """

            r1 = r2 = r3 = r4 = E

            if A != D and C != B:
                if A == C:
                    r1 = C
                if A == B:
                    r2 = B
                if D == C:
                    r3 = C
                if D == B:
                    r4 = B

            RowRez.extend([r1, r2])
            RowDvo.extend([r3, r4])

        EPXImage.append(RowRez)
        EPXImage.append(RowDvo)

    return EPXImage  # rescaling two times finished


""" ╔════════════════════════════════════════════╗
    ║ Scaling image nested list to 3x image list ║
    ╚════════════════════════════════════════════╝ """


def scale3x(image3d: list[list[list[int]]]) -> list[list[list[int]]]:
    """Scale3x image rescale
    -

    ``EPXImage = scale3x(image3d)``

    Takes ``image3d`` as 3D nested list (image) of lists (rows) of lists (pixels) of int (channel values), and performs Scale3x rescaling, returning scaled EPXImage of similar structure.

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
                ┌───┬───┬───┐
                │ A │ B │ C │
                ├───┼───┼───┤
                │ D │ E │ F │
                ├───┼───┼───┤
                │ G │ H │ I │
                └───┴───┴───┘
            """

            E = image3d[y][x]  # E is a center of 3x3 square

            A = image3d[max(y - 1, 0)][max(x - 1, 0)]
            B = image3d[max(y - 1, 0)][x]
            C = image3d[max(y - 1, 0)][min(x + 1, X - 1)]

            D = image3d[y][max(x - 1, 0)]
            # central pixel E = image3d[y][x] retrieved already
            F = image3d[y][min(x + 1, X - 1)]

            G = image3d[min(y + 1, Y - 1)][max(x - 1, 0)]
            H = image3d[min(y + 1, Y - 1)][x]
            I = image3d[min(y + 1, Y - 1)][min(x + 1, X - 1)]

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

            if B != H and D != F:
                if D == B:
                    r1 = D
                if (D == B and E != C) or (B == F and E != A):
                    r2 = B
                if B == F:
                    r3 = F
                if (D == B and E != G) or (D == H and E != A):
                    r4 = D
                # central pixel r5 = E set already
                if (B == F and E != I) or (H == F and E != C):
                    r6 = F
                if D == H:
                    r7 = D
                if (D == H and E != I) or (H == F and E != G):
                    r8 = H
                if H == F:
                    r9 = F

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
