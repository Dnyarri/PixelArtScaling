# ScaleNx

[ScaleNx](https://dnyarri.github.io/scalenx.html) is a pure Python module for pixel image rescaling using Scale2x, Scale3x, Scale2xSFX and Scale3xSFX algorithms.

Current changelog is related to ScaleNx module, not the main GUI shell. Main GUI shell gets updated more frequently and without notice.

## Version

Current changelog is related to extended compatibility version [ScaleNx py34 branch for Python >= 3.4](https://github.com/Dnyarri/PixelArtScaling/tree/py34). For main version see [ScaleNx main branch for Python >= 3.10](https://github.com/Dnyarri/PixelArtScaling).

## Downloads

1. [ScaleNx main branch for Python >= 3.10](https://github.com/Dnyarri/PixelArtScaling)
2. [ScaleNx py34 branch for Python >= 3.4](https://github.com/Dnyarri/PixelArtScaling/tree/py34)
3. [ScaleNx py34 at PyPI](https://pypi.org/project/ScaleNx/)

## History

| Version | Changes |
| :--- | :--- |
| 2026.06.12.34 | Attempts made to use `lru_cache` to increase conditional trees speed for big size low color images. Testing performed on 1 bpc text images, A4 size, 75-150 ppi range. According to test results, `lru_cache` is inefficient for Scale2x and Scale2xSFX, and gives speed gain *ca.* 4% (up to 6.4%) for Scale3x, and *ca.* 17% (up to 18.5%) for Scale3xSFX. Cache `maxsize` impact was also investigated using some actual images corpus. For Scale3x, cache size rarely exceeded 400; for Scale3xSFX it tended to exceed 2000 but speed impact of increasing cache size over 1024 appeared to be statistically insignificant, if any. Based on the results above, decision was made to leave 2x methods uncached, and use `lru_cache(maxsize=512)` for Scale3x, and `lru_cache(maxsize=1024)` for Scale3xSFX. Note that for `lru_cache` to work pixels must be tuple[int], as provided by newest [PyPNM](https://dnyarri.github.io/pypnm.html "Pure Python module for reading, displaying and writing PPM and PGM image files") version. |
| 2026.02.12.34 | Added generalized export scheme, allowing to simplify main programs. |
| 2025.09.25.34 | Code improvements, mostly academic. Expected speed increase below limit of detection. |
| 2025.03.34 | Since 26 Mar 2025 only py34 branch, compatible with Python 3.4, will be used for publishing at PyPI; last digits "34" in version number indicate Python 3.4 compatibility. |
| 2025.02.01 | FIR optimization. Speed gain, % of original (median): ca.15% Scale2x, ca. 50% Scale3x, ca.50% Scale2xSFX, ca. 40% Scale2xSFX. |
| 2025.01.16 | Initial implementation of ScaleNxSFX. |
| 2025.01.15 | Conditional optimization. Some appends replaced with extends. |
| 2024.11.24 | Improved documentation. First publishing at PyPI. |
| 2024.10.01 | Internal restructure, imports change, maintenance release. |
| 2024.07.03 | Small improvements, one more revalidation with new test corpse, as you were, corpus. |
| 2024.05.14 | Arguments and return format changed. Incompatible with previous versions! |
| 2024.02.24 | Scale2x and Scale3x converted from standalone to module. |
| 2024.02.14 | Initial public commit of satandalone versions. |
