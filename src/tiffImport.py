from PIL import Image
import numpy as np
import cv2

# Read .tiff images into a numpy array, this is done using a mix of PIL to find
#
def readTiff(path, validThreshold):
    """
        path - Path to the multipage-tiff file
        nImages - Number of pages in the tiff file
        validThreshold - pixel intensity requred to be a valid reading. This was
                        included because many files have long starts without valid
                        readings, usually use 500
    """
    img = Image.open(path);
    images = [];

    validStart = False;
    lastMax = 0;

    for i in range(10000):
        try:
            img.seek(i);
            imgData = np.array(img);


            images.append(imgData);

        except EOFError:
            # Not enough frames in img
            break

    return np.array(images);
