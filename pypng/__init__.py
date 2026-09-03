"""Joint between `PyPNG`_ and other programs.

Usage::

    from pypng import list2png, png2list

.. _PyPNG: https://gitlab.com/drj11/pypng

"""

__version__ = '26.8.28.312'
__all__ = ['list2png', 'png2list']

from .pnglpng import list2png, png2list
