import numpy as np
import cv2
import math
from PIL import Image
import matplotlib.pyplot as plt

# Changes image saturaton/brightness proportianal to the distance from the centre
def changeSaturation(data, alpha, beta, radAlpha, radBeta, xScale, yScale):
    scaledData = np.zeros(data.shape);
    shape = (data.shape[1], data.shape[2]);

    circFilter = createGaussianFilter((data.shape[1], data.shape[2]), xScale, yScale);

    # filter
    for i in range (0, data.shape[0]):
        if (data[i].max() != 0):

            # Linear scaleing
            if (alpha == 0):
                alphaVal = float(1)/100;
            else:
                alphaVal = float(alpha)/100;
            scaledData[i] = cv2.multiply(alphaVal, data[i], dtype = cv2.CV_16U);


            # Radial scaling
            if (radAlpha == 0):
                radAlphaVal = float(1)/100;
            else:
                radAlphaVal = float(radAlpha)/100;

            scaledData[i] += cv2.multiply(circFilter * radAlphaVal, data[i], dtype = cv2.CV_16U);

            # Linear Brightness
            scaledData[i] = cv2.add(beta, scaledData[i]);

            # Radial Brightness
            scaledData[i] = cv2.add(circFilter * float(radBeta), scaledData[i], dtype = cv2.CV_16U);

    return scaledData;

def createGaussianFilter(shape, sigmaX, sigmaY):
    gaussX = cv2.getGaussianKernel(shape[1] + 1 , sigmaX);
    gaussX = np.delete(gaussX, gaussX.size - 1);
    gaussY = cv2.getGaussianKernel(shape[1] + 1 , sigmaY);
    gaussY = np.delete(gaussY, gaussY.size - 1);

    gaussKern = np.outer(gaussX, gaussY);
    gaussKern = (1/gaussKern.max())*gaussKern;
    gaussKern = np.ones(gaussKern.shape) - gaussKern

    return gaussKern
