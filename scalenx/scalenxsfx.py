#!/usr/bin/env python3

"""
=======
ScaleNx
=======

-----------------------------------------
Scale2xSFX and Scale3xSFX image rescaling
-----------------------------------------

:Abstract: Current module comprise **Scale2xSFX** and **Scale3xSFX** `[1]`_ image rescaling functions, implemented in pure Python.

Usage
-----

Scale2xSFX::

    scaled_image = scalenxsfx.scale2x(source_image)

Scale3xSFX::

    scaled_image = scalenxsfx.scale3x(source_image)

where:

- `source_image`: input image as list of lists (rows) of lists (pixels) of int (channel values);
- `scaled_image`: output image as list of lists (rows) of lists (pixels) of int (channel values).

References
----------

`[1]`_. Original Scale2xSFX and Scale3xSFX proposal, archived copy.

.. _[1]: https://web.archive.org/web/20160527015550/https://libretro.com/forums/archive/index.php?t-1655.html

----
The Developer site: `The Toad's Slimy Mudhole`_

.. _The Toad's Slimy Mudhole: https://dnyarri.github.io

`ScaleNx`_ explanations and illustrations page for current ScaleNx Python implementation.

.. _ScaleNx: https://dnyarri.github.io/scalenx.html

ScaleNx source repositories: `ScaleNx@Github`_, `ScaleNx@Gitflic`_.

.. _ScaleNx@Github: https://github.com/Dnyarri/PixelArtScaling

.. _ScaleNx@Gitflic: https://gitflic.ru/project/dnyarri/pixelartscaling

`Changelog`_ for current implementation:

.. _Changelog: https://github.com/Dnyarri/PixelArtScaling/blob/main/CHANGELOG.md

"""

__author__ = 'Ilya Razmanov'
__copyright__ = '(c) 2025 Ilya Razmanov'
__credits__ = 'Ilya Razmanov'
__license__ = 'unlicense'
__version__ = '2025.11.15.1'
__maintainer__ = 'Ilya Razmanov'
__email__ = 'ilyarazmanov@gmail.com'
__status__ = 'Production'

""" ╔════════════════════════════════════════════╗
    ║ Scaling image nested list to 2x image list ║
    ╚════════════════════════════════════════════╝ """


def scale2x(image3d: list[list[list[int]]]) -> list[list[list[int]]]:
    """Scale2xSFX image rescale.
    ----

    :param image3d: 3D nested list (image) of lists (rows) of lists (pixels) of int (channel values);
    :type image3d: list[list[list[int]]]
    :return: 3D nested list of the same structure as input, rescaled in X and Y directions twice using Scale2xSFX.
    :rtype: list[list[list[int]]]

    """

    # ↓ determining source image size from list
    Y = len(image3d)
    X = len(image3d[0])

    # ↓ starting new image list
    scaled_image: list[list[list[int]]] = []

    def _dva(A: list[int], B: list[int], C: list[int], D: list[int], E: list[int], F: list[int], G: list[int], H: list[int], I: list[int], J: list[int], K: list[int], L: list[int], M: list[int]):
        """Scale2xSFX conditional tree function."""

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
        """ ┌───────────────────────┐
            │ First pixel in a row. │
            │ "Repeat edge" mode.   │
            └───────────────────────┘ """
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

        """ ┌───────────────────────────────────────────┐
            │ Next pixels in a row (below).             │
            │ Reusing pixels from previous kernel.      │
            │ Only rightmost pixels are read from list. │
            └───────────────────────────────────────────┘ """
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

    return scaled_image
# ↑ rescaling two times finished


""" ╔════════════════════════════════════════════╗
    ║ Scaling image nested list to 3x image list ║
    ╚════════════════════════════════════════════╝ """


def scale3x(image3d: list[list[list[int]]]) -> list[list[list[int]]]:
    """Scale3xSFX image rescale.
    ----

    :param image3d: 3D nested list (image) of lists (rows) of lists (pixels) of int (channel values);
    :type image3d: list[list[list[int]]]
    :return: 3D nested list of the same structure as input, rescaled in X and Y directions thrice using Scale3xSFX.
    :rtype: list[list[list[int]]]

    """

    # ↓ determining source image size from list
    Y = len(image3d)
    X = len(image3d[0])

    # ↓ starting new image list
    scaled_image: list[list[list[int]]] = []

    def _tri(A: list[int], B: list[int], C: list[int], D: list[int], E: list[int], F: list[int], G: list[int], H: list[int], I: list[int], J: list[int], K: list[int], L: list[int], M: list[int]):
        """Scale3xSFX conditional tree function."""

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
        """ ┌───────────────────────┐
            │ First pixel in a row. │
            │ "Repeat edge" mode.   │
            └───────────────────────┘ """
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

        """ ┌───────────────────────────────────────────┐
            │ Next pixels in a row (below).             │
            │ Reusing pixels from previous kernel.      │
            │ Only rightmost pixels are read from list. │
            └───────────────────────────────────────────┘ """
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

    return scaled_image
# ↑ rescaling three times finished


# ↓ Dummy stub for standalone execution attempt
if __name__ == '__main__':
    print('Module to be imported, not run as standalone.')
    need_help = input('Would you like to read some help (y/n)?')
    if need_help.startswith(('y', 'Y')):
        import scalenxsfx
        help(scalenxsfx)
