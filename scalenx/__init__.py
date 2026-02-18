"""
=======
ScaleNx
=======

------------------------------------------------------------------------------
Scale2x, Scale3x, Scale2xSFX and Scale3xSFX image rescaling for Python >=3.10.
------------------------------------------------------------------------------

:Abstract: Current module comprise **Scale2x**, **Scale3x**, **Scale2xSFX**
    and **Scale3xSFX** image rescaling functions, implemented in pure Python.

    Scale2x, Scale3x and Scale4x algorithms `[1]`_ were initially developed by
    `Andrea Mazzoleni`_ in 2001 AD for the sole purpose of upscaling
    low resolution screen output without introducing intermediate colors
    (*i.e.* blur) for old DOS games emulators `[2]`_ and
    similar narrow niche software.

    Later on *ca.* 2014 AD significantly improved Scale2xSFX and Scale3xSFX
    algorithms `[3]`_, providing better diagonals rendering, were introduced
    for the same very specific purpose.

    While screen scalers, based on algorithms above, are numerous,
    general purpose image rescaling wants still seem to be unsupplied.

    Due to severe demand for general purpose ScaleNx library,
    and apparent lack thereof, current general purpose pure Python
    `ScaleNx`_ implementation was developed.

Usage
-----

::

    from scalenx import scaleNx
    result_image = scaleNx(source_image, n, sfx)

where:

- **``source_image``**: source image 3D nested list;
        coordinate system match Photoshop, *i.e.* origin is top left corner,
        channels order is LA or RGBA from 0 to top;
- **``n``**: choice between Scale2* and Scale3* methods:
    - ``n=2``: Scale2x or Scale2xSFX;
    - ``n=3``: Scale3x or Scale3xSFX;

- **``sfx``**: choice between original ScaleNx and improved ScaleNxSFX methods:
    - ``sfx=False``: Scale2x or Scale3x;
    - ``sfx=True``: Scale2xSFX or Scale3xSFX.

.. note:: Function name **``scaleNx``** must contain capital **N**
    to avoid confusion with legacy file/module names.

Compatibility info
------------------

Current implementation is proven to work with CPython 3.10 and above,
and supposed to do so with any other Python version
understanding or ignoring type hints *etc.*

Copyright and redistribution
----------------------------

Current Python `ScaleNx`_ implementation is developed by
Ilya Razmanov (hereinafter referred to as "the Developer"), based on
algorithm descriptions `[1]`_, `[3]`_ by corresponding originators.

Changes introduced by the Developer for the purpose of
speed-up are entirely on his conscience.

Current implementation may be freely used, redistributed and
improved at will by anyone.
Sharing useful modifications with the Developer and lesser species
is your sacred duty to the Universe.

References
----------

`[1]`_. Original description of Scale2x and Scale3x algorithms by `Andrea Mazzoleni`_.

`[2]`_. DOSBox - DOS emulator, using Scale2x and Scale3x screen upscaling.

`[3]`_. Original Scale2xSFX and Scale3xSFX proposal, archived copy.

.. _[1]: https://www.scale2x.it/algorithm

.. _[2]: https://www.dosbox.com/

.. _[3]: https://web.archive.org/web/20160527015550/https://libretro.com/forums/archive/index.php?t-1655.html

.. _Andrea Mazzoleni: https://www.scale2x.it/authors

Resources
---------

The Developer's site: `The Toad's Slimy Mudhole`_

.. _The Toad's Slimy Mudhole: https://dnyarri.github.io

`ScaleNx`_ explanations and illustrations page for current implementation.

.. _ScaleNx: https://dnyarri.github.io/scalenx.html

ScaleNx source repositories: `ScaleNx@Github`_, `ScaleNx@Gitflic`_.

.. _ScaleNx@Github: https://github.com/Dnyarri/PixelArtScaling

.. _ScaleNx@Gitflic: https://gitflic.ru/project/dnyarri/pixelartscaling

`Changelog`_ for current implementation:

.. _Changelog: https://github.com/Dnyarri/PixelArtScaling/blob/main/CHANGELOG.md

"""

__author__ = 'Ilya Razmanov'
__copyright__ = '(c) 2024-2026 Ilya Razmanov'
__credits__ = 'Ilya Razmanov'
__license__ = 'unlicense'
__version__ = '2026.2.16.16'
__maintainer__ = 'Ilya Razmanov'
__email__ = 'ilyarazmanov@gmail.com'
__status__ = 'Production'

from .scalenx import scale2x
from .scalenx import scale3x
from .scalenxsfx import scale2x as scale2xsfx
from .scalenxsfx import scale3x as scale3xsfx


def scaleNx(source_image: list[list[list[int]]], n: int, sfx: bool) -> list[list[list[int]]]:
    """ScaleNx image rescaling, configurable via ``n`` and ``sfx`` options.
    ----

    :param source_image: source image 3D nested list;
        coordinate system match Photoshop, *i.e.* origin is top left corner,
        channels order is LA or RGBA from 0 to top;
    :type source_image: list[list[list[int]]]
    :param int n: ``2`` or ``3``, choice between Scale2* and Scale3* methods;
    :param bool sfx: choice between ScaleNx and ScaleNxSFX methods.
    :raises ValueError: Attempt to use nonexistent method ``n``.
    :return: rescaled image os the same type as ``source_image``.
    :rtype: list[list[list[int]]]

    """
    if sfx:
        if n == 2:
            return scale2xsfx(source_image)
        elif n == 3:
            return scale3xsfx(source_image)
        else:
            raise ValueError('Allowed ScaleNxSFX methods are 2 and 3')
    else:
        if n == 2:
            return scale2x(source_image)
        elif n == 3:
            return scale3x(source_image)
        else:
            raise ValueError('Allowed ScaleNx methods are 2 and 3')
