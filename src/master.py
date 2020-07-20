import tiffImport
import scalingInterface
import scaling
import noisingInterface
import noising
import findVesselsInterface
import findVessels
import mipGen
import save
import os
import sys

folderPath = "/imageData";

for fileTree in os.walk(folderPath):
    for filename in fileTree[2]:
        try:
            if "800nm_sweep" in filename:
                filepath = fileTree[0] + "/" + filename;
                print("Valid File found")
                print(filepath);

                ### Import .tiff imges
                data = tiffImport.readTiff(filepath, 800);

                ### Remove junk images

                ### Scale images
                ## With interface
                data = scalingInterface.runInterface(data);
                ## Without interface
                # data, alpha, beta, radAlpha, radBeta, xScale, yScale
                #data = scaling.changeSaturation(data, 20, 0, 0, 0, 0, 0);
                '''
                ### Noise filter images
                ## With interface
                #data = noisingInterface.runInterface(data);
                ## Without interface
                data = noising.noiseFilter(data, 10, 7, 14);

                ### Find blood vessels
                ## With interface
                data = findVesselsInterface.runInterface(data);
                ## Without interface
                #data = findVessels.findVessels(data, 6, 20, 30, 2, "Circle", 10, 5);


                ### Create MIPs
                dataName = filename[0:13];
                parentMIP = mipGen.findParentMip(dataName, fileTree[0]);
                #parentMIP = scaling.changeSaturation(parentMIP, 8, 0, 0, 0, 50, 50);
                MIPs = mipGen.genMIPs(data, 60, parentMIP);

                ### Save images
                save.saveData(data, MIPs, "../", filename);
                '''
            else:
                print ("ignored; " + filename);
        except:
            print("failed to load: " + filename)


print("done");
