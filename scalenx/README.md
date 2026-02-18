# Pixel art image scaling - Scale2x, Scale3x, Scale2xSFX and Scale3xSFX in pure Python

## Overview

[**ScaleNx**](https://dnyarri.github.io/scalenx.html), encompassing **Scale2x**, **Scale3x**, **Scale2xSFX**, and **Scale3xSFX**, is a group of [pixel-art scaling algorithms](https://en.wikipedia.org/wiki/Pixel-art_scaling_algorithms), intended to rescale images without introducing additional colors and blurring sharp edges.

[**Scale2x** and **Scale3x**](https://github.com/amadvance/scale2x) (aka **AdvMAME2x** and **AdvMAME3x**) algorithms were developed by [Andrea Mazzoleni](https://www.scale2x.it/) for the sole purpose of scaling up small graphics like icons and game sprites while keeping sharp edges, avoiding blurs, and, unlike nearest neighbour interpolation, taking into account diagonal patterns to avoid converting image into square mosaic.

Later on improved versions, called [**Scale2xSFX** and **Scale3xSFX**](https://web.archive.org/web/20160527015550/https://libretro.com/forums/archive/index.php?t-1655.html), were introduced for the same purpose, providing better diagonals rendering and less artifacts on some patterns.

| Fig. 1. *Example of consecutive upscaling with Scale3xSFX.* |
| :---: |
| ![Consecutive upscaling with Scale3xSFX](https://dnyarri.github.io/imgscalenx/diag3sfx.png "Consecutive upscaling with Scale3xSFX thrice") |
| *Consecutive upscaling of tiny diagonal object with Scale3xSFX thrice. Source object on the left upscaled 3x3x3=27 times bigger in linear size, i.e. 27x27=729 times bigger by area, meaning that 728 out of 729 resulting pixels are purely artificial; yet the result looks surprisingly clear.* |

Being initially created for tiny game sprite images, these algorithms appeared to be useful for some completely different tasks, *e.g.* scaling up text scans with low resolution before OCR, to improve OCR quality, or upscaling old low quality gravure and line art prints. One of the advantages of ScaleNx algorithms is that they don't use any empirical chroma mask or something else specifically adopted for game sprites on screen, and therefore are capable to work efficiently on any image, including images intended for print.

| Fig. 2. *Example of low resolution drawing upscaling with Scale3xSFX.* |
| :---: |
| ![Upscaling with Scale3xSFX](https://dnyarri.github.io/imgscalenx/mu3sfx.png "Upscaling with Scale3xSFX") |
| *Jagged lines of low resolution original are turned into smoother diagonals.* |

Unfortunately, while specialised Scale2x and Scale3x screen renderers (*e.g.* scalers for DOS emulators) are numerous, it appears to be next to impossible to find ready-made batch processing application working with arbitrary images in common graphics formats.

Therefore, due to severe demand for general purpose ScaleNx library, and apparent lack thereof, current general purpose pure Python implementation of algorithms above was developed. Current implementation does not use any import, neither Python standard nor third party, and therefore is quite cross-platform and next to omnicompatible.

Note that current wheel package is intended for developers, and therefore include ScaleNx core module only. For example of practical Python program utilizing this module, with Tkinter GUI, multiprocessing *etc.*, please visit [ScaleNx at Github](https://github.com/Dnyarri/PixelArtScaling) (PNG support in this program is based on [PyPNG](https://gitlab.com/drj11/pypng), and PPM and PGM support - on [PyPNM](https://pypi.org/project/PyPNM/), both of the above being pure Python modules with excellent backward compatibility as well).

## Python compatibility

Current distribution is **ScaleNx main branch** build, proven to work with Python 3.10 and above.

For a Python 3.4 compatible version, please refer to [ScaleNx for Python 3.4 branch](https://github.com/Dnyarri/PixelArtScaling/tree/py34).

## Installation

`python -m pip install scalenx-????.??.??.??-py3-none-any.whl`.

where "?" correspond to actual version number.

## Usage

As of version 2026.2.16.16, recommended ScaleNx module usage is:

```python
from scalenx import scaleNx
scaled_image = scaleNx(source_image, n, sfx)
```

where:

- **`source_image`** is source image data as `list[list[list[int]]]`;
- `int` **`n`** value should be either **`2`** or **`3`**, meaning the choice between Scale**2**\* and Scale**3**\* methods;
- `bool` **`sfx`** means whether you choose ScaleNx**SFX** methods rather than classic ScaleNx;
- **`scaled_image`** is resulting image data as `list[list[list[int]]]`.

However, legacy module access (as of version 2024.11.24) still works, and for, say, Scale2x it looks like:

```python
from scalenx import scalenx
scaled_image = scalenx.scale2x(source_image)
```

therefore no changes required for programs written using older (2024-2025) versions of ScaleNx.

## Copyright and redistribution

Current Python implementation was written by [Ilya Razmanov](https://dnyarri.github.io/) and may be freely used, copied and improved. In case of making substantial improvements it's almost obligatory to share your work with the developer and lesser species.

## References

1. [Scale2x and Scale3x algorithms description](https://www.scale2x.it/algorithm) by the inventor, Andrea Mazzoleni.

2. [Scale2xSFX and Scale3xSFX algorithms description](https://web.archive.org/web/20160527015550/https://libretro.com/forums/archive/index.php?t-1655.html) at dead forum article, archived copy.

3. [Pixel-art scaling algorithms review](https://en.wikipedia.org/wiki/Pixel-art_scaling_algorithms) at Wikipedia.

4. [Current ScaleNx implementation main page](https://dnyarri.github.io/scalenx.html) with some explanations and illustration.

5. [ScaleNx source code at Github](https://github.com/Dnyarri/PixelArtScaling/) - current ScaleNx source at Github, containing main program for single and batch image processing, with GUI, multiprocessing *etc.*.

6. [ScaleNx source code for Python 3.4 at Github](https://github.com/Dnyarri/PixelArtScaling/tree/py34) - same as above, but fully compatible with Python 3.4 (both ScaleNx and image formats I/O and main application).
