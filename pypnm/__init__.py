"""
=====
PyPNM
=====
--------------------------------------------------------------------------
PPM and PGM image files reading, displaying and writing for Python >=3.11.
--------------------------------------------------------------------------

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

Module provides full read and write support for 8 and 16 bpc
binary and ASCII `PPM`_ and `PGM`_ image files, and
read-only support for 1 bpc binary and ASCII `PBM`_ files.

Python compatibility
--------------------

This module belongs to **main** `PyPNM for Python >= 3.11`_ branch;
module itself actually works with older Pythons supporting f-strings,
but Tkinter included with CPython 3.10 and below can not handle double
bytes (16 bpc image data) correctly.

If you need more compatibility with old Python and Tkinter versions,
please consider using `PyPNM for Python >= 3.4`_ aka `PyPNM at PyPI`_,
containing workarounds for old Tkinter.

.. note:: versions 3.x.x.x of PyPNM include ``list2bin`` patch with
    multithreading support. When used with free-threaded CPython
    (e.g., ``python3.14t.exe``), it ensures ``list2bin`` speed gain
    proportional to number of CPU cores.

    Free-threaded Python detection is performed upon module import
    and is based solely on ``sys._is_gil_enabled()`` function. Any
    Python implementation missing this function is considered
    GIL-enabled regardless of end user opinion, and module falls back
    to importing classic 2.x.x.x version automatically.

.. data:: SUBVERSION

    For developers, current PyPNM version returns **SUBVERSION** ``str``,
    equal to either ``'MT'`` (multithreaded) or ``'ST'`` (single threaded),
    depending on what ``list2bin`` version is *actually* used right now.

Copyright and redistribution
----------------------------

Written by Ilya Razmanov (https://dnyarri.github.io) to facilitate developing
image editing programs in Python by simplifying displaying image-like data
with Tkinter ``PhotoImage`` class, and providing support for PPM/PGM files.

Module is supposed to be used and redistributed freely, and modified at will.

In case of introducing useful modifications it's your duty to all human race
(and probably some other ones) to share it.

----
References:

1. `PyPNM Documentation`_ (PDF)
2. `PPM`_ specification
3. `PGM`_ specification
4. `PBM`_ specification

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
__version__ = '3.34.24.314'  # 24 Oct 2026
__maintainer__ = 'Ilya Razmanov'
__email__ = 'ilyarazmanov@gmail.com'
__status__ = 'Production'
__all__ = ['list2bin', 'list2pnm', 'pnm2list']

from .pnmlpnm import list2pnm, pnm2list

try:
    from sys import _is_gil_enabled

    if _is_gil_enabled():
        SUBVERSION = 'ST'
        from .pnmlpnm import list2bin
    else:
        SUBVERSION = 'MT'
        from .bint import list2bin

except ImportError:
    SUBVERSION = 'ST'
    from .pnmlpnm import list2bin
