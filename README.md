
| 【EN】 | [〖RU〗](README.RU.md) |
| --- | --- |

# Pixel Art Scaling programs

[![PyPI - Downloads](https://img.shields.io/pypi/dm/scalenx)](https://pypi.org/project/ScaleNx/)

**ScaleNx**, encompassing Scale2x, Scale3x, Scale2xSFX, and Scale3xSFX, is a group of [pixel-art scaling algorithms](https://en.wikipedia.org/wiki/Pixel-art_scaling_algorithms), intended to rescale images without blurring sharp edges.

Algorithms were originally developed for scaling up small low-color images like icons and game sprites without blurring.

Apparently algorithms appear to be useful for scaling up grey text scans with low resolution before OCR, to improve OCR quality.

Currently **Scale2x** (aka AdvMAME2x), **Scale3x** (aka AdvMAME3x), **Scale2xSFX** and **Scale3xSFX** methods are implemented.  

[**ScaleNxGUI.py**](https://github.com/Dnyarri/PixelArtScaling/blob/main/ScaleNxGUI.py) is a common shell joining together image formats reading/writing and image rescaling modules. Program provides suitable GUI to access both single file and batch files processing.

| ScaleNxGUI |
| :---: |
| [![Main ScaleNx program GUI](https://dnyarri.github.io/imgscalenx/guismall.png "Main ScaleNx program GUI")](https://dnyarri.github.io/scalenx.html) |

> [!NOTE]
> Main version of ScaleNx is compatible with Python 3.10 and above. For older Python users, there is [extended compatibility version](https://github.com/Dnyarri/PixelArtScaling/tree/py34), successfully validated with Python 3.4 under Windows XP 32-bit.

> [!CAUTION]
> Batch processing programs replace original files with scaled copies. Batch processing programs in this version use async multiprocessing, thus drastically reducing processing time but loading all CPUs at 100% and rendering GUI almost unresponsive.  

## Sample of Scale3x (twice)

[![Example of Scale3x run twice](https://dnyarri.github.io/imgscalenx/x3x3.png "Example of Scale3x run twice")](https://dnyarri.github.io/scalenx.html)

## Dependencies

1. [PyPNG](https://gitlab.com/drj11/pypng). Copy included into current ScaleNx distribution.
2. [PyPNM](https://pypi.org/project/PyPNM/). Copy included into current ScaleNx distribution.
3. Tkinter. Normally included into standard CPython distribution for "big" OS-es, although Linux users may need installing it separately.

> [!NOTE]
> Programs are written entirely on Python, using image representation as list of lists of lists.
> While this representation is logical for human understanding, Python processing of this is slow.
> Moreover, programs contain lists reshaping for PNG I/O purposes, also performed using Python native means only.
> As a result, programs are slow but quite compatible with anything capable of running Python, and don't require large external packages causing version conflicts.

## References

1. [Scale2x and Scale3x](https://www.scale2x.it/algorithm) algorithms description by the inventor, Andrea Mazzoleni.

2. [Scale2xSFX and Scale3xSFX](https://web.archive.org/web/20160527015550/https://libretro.com/forums/archive/index.php?t-1655.html) algorithms description at forums archive.

3. [Pixel-art scaling algorithms review](https://en.wikipedia.org/wiki/Pixel-art_scaling_algorithms) at Wikipedia.

### Related

[Dnyarri website - more Python freeware](https://dnyarri.github.io) by the same author.

[ScaleNx page with illustrations](https://dnyarri.github.io/scalenx.html), explanations etc.

[ScaleNx source at github](https://github.com/Dnyarri/PixelArtScaling)

[ScaleNx source at gitflic mirror](https://gitflic.ru/project/dnyarri/pixelartscaling)

[ScaleNx at PyPI](https://pypi.org/project/ScaleNx/) - install current ScaleNx core library via *pip*. Does not contain shell, image I/O, and GUI, only ScaleNx core for developers.
