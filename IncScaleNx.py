'''
Overview
----------

- IncScaleNx.Scale2x    - Scale2x aka AdvMAME2x image scaling two times
- IncScaleNx.Scale3x    - Scale3x aka AdvMAME3x image scaling three times

Installation
--------------
Simply put module into your program folder

Usage
-------
After import IncScaleNx, use something like:

``ScaledImage,newX,newY = IncScaleNx.Scale3x(SourceImage,SourceX,SourceY)``

where both "Image" are lists, all "X" and "Y" are integer sizes of "Image" along X and Y.


Copyright and redistribution
-----------------------------
Deleloped by Ilya Razmanov (https://github.com/Dnyarri/),
based on brief algorithm description by Andrea Mazzoleni (https://www.scale2x.it/)

Last modified 18.02.2024

May be freely used and included anywhere by anyone who found it useful.

'''


# --------------------------------------------------------------
# Scaling image list to 2x image list
#

def Scale2x(ImageAsListListList, X, Y):

    doubleX = 2*X; doubleY = 2*Y

    EPXImage = list()

    for y in range(0, Y, 1):
        RowRez = list(); RowDvo = list()
        for x in range(0, X, 1):

            P = ImageAsListListList[y][x]
            A = ImageAsListListList[max(y-1, 0)][x]
            B = ImageAsListListList[y][min(x+1, X-1)]
            C = ImageAsListListList[y][max(x-1, 0)]
            D = ImageAsListListList[min(y+1, Y-1)][x]

            r1 = P; r2 = P; r3 = P; r4 = P
        
            if ((C==A) and (C!=D) and (A!=B)):
                r1 = A
            if ((A==B) and (A!=C) and (B!=D)):
                r2 = B
            if ((D==C) and (D!=B) and (C!=A)):
                r3 = C
            if ((B==D) and (B!=A) and (D!=C)):
                r4 = D

            RowRez.append(r1); RowRez.append(r2)
            RowDvo.append(r3); RowDvo.append(r4)
    
        EPXImage.append(RowRez)
        EPXImage.append(RowDvo)

    return(EPXImage, doubleX, doubleY)

#
# rescaling two times finished
# --------------------------------------------------------------


# --------------------------------------------------------------
# Scaling to 3x image list
#

def Scale3x(ImageAsListListList, X, Y):

    tripleX = 3*X; tripleY = 3*Y

    EPXImage = list()

    for y in range(0, Y, 1):
        RowRez = list(); RowDvo = list(); RowTre = list()
        for x in range(0, X, 1):

            E = ImageAsListListList[y][x]   # E is a center of 3x3 square

            A = ImageAsListListList[max(y-1, 0)][max(x-1, 0)]
            B = ImageAsListListList[max(y-1, 0)][x]
            C = ImageAsListListList[max(y-1, 0)][min(x+1, X-1)]

            D = ImageAsListListList[y][max(x-1, 0)]
            # central pixel E = ImageAsListListList[y][x] calculated already
            F = ImageAsListListList[y][min(x+1, X-1)]

            G = ImageAsListListList[min(y+1, Y-1)][max(x-1, 0)]
            H = ImageAsListListList[min(y+1, Y-1)][x]
            I = ImageAsListListList[min(y+1, Y-1)][min(x+1, X-1)]

            r1 = E; r2 = E; r3 = E; r4 = E; r5 = E; r6 = E; r7 = E; r8 = E; r9 = E

            if ((D==B) and (D!=H) and (B!=F)):
                r1 = D
            if (((D==B) and (D!=H) and (B!=F) and (E!=C)) or ((B==F) and (B!=D) and (F!=H) and (E!=A))):
                r2 = B
            if ((B==F) and (B!=D) and (F!=H)):
                r3 = F
            if  (((H==D) and (H!=F) and (D!=B) and (E!=A)) or ((D==B) and (D!=H) and (B!=F) and (E!=G))):
                r4 = D
            # r5 = E already
            if  (((B==F) and (B!=D) and (F!=H) and (E!=I)) or ((F==H) and (F!=B) and (H!=D) and (E!=C))):
                r6 = F
            if  ((H==D) and (H!=F) and (D!=B)):
                r7 = D
            if  (((F==H) and (F!=B) and (H!=D) and (E!=G)) or ((H==D) and (H!=F) and (D!=B) and (E!=I))):
                r8 = H
            if  ((F==H) and (F!=B) and (H!=D)):
                r9 = F

            RowRez.append(r1); RowRez.append(r2); RowRez.append(r3)
            RowDvo.append(r4); RowDvo.append(r5); RowDvo.append(r6)
            RowTre.append(r7); RowTre.append(r8); RowTre.append(r9)

        EPXImage.append(RowRez)
        EPXImage.append(RowDvo)
        EPXImage.append(RowTre)

    return(EPXImage, tripleX, tripleY)

#
# rescaling three times finished
# --------------------------------------------------------------


if __name__ == "__main__":
    print('Module to be imported, not run as standalone')