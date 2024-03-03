**(EN)** [(RU)](README.RU.md)

# Pixel Art Scaling programs

Programs for scaling up small low-color images like icons and game sprites.

Apparently useful for scaling up grey text scans with low resolution before OCR, to improve OCR quality.

> [!NOTE]
> Only PNG image format is supported. Batch processing of folders and subfolders is supported.

Currently **Scale2x** (aka **AdvMAME2x**) and **Scale3x** (aka **AdvMAME3x**) are implemented.

- Scale2xGUI.py - uses AdvMAME2x scaling, equipped with simple GUI for opening and saving PNG files.
- Scale2xCLI.py - same AdvMAME2x scaling as above, runs with command line:  
        *python Scale2xCLI.py input.png output.png*
- batchScale2x.py - batch rescaling of all PNG files within chosen directory, recursively, using AdvMAME2x scaling. Rescaled images are saved as copies with ".2x.png" extension added.

- Scale3xGUI.py - uses AdvMAME3x scaling, equipped with simple GUI for opening and saving PNG files.
- Scale3xCLI.py - same AdvMAME3x scaling as above, runs with command line:  
        *python Scale3xCLI.py input.png output.png*
- batchScale3x.py - batch rescaling of all PNG files within chosen directory, recursively, using AdvMAME3x scaling. Rescaled images are saved as copies with ".3x.png" extension added.

Take notice that, by running batchScaleNx programs on the same folder several times, you progressively populate this folder with copies of copies of copies of PNGs with different rescaling. Soon they multiply, and only one man can stop it.

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