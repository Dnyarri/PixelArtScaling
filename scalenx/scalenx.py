#!/usr/bin/env python3

"""Module contain Scale2x and Scale3x image rescaling functions.

Overview
---------

- `scalenx.scale2x`: Scale2x aka AdvMAME2x image scaling up two times
without introducing intermediate colors (blur).

- `scalenx.scale3x`: Scale3x aka AdvMAME3x image scaling up three times
without introducing intermediate colors (blur).

Installation
-------------

Either use `pip scalenx` or simply put `scalenx` module folder into your main program folder, then:

    `from scalenx import scalenx`

Usage
------

Syntaxis example:

    `scaled_image = scalenx.scale3x(source_image)`

where both `image` are list[list[list[int]]].
Note that `image` X and Y sized are determined automatically, Z not used and remains unchanged.


Copyright and redistribution
-----------------------------

Current Python implementation of ScaleNx developed by `Ilya Razmanov <https://dnyarri.github.io/>`_
(hereinafter referred to as "the Developer"), based on `brief algorithm description <https://www.scale2x.it/algorithm>`_
by `Andrea Mazzoleni <https://www.scale2x.it/>`_ (hereinafter referred to as "the Inventor").

Current implementation may be freely used, included and modified anywhere by anyone.
In case of useful modifications sharing it with the Developer is almost obligatory.

History
--------

2024.02.24  Release as shared module, versioning changed to YYYY.MM.DD.

2024.05.14  Arguments and return format changed. Incompatible with previous versions!

2024.07.03  Small improvements, one more retest with new test corpse, as you were, corpus.

2024.10.01  Internal restructure, imports change, maintenance release.

2024.11.24  Improved documentation.

2025.01.15  Conditional optimization. Some appends replaced with extends.

2025.02.01  FIR optimization. Speed gain, % of original: ca.15% 2x, ca. 50% 3x.

"""

__author__ = 'Ilya Razmanov'
__copyright__ = '(c) 2024-2025 Ilya Razmanov'
__credits__ = ['Ilya Razmanov', 'Andrea Mazzoleni']
__license__ = 'unlicense'
__version__ = '2025.03.01'
__maintainer__ = 'Ilya Razmanov'
__email__ = 'ilyarazmanov@gmail.com'
__status__ = 'Production'

""" ╔════════════════════════════════════════════╗
    ║ Scaling image nested list to 2x image list ║
    ╚════════════════════════════════════════════╝ """


def scale2x(image3d: list[list[list[int]]]) -> list[list[list[int]]]:
    """Scale2x image rescale
    -

        `scaled_image = scalenx.scale2x(image3d)`

    Takes `image3d` as 3D nested list (image) of lists (rows) of lists (pixels) of int (channel values),
    and performs Scale2x rescaling, returning scaled `scaled_image` of similar structure.

    """

    # determining source image size from list
    Y = len(image3d)
    X = len(image3d[0])

    # starting new image list
    scaled_image: list[list[list[int]]] = list()

    def _dva(A: list[int], B: list[int], C: list[int], D: list[int], E: list[int]):
        """Scale2x conditional tree function"""

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
        return r1, r2, r3, r4

    """ Source around default pixel E
        ┌───┬───┬───┐
        │   │ A │   │
        ├───┼───┼───┤
        │ C │ E │ B │
        ├───┼───┼───┤
        │   │ D │   │
        └───┴───┴───┘

        Result
        ┌────┬────┐
        │ r1 │ r2 │
        ├────┼────┤
        │ r3 │ r4 │
        └────┴────┘
    """
    for y in range(Y):
        """
            ┌───────────────────────┐
            │ First pixel in a row. │
            │ "Repeat edge" mode.   │
            └───────────────────────┘
        """
        A = image3d[max(y - 1, 0)][0]
        B = image3d[y][min(1, X - 1)]
        C = E = image3d[y][0]
        D = image3d[min(y + 1, Y - 1)][0]

        r1, r2, r3, r4 = _dva(A, B, C, D, E)

        row_rez = [r1, r2]
        row_dvo = [r3, r4]

        """
            ┌───────────────────────────────────────────┐
            │ Next pixels in a row (below).             │
            │ Reusing pixels from previous kernel.      │
            │ Only rightmost pixels are read from list. │
            └───────────────────────────────────────────┘
        """
        for x in range(1, X):
            C = E
            E = B
            A = image3d[max(y - 1, 0)][x]
            B = image3d[y][min(x + 1, X - 1)]
            D = image3d[min(y + 1, Y - 1)][x]

            r1, r2, r3, r4 = _dva(A, B, C, D, E)

            row_rez.extend((r1, r2))
            row_dvo.extend((r3, r4))

        scaled_image.append(row_rez)
        scaled_image.append(row_dvo)

    return scaled_image  # rescaling two times finished


