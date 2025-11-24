"""
=====
PyPNM
=====
--------------------------------------------------------------------------
PPM and PGM image files reading, displaying and writing for Python >=3.11.
--------------------------------------------------------------------------

Usage
-----

::

    from pypnm import pnmlpnm

to access functions.

Formats compatibility
---------------------

Module provides full read and write support for 8 and 16 bpc binary and ASCII
`PPM`_ and `PGM`_ image files, and read-only support for `PBM`_ files.

Python compatibility
--------------------

This is **main** `PyPNM for Python >= 3.11`_ branch; module itself actually
works with any Python supporting f-strings, but Tkinter included with
CPython < 3.11 can not handle 16 bpc images.

If you need more compatibility with old Python and Tkinter versions,
please consider using `PyPNM for Python >= 3.4`_ aka `PyPNM at PyPI`_.

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
