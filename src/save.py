import os
from PIL import Image
import numpy as np
from tqdm import tqdm

def saveData(tiffData, mipData, savePath, name):
    print("Saving data")
    # Create directory for images
    path = savePath + "/" + name + "_Data";
    os.mkdir(path);

    '''
    # Save .tiff data images
    tiffPath = path + "/" + "tiffData";
    os.mkdir(tiffPath);

    for i in tqdm(range(0, tiffData.shape[0])):
        im = Image.fromarray(tiffData[i]);

        if im.mode != 'RGB':
            im = im.convert('RGB');
        im.save(tiffPath + "/layer_" + str(i) + ".png");
    '''

    # Save MIP data
    mipPath = path + "/" + "mipData";
    os.mkdir(mipPath);
    for i in tqdm(range(0, len(mipData))):
        im = Image.fromarray(mipData[i]);

        if im.mode != 'RGB':
            im = im.convert('RGB');
        im.save(mipPath + "/MIP_" + str(i) + ".png");
