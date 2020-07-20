import numpy as np
import cv2
import math
from PIL import Image
import matplotlib.pyplot as plt

def createGaussianFilter(shape, sigmaX, sigmaY):
    gaussX = cv2.getGaussianKernel(shape[1] + 1 , sigmaX);
    gaussX = np.delete(gaussX, gaussX.size - 1);
    gaussY = cv2.getGaussianKernel(shape[1] + 1 , sigmaY);
    gaussY = np.delete(gaussY, gaussY.size - 1);

    gaussKern = np.ones(shape)
    gaussKern = np.outer(gaussX, gaussY);
    print(gaussKern.shape)
    print(gaussKern.max())
    return gaussKern

gaussy = createGaussianFilter((64,64), 5, 8);

plt.imshow(gaussy, interpolation='none')
plt.show()
print('done')
