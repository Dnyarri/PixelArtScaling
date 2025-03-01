#!/usr/bin/env python3

"""Module contain Scale2xSFX and Scale3xSFX image rescaling functions.

Overview
---------

- `scalenxsfx.scale2x`: Scale2xSFX image scaling two times
without introducing intermediate colors (blur).

- `scalenxsfx.scale3x`: Scale3xSFX image scaling three times
without introducing intermediate colors (blur).

Installation
-------------

Either use `pip scalenx` or simply put `scalenx` module folder into your main program folder, then:

    `from scalenx import scalenxsfx`

Usage
------

Syntaxis example:

    `scaled_image = scalenxsfx.scale3x(source_image)`

Current Python implementation of ScaleNxSFX developed by `Ilya Razmanov <https://dnyarri.github.io/>`_
(hereinafter referred to as "the Developer"), based on `brief algorithm description<https://web.archive.org/web/20160527015550/https://libretro.com/forums/archive/index.php?t-1655.html>`_.
Real name of the author unknown, therefore due credits not given.

Current implementation may be freely used, included and modified anywhere by anyone.
In case of useful modifications sharing it with the Developer is almost obligatory.

History
--------

2025.01.16  Initial implementation of ScaleNxSFX.

2025.02.01  FIR and conditional optimization. Speed gain, % of original: ca.50% 2x, ca. 40% 3x.

"""

__author__ = 'Ilya Razmanov'
__copyright__ = '(c) 2025 Ilya Razmanov'
__credits__ = 'Ilya Razmanov'
__license__ = 'unlicense'
__version__ = '2025.03.01'
__maintainer__ = 'Ilya Razmanov'
__email__ = 'ilyarazmanov@gmail.com'
__status__ = 'Production'

""" ╔════════════════════════════════════════════╗
    ║ Scaling image nested list to 2x image list ║
    ╚════════════════════════════════════════════╝ """


def scale2x(image3d: list[list[list[int]]]) -> list[list[list[int]]]:
    """Scale2xSFX image rescale
    -

        `scaled_image = scalenxsfx.scale2x(image3d)`

    Takes `image3d` as 3D nested list (image) of lists (rows) of lists (pixels) of int (channel values),
    and performs Scale2xSFX rescaling, returning scaled `scaled_image` of similar structure.

    """

    # determining source image size from list
    Y = len(image3d)
    X = len(image3d[0])

    # starting new image list
    scaled_image: list[list[list[int]]] = list()

    def _dva(A: list[int], B: list[int], C: list[int], D: list[int], E: list[int], F: list[int], G: list[int], H: list[int], I: list[int], J: list[int], K: list[int], L: list[int], M: list[int]):
        """Scale2xSFX conditional tree function"""

        r1 = r2 = r3 = r4 = E

        if B != F and D != H:
            if B == D and (A != E or C == E or E == G or A == J or A == K):
                r1 = B
            if H == F and (E != I or C == E or E == G or I == L or I == M):
                r4 = H
        if B != D and F != H:
            if B == F and (C != E or A == E or E == I or C == J or C == L):
                r2 = B
            if H == D and (E != G or A == E or E == I or G == K or G == M):
                r3 = H

        return r1, r2, r3, r4

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
        A = B = image3d[max(y - 1, 0)][0]
        C = image3d[max(y - 1, 0)][min(1, X - 1)]
        D = E = K = image3d[y][0]
        F = image3d[y][min(1, X - 1)]
        G = H = image3d[min(y + 1, Y - 1)][0]
        I = image3d[min(y + 1, Y - 1)][min(1, X - 1)]
        J = image3d[max(y - 2, 0)][0]
        M = image3d[min(y + 2, Y - 1)][0]
        L = image3d[y][min(2, X - 1)]

        r1, r2, r3, r4 = _dva(A, B, C, D, E, F, G, H, I, J, K, L, M)

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
            A = B
            B = C
            C = image3d[max(y - 1, 0)][min(x + 1, X - 1)]
            K = D
            D = E
            E = F
            F = L
            L = image3d[y][min(x + 2, X - 1)]
            G = H
            H = I
            I = image3d[min(y + 1, Y - 1)][min(x + 1, X - 1)]
            J = image3d[max(y - 2, 0)][x]
            M = image3d[min(y + 2, Y - 1)][x]

            r1, r2, r3, r4 = _dva(A, B, C, D, E, F, G, H, I, J, K, L, M)

            row_rez.extend((r1, r2))
            row_dvo.extend((r3, r4))

        scaled_image.append(row_rez)
        scaled_image.append(row_dvo)

    return scaled_image  # rescaling two times finished


