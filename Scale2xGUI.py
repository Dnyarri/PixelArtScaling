# Attempt to write Scale2x aka AdvMAME2x using Python only
# Created by Ilyich the Toad (mailto: amphisoft@gmail.com)
# Versions:
# 01.001    Scale2x (AdvMAME2x) seem to work 
# 01.002    Changed from self-contained to modular, IncSrc and IncScaleNx modules created 
# 01.003    Ultimate modular evil, moving everything possible to IncSrc.py and IncScaleNx.py 
# 01.004    Progress indication added, showing processing stage 

from tkinter import Tk
from tkinter import Label
from tkinter import filedialog

import png                      # PNG reading: PyPNG from: https://gitlab.com/drj11/pypng
import IncSrc                   # Image reshaping from: https://github.com/Dnyarri/PixelArtScaling
from IncScaleNx import Scale2x  # Scale2x and Scale3x from: https://github.com/Dnyarri/PixelArtScaling

# --------------------------------------------------------------
# Creating dialog

sortir = Tk()
sortir.title('Scale2x')
zanyato = Label(sortir, text = 'Starting...', font=("arial", 36), padx=15, pady=10, justify='center')
zanyato.pack()
sortir.withdraw()

# Main dialog created and hidden
# --------------------------------------------------------------

# --------------------------------------------------------------
# Open source file

sourcefilename = filedialog.askopenfilename(title='Open source PNG file', filetypes=[('PNG','.png')])
if (sourcefilename == ''):
    quit()

source = png.Reader(filename = sourcefilename)
X,Y,pixels,info = source.asDirect() # Opening image, iDAT comes to "pixels" as bytearray, to be tuple'd lated.
Z = (info['planes'])                # PyPNG returns X,Y directly, but not Z. Z should be extracted from info
imagedata = tuple((pixels))         # Attempt to fix all bytearrays as something solid

# Source file opened as imagedata
# --------------------------------------------------------------

# --------------------------------------------------------------
# Updating dialog

sortir.deiconify()
zanyato.config(text = 'Reading...')
sortir.update()
sortir.update_idletasks()

# Dialog shown and updated
# --------------------------------------------------------------

# Reading image as list
ImageAsListListList = IncSrc.Img3D(imagedata, X, Y, Z)

# --------------------------------------------------------------
# Updating dialog

zanyato.config(text = 'Scaling...')
sortir.update()
sortir.update_idletasks()

# Dialog updated
# --------------------------------------------------------------

# Scaling list to 2x image list
EPXImage,doubleX,doubleY = Scale2x(ImageAsListListList, X, Y)

# --------------------------------------------------------------
# Updating dialog

zanyato.config(text='Almost there...')
sortir.update()
sortir.update_idletasks()

# Dialog updated
# --------------------------------------------------------------

# Reshaping 2x scaled 3D list into 1D list for PyPNG .write_array method
ResultImageAsList = IncSrc.Img3Dto1D(EPXImage, doubleX, doubleY, Z)

# --------------------------------------------------------------
# Hiding dialog

sortir.withdraw()

# Dialog hidden
# --------------------------------------------------------------

# --------------------------------------------------------------
# Open export file

resultPNG = filedialog.asksaveasfile(mode='wb', title='Save resulting PNG file', filetypes=[('PNG','.png')], defaultextension = ('PNG file','.png'))
if (resultPNG == ''):
    quit()

# Export file opened
# --------------------------------------------------------------

# --------------------------------------------------------------
# Writing export file

writer = png.Writer(doubleX, doubleY, greyscale = info['greyscale'], alpha = info['alpha'], bitdepth = info['bitdepth'])
writer.write_array(resultPNG, ResultImageAsList)
resultPNG.close()

# Export file written and closed
# --------------------------------------------------------------

# --------------------------------------------------------------
# Destroying dialog

sortir.destroy()
sortir.mainloop()

# Dialog destroyed and closed
# --------------------------------------------------------------
