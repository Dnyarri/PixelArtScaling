"""
=====
PyPNM
=====
-------------------------------------------------------------------------
PPM and PGM image files reading, displaying and writing for Python >=3.4.
-------------------------------------------------------------------------

:Abstract: Current module encompass functions for reading `PPM`_, `PGM`_ or
    `PBM`_ file as image list[list[list[int]]], displaying corresponding
    nested list by means of Tkinter, and writing an image nested list to
    `PPM`_ or `PGM`_ file.

    All functions are implemented in pure Python with minimal import of
    standard CPython modules.

Usage
-----

recommended import::

    import pypnm

or::

    from pypnm import list2bin, list2pnm, pnm2list

legacy import, still operational but considered mauvais ton::

    from pypnm import pnmlpnm

to access functions:

- **``pnm2list``**: reading binary or ASCII
  RGB `PPM`_, or L `PGM`_, or ink on/off `PBM`_ file
  and returning image data as nested list of int.

- **``list2bin``**: getting image data as nested list of int and
  creating binary PPM (P6) or PGM (P5) data structure in memory.

  Suitable for generating data to display with Tkinter
  ``PhotoImage(data=...)`` class.

- **``list2pnm``**: getting image data as nested list of int and writing
  either binary or ASCII PNM file depending on ``bin`` bool argument.

Formats compatibility
---------------------

Module provides full read and write support for 8 and 16 bpc binary and ASCII
`PPM`_ and `PGM`_ image files, and read-only support for
1 bpc binary and ASCII `PBM`_ files.

Python compatibility
--------------------

This is **py34** `PyPNM for Python >= 3.4`_ aka `PyPNM at PyPI`_ branch,
containing some workarounds for old Python and old Tkinter versions.
These workarounds make program work a bit slower under some circumstances.

If you are sure you will never use Python versions below 3.11, you may
consider downloading and using `PyPNM for Python >= 3.11`_ branch.

Copyright and redistribution
----------------------------

Written by Ilya Razmanov (https://dnyarri.github.io) to facilitate developing
image editing programs in Python by simplifying work with PPM/PGM files
and displaying arbitrary image-like data with Tkinter ``PhotoImage`` class.

Module is supposed to be used and redistributed freely, and modified at will.

In case of introducing useful modifications it's your duty to all human race
(and probably some other ones) to share it.

----
`PyPNM Documentation`_ (PDF)

.. _PyPNM Documentation: https://dnyarri.github.io/pypnm/pypnm.pdf

.. _PyPNM for Python >= 3.11: https://github.com/Dnyarri/PyPNM/

.. _PyPNM for Python >= 3.4: https://github.com/Dnyarri/PyPNM/tree/py34

.. _PyPNM at PyPI: https://pypi.org/project/PyPNM/

.. _PPM: https://netpbm.sourceforge.net/doc/ppm.html

.. _PGM: https://netpbm.sourceforge.net/doc/pgm.html

.. _PBM: https://netpbm.sourceforge.net/doc/pbm.html

"""

__author__ = 'Ilya Razmanov'
__copyright__ = '(c) 2024-2026 Ilya Razmanov'
__credits__ = 'Ilya Razmanov'
__license__ = 'unlicense'
__version__ = '2.26.26.34'
__maintainer__ = 'Ilya Razmanov'
__email__ = 'ilyarazmanov@gmail.com'
__status__ = 'Production'

from .pnmlpnm import list2bin, list2pnm, pnm2list

# ↓ Assignments below do nothing but stop linter from bitching and whining.
pnm2list = pnm2list
list2bin = list2bin
list2pnm = list2pnm
