# ScaleNx test images

Current folder contains simple test images for ScaleNx image rescaler.

Image files are intended for both format compatibility tests and scaling artifacts detection.

Both images per se and files containing images are constructed for testing purposes. For example, all PNGs have non-square resolution, making them look weird under other software (for example, Windows Explorer). This is made to check proper resolution handling - upon rescaling PNGs are supposed to keep print size, that is, have Nx times bigger resolution. All files have useless comments, supposed to be deleted when processing. And so on.

File naming roughly follows "WIDTHxHEIGHTxBITDEPTH TYPE.extension" pattern.
