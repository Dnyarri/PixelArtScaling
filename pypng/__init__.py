"""Joint between `PyPNG`_ and other programs.

Usage::

    from pypng import list2png, png2list

.. _PyPNG: https://gitlab.com/drj11/pypng

"""

__version__ = '26.6.12.312'

from .pnglpng import list2png, png2list

png2list = png2list
list2png = list2png
