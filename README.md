
| EN | [RU](README.RU.md) |
| --- | --- |

# Pixel Art Scaling programs

Programs for scaling up small low-color images like icons and game sprites.

Apparently useful for scaling up grey text scans with low resolution before OCR, to improve OCR quality.

> [!NOTE]
> For single file processing PNG, PGM and PPM formats are supported. Batch processing of folders and subfolders is supported. Currently only PNG format is supported for batch processing to avoid batch confusions due to different PNM subversions.

Currently [**Scale2x**](https://github.com/amadvance/scale2x) (aka **AdvMAME2x**) and **Scale3x** (aka **AdvMAME3x**) are implemented.  

- **Scale2x.py** - single image rescale, uses Scale2x scaling, equipped with simple GUI for opening and saving PNG files, but can also be run from command line.  
Usage:  
    *python Scale2x.py*                           - starts GUI for selecting source and result  
    *python Scale2x.py source.png*                - rescales source.png and overwrites source.png  
    *python Scale2x.py source.png result.png*     - rescales source.png and writes result.png  

- **batchScale2x.py** - batch rescaling of all PNG files within chosen directory, recursively, using Scale2x algorithm. *Attention:* Source images are replaced, no backup - no mercy.  

- **Scale3x.py** - single image rescale, uses Scale3x scaling, equipped with simple GUI for opening and saving PNG files, but can also be run from command line.  
Usage:  
    *python Scale3x.py*                           - starts GUI for selecting source and result  
    *python Scale3x.py source.png*                - rescales source.png and overwrites source.png  
    *python Scale3x.py source.png result.png*     - rescales source.png and writes result.png  

- **batchScale3x.py** - batch rescaling of all PNG files within chosen directory, recursively, using Scale3x algorithm. *Attention:* Source images are replaced, no backup - no mercy.  

> [!NOTE]
> Batch processing programs in this version use async multiprocessing, drastically reducing processing time but loading CPU at 100% and rendering GUI almost unresponsive.  

## Sample of Scale3x output (twice)

[![Example of Scale3x run twice](https://dnyarri.github.io/imgscalenx/x3x3.png)](https://dnyarri.github.io/scalenx.html)

*Dependencies:* [PyPNG](https://gitlab.com/drj11/pypng), Tkinter, multiprocessing, sys

> [!NOTE]
> Programs are written entirely on Python, using image representation as list of lists of lists.
> While this representation is logical for human understanding, Python processing of this is slow.
> Moreover, programs contain lists reshaping for PNG I/O purposes, also performed using Python native means only.
> As a result, programs are slow but quite compatible with anything and don't require large external packages.

Related links:

[Dnyarri website](https://dnyarri.github.io)

[github Dnyarri](https://github.com/Dnyarri)

[gitflic Dnyarri](https://gitflic.ru/user/dnyarri)
