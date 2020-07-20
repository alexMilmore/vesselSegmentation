import cv2
import numpy as np
from PIL import Image
import math

# current best constants; kernel = 5, hi = 30, lo = 20, erosionCount = 2

# Finds the blood vessels in an image
def findVessels(data, kernelSize, cannyThreshLo, cannyThreshHi, \
erosionCount, kernel, lengthThreshold, iterations):
    newData = np.zeros(data.shape);

    for j in range(0, data.shape[0]):
        if (data[j].max() != 0):
            shape = data[j].shape
            imageData = data[j];

            # Edge detection with several different kernels
            imageEdges =  np.zeros(shape);

            confidenceMap = np.zeros(shape, dtype = np.float);

            circKernel = circleKern((kernelSize, kernelSize), kernelSize/2);


            for iteration in range(0, int(iterations)):
                imageEdges = erodeImage(imageData, "Circle");

                # Find edges with Canny and clean up with a closing operation
                imageEdges = cv2.Canny(np.array(imageData, dtype = np.uint8), cannyThreshLo, cannyThreshHi);
                imageEdges = cv2.morphologyEx(imageEdges, cv2.MORPH_CLOSE, circKernel, iterations=erosionCount);

                # add grading of confidence by length of contour & poximity to contents
                confidenceMap = imageEdges/np.max(imageEdges)*iteration*20;

            # Threshold a specific certainty
            confidenceMap = cv2.threshold(confidenceMap, 110, 255, cv2.THRESH_BINARY)[1];

            confidenceMap = cv2.morphologyEx(confidenceMap, cv2.MORPH_CLOSE, circKernel);
            confidenceMap = cv2.morphologyEx(confidenceMap, cv2.MORPH_OPEN, \
            circleKern((kernelSize/2,kernelSize/2), kernelSize/4), iterations = 3);

            newData[j] = confidenceMap;
        print("Vessels isolated in layer " + str(j));

    return newData;

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
        newData = np.zeros(data.shape);

        # Iterate over every image in data array
        for j in range(0, data.shape[0]):
            # check if empty
            if (data[j].max() != 0):
                shape = data[j].shape;
                imageData = data[j];

                # Edge detection with morphological erosions
                imageEdges =  np.zeros(shape);

                #confidenceMap = np.zeros(shape, dtype = np.float);

                circKernel = circleKern((kernelSize, kernelSize), kernelSize/2);

                # 1st pass with a threshold function
                confidenceMap = cv2.threshold(data[j], 110, 255, cv2.THRESH_BINARY)[1])

                for iteration in range(0, int(iterations)):
                    if (kernel == "Circle"):
                        imageData = cv2.erode(imageData, circKernel);
                    elif (kernel == "Gauss"):
                        imageData = gaussianErosion(gaussData, 5, 10, 10);
                    else:
                        print("Unregognised kernel setting");

                    # Find edges with Canny and clean up with a closing operation
                    imageEdges = cv2.Canny(np.array(imageData, dtype = np.uint8), cannyThreshLo, cannyThreshHi);
                    imageEdges = cv2.morphologyEx(imageEdges, cv2.MORPH_CLOSE, circKernel, iterations=erosionCount);

                    # add grading of confidence by length of contour & poximity to contents
                    confidenceMap = imageEdges/np.max(imageEdges)*iteration*20;

                # Threshold a specific certainty
                confidenceMap = cv2.threshold(confidenceMap, 110, 255, cv2.THRESH_BINARY)[1];

                # Clean up artifacts with a few morphology functions
                confidenceMap = cv2.morphologyEx(confidenceMap, cv2.MORPH_CLOSE, circKernel);
                confidenceMap = cv2.morphologyEx(confidenceMap, cv2.MORPH_OPEN, \
                circleKern((kernelSize/2,kernelSize/2), kernelSize/4), iterations = 3);

                newData[j] = confidenceMap;
            print("Vessels isolated in layer " + str(j));

        return newData;

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
