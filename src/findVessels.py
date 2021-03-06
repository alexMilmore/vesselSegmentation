import cv2
import numpy as np
from PIL import Image
import math
import matplotlib.pyplot as plt

# current best constants; kernel = 5, hi = 30, lo = 20, erosionCount = 2

# Erodes image with different possible kernels
def erodeImage(data, kernelType):
    imageData = np.zeros(data.shape);
    kernelSize = 3
    circKernel = circleKern((kernelSize, kernelSize), kernelSize/2);

    if (kernelType == "Circle"):
        imageData = cv2.erode(imageData, circKernel);
    elif (kernelType == "Gauss"):
        imageData = gaussianErosion(gaussData, 5, 10, 10);
    else:
        print("Unregognised kernel setting");

    return imageData;

def generateConfidencemap(data, kernelSize, cannyThreshLo, cannyThreshHi, \
erosionCount, kernel, iterations):
    shape = data[0].shape;
    # needs to be float for nomalization, will be changed to uint8 at end
    confidenceMap = np.zeros(data.shape, dtype = np.float);

    # Edge detection with morphological erosions
    imageEdges =  np.zeros(shape);

    for j in range(0, data.shape[0]):
        imageData = np.copy(data[j]);
        circKernel = circleKern((kernelSize, kernelSize), kernelSize/2);


        for iteration in range(0, int(iterations)):
            # Choose the kernel used for this operation
            if (kernel == "Circle"):
                imageData = cv2.erode(imageData, circKernel);
            elif (kernel == "Gauss"):
                imageData = gaussianErosion(gaussData, 5, 10, 10);
            else:
                print("Unrecognised kernel setting");

            # Find edges with Canny and clean up with a closing operation
            imageEdges = cv2.Canny(np.array(imageData, dtype = np.uint8), cannyThreshLo, cannyThreshHi);
            imageEdges = cv2.morphologyEx(imageEdges, cv2.MORPH_CLOSE, circKernel, iterations=erosionCount);
            print(imageEdges.max())
            # add grading of confidence by length of contour & proximity to contents
            confidenceMap[j] += np.array(imageEdges, dtype = np.float)/(np.max(imageEdges) + 1)*iteration*20;

            '''
            plt.imshow(imageData)
            plt.show();
            plt.imshow(imageEdges);
            plt.show();
            plt.imshow(confidenceMap[j]);
            plt.show();
            '''

    print(confidenceMap.shape)

    return confidenceMap;

def generateSegmentedImage(data, edgeMap, initialThreshold, finalThreshold):
        newData = np.zeros(data.shape);
        kernelSize = 3;
        circKernel = circleKern((kernelSize, kernelSize), kernelSize/2);


        # Iterate over every image in data array
        for j in range(0, data.shape[0]):
            # check if empty
            if (data[j].max() != 0):
                shape = data[j].shape;
                imageData = data[j];

                # Use binary threshold for start point and add edge detection
                fullImage = cv2.threshold(np.array(data[j], dtype = np.uint8), initialThreshold, 255, cv2.THRESH_BINARY)[1];
                fullImage += np.array(edgeMap[j], dtype = np.uint8);
                fullImage[fullImage > 256] = 256;

                # Threshold a specific certainty
                fullImage = cv2.threshold(np.array(fullImage, dtype = np.uint8), finalThreshold, 255, cv2.THRESH_BINARY)[1];

                # Clean up artifacts with a few morphology functions
                fullImage = cv2.morphologyEx(fullImage, cv2.MORPH_CLOSE, circKernel);
                fullImage = cv2.morphologyEx(fullImage, cv2.MORPH_OPEN, \
                circleKern((kernelSize/2,kernelSize/2), kernelSize/4), iterations = 3);

                newData[j] = fullImage;
            print("Vessels isolated in layer " + str(j));

        return newData;

def generateFullSegmentedImage(data, kernelSize, cannyThreshLo, cannyThreshHi, \
erosionCount, kernel, iterations, initialThreshold, finalThreshold):
    map = generateConfidencemap(data, kernelSize, cannyThreshLo, cannyThreshHi, \
    erosionCount, kernel, iterations);
    return generateSegmentedImage(data, map, initialThreshold, finalThreshold);

def calcConfidence(edges, threshold):
    map = np.zeros(edges.shape);
    contours = cv2.findContours(edges, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE);

    # Approximate contours to remove noise
    for cnt in contours[1]:
        length = cv2.arcLength(cnt, True);
        if length < threshold:
            cv2.drawContours(map, cnt, 0, (0), 5);

    return map;

### Different kernel types
def circleKern(kernelShape, R):
    kern = np.zeros(kernelShape, dtype = np.uint8);
    centre = (kernelShape[1]/2, kernelShape[0]/2);
    # Draws a circle in the centre of the array
    cv2.circle(kern, centre, R, (255,255,255), -1);

    return kern;

# returns normalized gaussian value at x
def gaussian(x, sigma):
    gauss = 1/(sigma*math.sqrt(2*np.pi))*math.exp(-(0.5)*(x/sigma)*(x/sigma));
    return x;

def gaussKern(shape, angle, sigma):
    kern = np.zeros(shape, dtype = np.uint8);
    # calculate direction of kernel
    direction = np.array([math.cos(angle), math.sin(angle)]);

    for i in range(shape[0]):
        for j in range(shape[1]):
            vect = np.array([i - shape[0]/2, j - shape[1]/2]);
            x = np.dot(vect, direction);
            kern[i,j] = gaussian(x,sigma);

    return kern;

def gaussianErosion(img, size, numAngles, sigma):
    data = np.zeros(img.shape);

    for i in range(0,numAngles):
        kernel = gaussKern((size, size), 2*np.pi/numAngles*i, sigma);
        data += float(1)/numAngles*cv2.erode(img, kernel);

    return data;
