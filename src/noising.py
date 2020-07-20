import numpy as np
import cv2
import math
from tqdm import tqdm

# Uses opencv's fasfNlMeansDenoising algorithm
def noiseFilter(data, hVal, noiseTemplateSize, noiseSearchSize):
    print ("denoising");
    noisedData = np.zeros(data.shape)

    for i in tqdm(range(0, data.shape[0])):
        if (data[i].max() != 0):
            uint8Data = cv2.convertScaleAbs(data[i]);
            noisedData[i] = cv2.fastNlMeansDenoising(uint8Data, hVal, noiseTemplateSize);
    print("noise removed");

    return noisedData;
