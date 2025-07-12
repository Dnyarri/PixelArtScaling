# ScaleNx

[ScaleNx](https://dnyarri.github.io/scalenx.html) is a pure Python module
for pixel image rescaling using
**Scale2x**, **Scale3x**, **Scale2xSFX** and **Scale3xSFX**
algoritms.

## Download

[ScaleNx main branch for Python >= 3.10](https://github.com/Dnyarri/PixelArtScaling)

[ScaleNx py34 branch for Python >= 3.4](https://github.com/Dnyarri/PixelArtScaling/tree/py34)

[ScaleNx py34 at PyPI](https://pypi.org/project/ScaleNx/)

## History

**2024.02.24**  Scale2x and Scale3x converted from standalone to module,
versioning changed to YYYY.MM.DD.

**2024.05.14**  Arguments and return format changed. Incompatible with previous versions!

**2024.07.03**  Small improvements, one more retest with new test corpse, as you were, corpus.

**2024.10.01**  Internal restructure, imports change, maintenance release.

**2024.11.24**  Improved documentation. First publishing at PyPI.

**2025.01.15**  Conditional optimization. Some appends replaced with extends.

**2025.01.16**  Initial implementation of ScaleNxSFX.

**2025.02.01**  FIR optimization. Speed gain, % of original (median):
ca.15% Scale2x, ca. 50% Scale3x, ca.50% Scale2xSFX, ca. 40% Scale2xSFX.

**2025.07.12**  12 Jul 2025 "Kutuzov" release. Compacting, hinting.
