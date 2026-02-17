# ScaleNx

[ScaleNx](https://dnyarri.github.io/scalenx.html) is a pure Python module for pixel image rescaling using Scale2x, Scale3x, Scale2xSFX and Scale3xSFX algorithms.

Current changelog is related to ScaleNx module, not the main GUI shell. Main GUI shell gets updated more frequently and without notice.

## Version

Current changelog is related to [ScaleNx main branch for Python >= 3.10](https://github.com/Dnyarri/PixelArtScaling). For extended compatibility version see [ScaleNx py34 branch for Python >= 3.4](https://github.com/Dnyarri/PixelArtScaling/tree/py34).

## Downloads

1. [ScaleNx main branch for Python >= 3.10](https://github.com/Dnyarri/PixelArtScaling)
2. [ScaleNx py34 branch for Python >= 3.4](https://github.com/Dnyarri/PixelArtScaling/tree/py34)
3. [ScaleNx py34 at PyPI](https://pypi.org/project/ScaleNx/)

## History

| Version | Changes |
| :--- | :--- |
| 2026.02.16.16 | Module export/import generalized to simplify usage; main programs modified to illustrate new import scheme. |
| 2025.11.15.01 | Some module restructure, more helpful docstrings. |
| 2025.09.25.09 | Code improvements, mostly academic. Expected speed increase below limit of detection. |
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