""" ╔════════════════════════════════════════════╗
    ║ Scaling image nested list to 3x image list ║
    ╚════════════════════════════════════════════╝ """


def scale3x(image3d: list[list[list[int]]]) -> list[list[list[int]]]:
    """Scale3x image rescale
    -

        `scaled_image = scalenx.scale3x(image3d)`

    Takes `image3d` as 3D nested list (image) of lists (rows) of lists (pixels) of int (channel values),
    and performs Scale3x rescaling, returning scaled `scaled_image` of similar structure.

    """

    # determining source image size from list
    Y = len(image3d)
    X = len(image3d[0])

    # starting new image list
    scaled_image: list[list[list[int]]] = list()

    def _tri(A: list[int], B: list[int], C: list[int], D: list[int], E: list[int], F: list[int], G: list[int], H: list[int], I: list[int]):
        """Scale3x conditional tree function"""

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
        return r1, r2, r3, r4, r5, r6, r7, r8, r9

    """ Source around default pixel E
        ┌───┬───┬───┐
        │ A │ B │ C │
        ├───┼───┼───┤
        │ D │ E │ F │
        ├───┼───┼───┤
        │ G │ H │ I │
        └───┴───┴───┘

        Result
        ┌────┬────┬────┐
        │ r1 │ r2 │ r3 │
        ├────┼────┼────┤
        │ r4 │ r5 │ r6 │
        ├────┼────┼────┤
        │ r7 │ r8 │ r9 │
        └────┴────┴────┘
    """
    for y in range(Y):
        """
            ┌───────────────────────┐
            │ First pixel in a row. │
            │ "Repeat edge" mode.   │
            └───────────────────────┘
        """
        A = B = image3d[max(y - 1, 0)][0]
        C = image3d[max(y - 1, 0)][min(1, X - 1)]
        D = E = image3d[y][0]
        F = image3d[y][min(1, X - 1)]
        G = H = image3d[min(y + 1, Y - 1)][0]
        I = image3d[min(y + 1, Y - 1)][min(1, X - 1)]

        r1, r2, r3, r4, r5, r6, r7, r8, r9 = _tri(A, B, C, D, E, F, G, H, I)

        row_rez = [r1, r2, r3]
        row_dvo = [r4, r5, r6]
        row_tre = [r7, r8, r9]

        """
            ┌───────────────────────────────────────────┐
            │ Next pixels in a row (below).             │
            │ Reusing pixels from previous kernel.      │
            │ Only rightmost pixels are read from list. │
            └───────────────────────────────────────────┘
        """
        for x in range(1, X):
            A = B
            B = C
            C = image3d[max(y - 1, 0)][min(x + 1, X - 1)]

            D = E
            E = F
            F = image3d[y][min(x + 1, X - 1)]

            G = H
            H = I
            I = image3d[min(y + 1, Y - 1)][min(x + 1, X - 1)]

            r1, r2, r3, r4, r5, r6, r7, r8, r9 = _tri(A, B, C, D, E, F, G, H, I)

            row_rez.extend((r1, r2, r3))
            row_dvo.extend((r4, r5, r6))
            row_tre.extend((r7, r8, r9))

        scaled_image.append(row_rez)
        scaled_image.append(row_dvo)
        scaled_image.append(row_tre)

    return scaled_image  # rescaling three times finished


# --------------------------------------------------------------


if __name__ == '__main__':
    print('Module to be imported, not run as standalone')
