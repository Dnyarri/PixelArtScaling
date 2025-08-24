
| 【EN】 | [〖RU〗](README.RU.md) |
| --- | --- |

# Pixel Art Scaling programs

[![PyPI - Downloads](https://img.shields.io/pypi/dm/scalenx)](https://pypi.org/project/ScaleNx/)

Programs for scaling up small low-color images like icons and game sprites.

Apparently useful for scaling up grey text scans with low resolution before OCR, to improve OCR quality.

> [!NOTE]
> This branch contains special backward compatible version, successfully tested under Python 3.4. It may be behind [main branch](https://github.com/Dnyarri/PixelArtScaling/tree/main).

Currently **Scale2x** (aka AdvMAME2x), **Scale3x** (aka AdvMAME3x), **Scale2xSFX** and **Scale3xSFX** methods are implemented.  

**ScaleNxGUI.py** is a common shell joining together image formats reading/writing and image rescaling modules. Program provides suitable GUI to access both single file and batch files processing.

> [!NOTE]
> In version 25.08.22.34 PNG compression options and PPM/PGM format preferences may be saved to disk as JSON file `scalenx.ini`, edited with any text editor, and loaded back to ScaleNx. Currently file is saved to your user directory (for easy access location is copied to clipboard when saving). Simply point you mouse to status field right above "Exit" button to display the reminder.

Version 25.08.22.34 of main program was intentionally downgraded from `pathlib` to `os` to provide extra compatibility with really antique Python versions.

> [!CAUTION]
> Batch processing programs replace original files with scaled copies. Batch processing programs in this version use async multiprocessing, thus drastically reducing processing time but loading CPU at 100% and rendering GUI almost unresponsive.  

## Sample of Scale3x (twice)

[![Example of Scale3x run twice](https://dnyarri.github.io/imgscalenx/x3x3.png)](https://dnyarri.github.io/scalenx.html)

## Dependencies

1. [PyPNG](https://gitlab.com/drj11/pypng). Copy included into current ScaleNx distribution.
2. [PyPNM](https://pypi.org/project/PyPNM/). Copy included into current ScaleNx distribution.
3. Tkinter, multiprocessing. Included into standard CPython distribution.

> [!NOTE]
> Programs are written entirely on Python, using image representation as list of lists of lists.
> While this representation is logical for human understanding, Python processing of this is slow.
> Moreover, programs contain lists reshaping for PNG and PNM I/O purposes, also performed using Python native means only.
> As a result, programs under discussion are slow as compared to C or C++, but quite compatible with anything capable of running Python, and don't require large external packages causing version conflicts.

## References

1. [Scale2x and Scale3x](https://www.scale2x.it/algorithm) algorithms description by the inventor, Andrea Mazzoleni.

2. [Scale2xSFX and Scale3xSFX](https://web.archive.org/web/20160527015550/https://libretro.com/forums/archive/index.php?t-1655.html) algorithms description at forums archive.

3. [Pixel-art scaling algorithms](https://en.wikipedia.org/wiki/Pixel-art_scaling_algorithms) review at Wikipedia.

4. [ScaleNx at PyPI](https://pypi.org/project/ScaleNx/) - install current ScaleNx core library via *pip*. Does not contain shell, image I/O, and GUI, only ScaleNx core for developers.

## Related

1. [Dnyarri website](https://dnyarri.github.io) - the rest of Dnyarri stuff with previews etc.

2. [github Dnyarri](https://github.com/Dnyarri).

3. [gitflic Dnyarri](https://gitflic.ru/user/dnyarri) mirror.
