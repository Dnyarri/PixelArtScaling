**(EN)** [(RU)](README.RU.md)

# Pixel Art Scaling

Programs for scaling up small low-color images like icons and game sprites.

Apparently useful for scaling up grey text scans with low resolution before OCR.

Currently **Scale2x** (aka **AdvMAME2x**) and **Scale3x** (aka **AdvMAME3x**) are implemented.

- Scale2xGUI.py - uses AdvMAME2x scaling, equipped with simple GUI for opening and saving PNG files.
- Scale2xCLI.py - same AdvMAME2x scaling as above, runs with command line:  
        *python Scale2xCLI.py input.png output.png*

- Scale3xGUI.py - uses AdvMAME3x scaling, equipped with simple GUI for opening and saving PNG files.
- Scale3xCLI.py - same AdvMAME3x scaling as above, runs with command line:  
        *python Scale3xCLI.py input.png output.png*


*Dependencies:* [PyPNG](https://gitlab.com/drj11/pypng), Tkinter, sys

> [!NOTE]
> Programs are written entirely on Python, using image representation as list of lists of lists.
> While this representation is logical for human understanding, Python processing of this is slow.
> Moreover, programs contain lists reshaping for PNG I/O purposes, also performed using Python native means only.
> As a result, programs are slow but quite compatible with anything and don't require large external packages.

Related projects:

[github Dnyarri](https://github.com/Dnyarri)