""" ╔════════════════════════════════════════════╗
    ║ Scaling image nested list to 3x image list ║
    ╚════════════════════════════════════════════╝ """


def scale3x(image3d: list[list[list[int]]]) -> list[list[list[int]]]:
    """Scale3xSFX image rescale
    -

        `scaled_image = scalenxsfx.scale3x(image3d)`

    Takes `image3d` as 3D nested list (image) of lists (rows) of lists (pixels) of int (channel values),
    and performs Scale3xSFX rescaling, returning scaled `scaled_image` of similar structure.

    """

    # determining source image size from list
    Y = len(image3d)
    X = len(image3d[0])

    # starting new image list
    scaled_image: list[list[list[int]]] = list()

    def _tri(A: list[int], B: list[int], C: list[int], D: list[int], E: list[int], F: list[int], G: list[int], H: list[int], I: list[int], J: list[int], K: list[int], L: list[int], M: list[int]):
        """Scale3xSFX conditional tree function"""

        r1 = r2 = r3 = r4 = r5 = r6 = r7 = r8 = r9 = E

        if B == D:
            if C == E and C != J and A != E:
                r1 = B
            elif E == G and A != E and G != K:
                r1 = B
            if B != F and D != H:
                if A != E or C == E or E == G or A == J or A == K:
                    r1 = B
                if C != E and (A != E or C == E or E == G or A == J or A == K):
                    r2 = B
                if E != G and (A != E or C == E or E == G or A == J or A == K):
                    r4 = D

        if B == F:
            if A == E and A != J and C != E:
                r3 = B
            elif E == I and C != E and I != L:
                r3 = B
            if B != D and F != H:
                if C != E or A == E or E == I or C == J or C == L:
                    r3 = B
                if A != E and (C != E or A == E or E == I or C == J or C == L):
                    r2 = B
                if E != I and (C != E or A == E or E == I or C == J or C == L):
                    r6 = F

        if D == H:
            if A == E and A != K and E != G:
                r7 = H
            elif E == I and E != G and I != M:
                r7 = H
            if B != D and F != H:
                if E != G or A == E or E == I or G == K or G == M:
                    r7 = H
                if A != E and (E != G or A == E or E == I or G == K or G == M):
                    r4 = D
                if E != I and (E != G or A == E or E == I or G == K or G == M):
                    r8 = H

        if F == H:
            if C == E and C != L and E != I:
                r9 = H
            elif E == G and E != I and G != M:
                r9 = H
            if B != F and D != H:
                if E != I or C == E or E == G or I == L or I == M:
                    r9 = H
                if C != E and (E != I or C == E or E == G or I == L or I == M):
                    r6 = F
                if E != G and (E != I or C == E or E == G or I == L or I == M):
                    r8 = H

        return r1, r2, r3, r4, r5, r6, r7, r8, r9

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
        D = E = K = image3d[y][0]
        F = image3d[y][min(1, X - 1)]
        G = H = image3d[min(y + 1, Y - 1)][0]
        I = image3d[min(y + 1, Y - 1)][min(1, X - 1)]
        J = image3d[max(y - 2, 0)][0]
        M = image3d[min(y + 2, Y - 1)][0]
        L = image3d[y][min(2, X - 1)]

        r1, r2, r3, r4, r5, r6, r7, r8, r9 = _tri(A, B, C, D, E, F, G, H, I, J, K, L, M)

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
            K = D
            D = E
            E = F
            F = L
            L = image3d[y][min(x + 2, X - 1)]
            G = H
            H = I
            I = image3d[min(y + 1, Y - 1)][min(x + 1, X - 1)]
            J = image3d[max(y - 2, 0)][x]
            M = image3d[min(y + 2, Y - 1)][x]

            r1, r2, r3, r4, r5, r6, r7, r8, r9 = _tri(A, B, C, D, E, F, G, H, I, J, K, L, M)

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
