import cv2
import numpy as np
from PIL import Image
import math
import os

##### Generates multiple MIP projections from a single piece of 3D data.
##### This is done because lots of data is required to train a neural network.
##### This is a cheap way to increase the amount of data.


### Generate multiple MIPS from same data
def genMIPs(data, cutoff, parentMIP):
    MIPs = []

    for i in range(0, 2):
        flippedData = flipStack(data, i);
        for j in range(0,4):
            rotData = rotateStack(flippedData, j);
            MIP = genMIP(rotData, 0);

            MIPs.append(MIP);
            #MIPs.append(cv2.threshold(MIP, cutoff, 255, cv2.THRESH_BINARY)[1])

    comparison = np.concatenate((parentMIP[0], MIPs[0]), axis = 1);
    #MIPs.append(comparison);

    ### Generate comparison image
    # Find corresponding MIP image


    # create comparison

    return MIPs;


def findParentMip(dataName, parentData):
    found = False

    for filename in os.listdir(parentData):
        if (dataName in filename) and ("MIPs" in filename):
            comparMIP = Image.open(parentData + "/" + filename);
            parentMIP = np.array(comparMIP);
            # turned into 3d array so scaling function can process
            parentMIP = np.array([parentMIP]);
            return parentMIP;
            found = True
    if (found == False):
        print("corresponding MIP; " + dataName + " cound not be found")

    return np.zeros((400,400));

### Genarate mips
def genMIP(data, mode):
    # xMIP (top view)
    shape = data.shape
    xMIP = np.zeros(data[0].shape);

    for i in range(0, shape[1]):
        for j in range(0, shape[2]):
            xMIP[i][j] = data[:, i, j].max();
    xMIP = xMIP*255/xMIP.max();

    if (mode == 0):
        # yMIP (side view)
        yMIP = np.zeros([shape[0],shape[1]]);
        for i in range(0, shape[0]):
            for j in range(0, shape[2]):
                yMIP[i][j] = data[i, :, j].max();
        yMIP = yMIP*255/(yMIP.max()+1);

        # zMIP (side view)
        zMIP = np.zeros([shape[0],shape[2]]);
        for i in range(0, shape[0]):
            for j in range(0, shape[1]):
                zMIP[i][j] = data[i, j, :].max();
        zMIP = zMIP*255/(zMIP.max()+1);

        ### Put MIPs together
        MIP = np.concatenate((xMIP, yMIP), axis = 0);
        buffer = np.zeros([shape[0], shape[0]]);
        zMIP = np.concatenate((zMIP, buffer), axis = 1);
        MIP = np.concatenate((MIP,np.transpose(zMIP)), axis = 1);

        return MIP;
    return xMIP;


### Genarate projections
def genProjection(data, mode):
    # xMIP (top view)
    shape = data.shape
    xMIP = np.zeros([shape[1],shape[2]]);
    for i in range(0, shape[0]):
        xMIP = np.add(xMIP, data[i]);
    xMIP = xMIP*255/xMIP.max();

    if (mode == 0):
        # yMIP (side view)
        yMIP = np.zeros([shape[0],shape[1]]);
        for i in range(0, shape[2]):
            yMIP = np.add(yMIP, data[:,i,:]);
        yMIP = yMIP*255/yMIP.max();

        # zMIP (side view)
        zMIP = np.zeros([shape[0],shape[2]]);
        for i in range(0, shape[1]):
            zMIP = np.add(zMIP, data[:,:,i]);
        zMIP = zMIP*255/zMIP.max();

        ### Put MIPs together
        MIP = np.concatenate((xMIP, yMIP), axis = 0);
        buffer = np.zeros([shape[0], shape[0]]);
        zMIP = np.concatenate((zMIP, buffer), axis = 1);
        MIP = np.concatenate((MIP,np.transpose(zMIP)), axis = 1);

        return MIP;
    return xMIP;


### Transformations that can be applied to the data to generate different MIPs
def rotateStack(data, n):
    newData = np.zeros(data.shape);
    for i in range(0, data.shape[0]):
        newData[i] = np.rot90(data[i], n);

    return newData;

def flipStack(data, n):
    newData = np.zeros(data.shape);
    for i in range(0, data.shape[0]):
        if (n == 0):
            return data;
        if (n == 1):
            newData[i] = np.flip(data[i], axis = 0);
        if (n == 2):
            newData[i] = np.flip(data[i], axis = 1);
        if (n == 3):
            newData[i] = np.flip(data[i], axis = 0);
            newData[i] = np.flip(newData[i], axis = 1);

    return newData;
