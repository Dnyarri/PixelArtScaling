
| 【EN】 | [〖RU〗](README.RU.md) |
| --- | --- |

# Pixel Art Scaling programs

[![PyPI - Downloads](https://img.shields.io/pypi/dm/scalenx)](https://pypi.org/project/ScaleNx/)

**ScaleNx**, encompassing Scale2x, Scale3x, Scale2xSFX, and Scale3xSFX, is a group of [pixel-art scaling algorithms](https://en.wikipedia.org/wiki/Pixel-art_scaling_algorithms), intended to rescale images without blurring sharp edges.

Algorithms were originally developed for scaling up small low-color images like icons and game sprites without blurring.

Apparently algorithms appear to be useful for scaling up grey text scans with low resolution before OCR, to improve OCR quality.

Currently **Scale2x** (aka AdvMAME2x), **Scale3x** (aka AdvMAME3x), **Scale2xSFX** and **Scale3xSFX** methods are implemented.

## Programs

[**ScaleNxGUI.py**](https://github.com/Dnyarri/PixelArtScaling/blob/main/ScaleNxGUI.py) is a common shell joining together image formats reading/writing and image rescaling modules. Program provides suitable GUI to access both single file and batch files processing.

| ScaleNxGUI |
| :---: |
| [![Main ScaleNx program GUI](https://dnyarri.github.io/imgscalenx/guismall.png "Main ScaleNx program GUI")](https://dnyarri.github.io/scalenx.html) |

> [!NOTE]
> Main version of ScaleNx is compatible with **Python 3.10 and above**. For older Python users, there is [extended compatibility version](https://github.com/Dnyarri/PixelArtScaling/tree/py34), successfully validated with **Python 3.4** under Windows XP 32-bit.

> [!CAUTION]
> Batch processing program replace original files with scaled copies. Batch processing programs in this version use async multiprocessing, thus drastically reducing processing time but loading all CPUs at 100% and rendering GUI almost unresponsive.

[**VisualNxGUI.py**](https://github.com/Dnyarri/PixelArtScaling/blob/main/VisualNxGUI.py) is a visual common shell, providing single image rescaling with preview. After saving rescaled image with, say, Ctrl+S, you may repeat rescaling. Note, however, that during such a sequential upscaling image size grows geometrically - every run of, say, Scale3x makes image 3×3=9 times bigger, so you quickly end up with image of gigabyte size, devouring all your computer memory.

| VisualNxGUI |
| :---: |
| [![Visual ScaleNx program GUI](https://dnyarri.github.io/imgscalenx/vissmall.png "Visual ScaleNx program GUI")](https://dnyarri.github.io/scalenx.html) |

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

## Developers info: Module usage

As of version 2026.2.12.14, recommended ScaleNx module usage is:

```python
from scalenx import scaleNx
scaled_image = scaleNx(source_image, n, sfx)
```

where:

- **`source_image`** is source image data as `list[list[list[int]]]`;
- `int` **`n`** value should be either **`2`** or **`3`**, meaning the choice between Scale**2**\* and Scale**3**\* methods;
- `bool` **`sfx`** means whether you choose ScaleNx**SFX** methods rather than classic ScaleNx;
- **`scaled_image`** is resulting image data as `list[list[list[int]]]`.

However, legacy module access (as of version 2024.02.24) still works, and for, say, Scale3xSFX it looks like:

```python
from scalenx import scalenxsfx
scaled_image = scalenxsfx.scale3x(source_image)
```

## References

1. [Scale2x and Scale3x algorithms description](https://www.scale2x.it/algorithm) by the inventor, Andrea Mazzoleni.

2. [Scale2xSFX and Scale3xSFX algorithms description](https://web.archive.org/web/20160527015550/https://libretro.com/forums/archive/index.php?t-1655.html) at forums archive.

3. [Pixel-art scaling algorithms review](https://en.wikipedia.org/wiki/Pixel-art_scaling_algorithms) at Wikipedia.

### Related

[Dnyarri website - more Python freeware for image processing, POV-Ray and other 3D, and batch automation](https://dnyarri.github.io "The Toad's Slimy Mudhole - Python freeware for POV-Ray and other 3D, Scale2x, Scale3x, Scale2xSFX, Scale3xSFX, PPM and PGM image support, bilinear and barycentric image interpolation, and batch processing") by the same author.

[ScaleNx page with illustrations](https://dnyarri.github.io/scalenx.html "ScaleNx main page, illustrated"), explanations etc.

[ScaleNx source and compiled executables at Github](https://github.com/Dnyarri/PixelArtScaling "ScaleNx source at Github")

[ScaleNx source mirror at Gitflic](https://gitflic.ru/project/dnyarri/pixelartscaling "ScaleNx source at Gitflic mirror")

[ScaleNx at PyPI](https://pypi.org/project/ScaleNx/ "ScaleNx module at PyPI, to be installed with pip") - install current ScaleNx core library using *pip*. Does not contain shell, image I/O, and GUI, only ScaleNx core module for developers.
