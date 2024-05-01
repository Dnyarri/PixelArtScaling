**(EN)** [(RU)](README.RU.md)

# Pixel Art Scaling programs

Programs for scaling up small low-color images like icons and game sprites.

Apparently useful for scaling up grey text scans with low resolution before OCR, to improve OCR quality.

> [!NOTE]
> This is (supposedly) last single-process release.

Currently **Scale2x** (aka **AdvMAME2x**) and **Scale3x** (aka **AdvMAME3x**) are implemented.

- Scale2xGUI.py - uses Scale2x scaling, equipped with simple GUI for opening and saving PNG files.
- Scale2xCLI.py - same Scale2x scaling as above, runs with command line:  
        *python Scale2xCLI.py input.png output.png*
- batchScale2x.py - batch rescaling of all PNG files within chosen directory, recursively, using Scale2x scaling. Source images are replaced, no backup - no mercy.  

- Scale3xGUI.py - uses Scale3x scaling, equipped with simple GUI for opening and saving PNG files.
- Scale3xCLI.py - same Scale3x scaling as above, runs with command line:  
        *python Scale3xCLI.py input.png output.png*
- batchScale3x.py - batch rescaling of all PNG files within chosen directory, recursively, using Scale3x scaling. Source images are replaced, no backup - no mercy.  

## Sample of Scale3x output (twice)

![Example of Scale3x run twice](https://dnyarri.github.io/imgscalenx/x3x3.png)

*Dependencies:* [PyPNG](https://gitlab.com/drj11/pypng), Tkinter, sys

> [!NOTE]
> Programs are written entirely on Python, using image representation as list of lists of lists.
> While this representation is logical for human understanding, Python processing of this is slow.
> Moreover, programs contain lists reshaping for PNG I/O purposes, also performed using Python native means only.
> As a result, programs are slow but quite compatible with anything and don't require large external packages.

Related links:

[Dnyarri website](https://dnyarri.github.io)

[github Dnyarri](https://github.com/Dnyarri)

[gitflic Dnyarri](https://gitflic.ru/user/dnyarri)
