"""
=======
ScaleNx
=======

-----------------------------------------------------------
Scale2x, Scale3x, Scale2xSFX and Scale3xSFX image rescaling
-----------------------------------------------------------

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

for ScaleNx::

    from scalenx import scalenx

for ScaleNxSFX::

    from scalenx import scalenxsfx

then refer to function descriptions in ``scalenx`` and ``scalenxsfx`` correspondingly.

Compatibility info
------------------------------

Current implementation is proven to work with CPython 3.10 and above,
and supposed to do so with any other Python version
understanding or ignoring type hints *etc.*

Copyright and redistribution
----------------------------

Current Python `ScaleNx`_ implementation is developed by
Ilya Razmanov (hereinafter referred to as "the Developer"),
based on algorithm descriptions `[1]`_, `[3]`_.

Changes introduced by the Developer for the purpose of
speed-up are on his conscience.

Current implementation may be freely used, redistributed and improved at will by anyone.
Sharing useful modifications with the Developer and lesser species is next to obligatory.

References
----------

`[1]`_. Original description of Scale2x and Scale3x algorithms by `Andrea Mazzoleni`_.

`[2]`_. DOSBox - DOS emulator, using Scale2x and Scale3x screen upscaling.

`[3]`_. Original Scale2xSFX and Scale3xSFX proposal, archived copy.

.. _[1]: https://www.scale2x.it/algorithm

.. _[2]: https://www.dosbox.com/

.. _[3]: https://web.archive.org/web/20160527015550/https://libretro.com/forums/archive/index.php?t-1655.html

.. _Andrea Mazzoleni: https://www.scale2x.it/authors

----
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
