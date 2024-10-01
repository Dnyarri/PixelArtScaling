#!/usr/bin/env python3

'''
Overview
----------

- scalenx.scale2x    - Scale2x aka AdvMAME2x image scaling two times
- scalenx.scale3x    - Scale3x aka AdvMAME3x image scaling three times

Installation
--------------
Simply put module into your program folder

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

2024.05.14  Arguments and return format changed. Incompatible with previous versions!

2024.07.03  Small improvements, one more retest with new test corpse, as you were, corpus.

24.10.01    Internal restructure, imports change, maintenance release.

'''

__author__ = 'Ilya Razmanov'
__copyright__ = '(c) 2024 Ilya Razmanov'
__credits__ = ['Ilya Razmanov', 'Andrea Mazzoleni']
__license__ = 'unlicense'
__version__ = '2024.07.03'
__maintainer__ = 'Ilya Razmanov'
__email__ = 'ilyarazmanov@gmail.com'
__status__ = 'Production'

# --------------------------------------------------------------
# Scaling image list to 2x image list
#


def scale2x(ImageAsListListList):
    '''
    Takes ``ImageAsListListList`` as 3D list (image) of lists (rows) of lists (pixels) of int (channel values) (see InSrc.py for detail), and performs Scale2x rescaling, returning scaled image of similar structure.

    '''

    # determining image size from list
    Y = len(ImageAsListListList)
    X = len(ImageAsListListList[0])

    # building new list
    EPXImage = list()

    for y in range(0, Y, 1):
        RowRez = list()
        RowDvo = list()
        for x in range(0, X, 1):

            P = ImageAsListListList[y][x]
            A = ImageAsListListList[max(y - 1, 0)][x]
            B = ImageAsListListList[y][min(x + 1, X - 1)]
            C = ImageAsListListList[y][max(x - 1, 0)]
            D = ImageAsListListList[min(y + 1, Y - 1)][x]

            r1 = r2 = r3 = r4 = P

            if (C == A) and (C != D) and (A != B):
                r1 = A
            if (A == B) and (A != C) and (B != D):
                r2 = B
            if (D == C) and (D != B) and (C != A):
                r3 = C
            if (B == D) and (B != A) and (D != C):
                r4 = D

            RowRez.append(r1)
            RowRez.append(r2)
            RowDvo.append(r3)
            RowDvo.append(r4)

        EPXImage.append(RowRez)
        EPXImage.append(RowDvo)

    return EPXImage  # rescaling two times finished


# --------------------------------------------------------------
# Scaling to 3x image list
#


def scale3x(ImageAsListListList):
    '''
    Takes ``ImageAsListListList`` as 3D list (image) of lists (rows) of lists (pixels) of int (channel values) (see InSrc.py for detail), and performs Scale3x rescaling, returning scaled image of similar structure.

    '''

    # determining image size from list
    Y = len(ImageAsListListList)
    X = len(ImageAsListListList[0])

    # building new list
    EPXImage = list()

    for y in range(0, Y, 1):
        RowRez = list()
        RowDvo = list()
        RowTre = list()
        for x in range(0, X, 1):

            E = ImageAsListListList[y][x]  # E is a center of 3x3 square

            A = ImageAsListListList[max(y - 1, 0)][max(x - 1, 0)]
            B = ImageAsListListList[max(y - 1, 0)][x]
            C = ImageAsListListList[max(y - 1, 0)][min(x + 1, X - 1)]

            D = ImageAsListListList[y][max(x - 1, 0)]
            # central pixel E = ImageAsListListList[y][x] calculated already
            F = ImageAsListListList[y][min(x + 1, X - 1)]

            G = ImageAsListListList[min(y + 1, Y - 1)][max(x - 1, 0)]
            H = ImageAsListListList[min(y + 1, Y - 1)][x]
            I = ImageAsListListList[min(y + 1, Y - 1)][min(x + 1, X - 1)]

            r1 = r2 = r3 = r4 = r5 = r6 = r7 = r8 = r9 = E

            if (D == B) and (D != H) and (B != F):
                r1 = D
            if ((D == B) and (D != H) and (B != F) and (E != C)) or ((B == F) and (B != D) and (F != H) and (E != A)):
                r2 = B
            if (B == F) and (B != D) and (F != H):
                r3 = F
            if ((H == D) and (H != F) and (D != B) and (E != A)) or ((D == B) and (D != H) and (B != F) and (E != G)):
                r4 = D
            # r5 = E already
            if ((B == F) and (B != D) and (F != H) and (E != I)) or ((F == H) and (F != B) and (H != D) and (E != C)):
                r6 = F
            if (H == D) and (H != F) and (D != B):
                r7 = D
            if ((F == H) and (F != B) and (H != D) and (E != G)) or ((H == D) and (H != F) and (D != B) and (E != I)):
                r8 = H
            if (F == H) and (F != B) and (H != D):
                r9 = F

            RowRez.append(r1)
            RowRez.append(r2)
            RowRez.append(r3)
            RowDvo.append(r4)
            RowDvo.append(r5)
            RowDvo.append(r6)
            RowTre.append(r7)
            RowTre.append(r8)
            RowTre.append(r9)

        EPXImage.append(RowRez)
        EPXImage.append(RowDvo)
        EPXImage.append(RowTre)

    return EPXImage  # rescaling three times finished


# --------------------------------------------------------------


if __name__ == '__main__':
    print('Module to be imported, not run as standalone')
