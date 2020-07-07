# Vessel Segmentation
Isolates blood vessel from .tiff image stacks produced by photoacoustic scans. Was designed to allow accurate segmentation on noisy image sets. Works in 3 steps:

1) Changes brightness & saturation in image to make blood vessels clearer.
2) Runs a noising algorihm to remove random noise
3) Uses edge detection & morphologicl funcitions to find the blood vessels
