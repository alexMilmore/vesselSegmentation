from PyQt5.QtWidgets import *
from PyQt5.QtCore import *
from PyQt5.QtGui import QPixmap
from PIL import Image
import numpy as np
from commonInterface import *
import findVessels


def runInterface(data):
    app = QApplication([]);
    window = QWidget();

    inter = interface(data);
    window.setLayout(inter.layout);
    window.resize(1480, 720)

    window.show();
    app.exec_();
    return inter.segmentedData;

class interface:
    def __init__(self, data):
        # Current coords
        self.z = 0;
        self.imagesLoaded = 300
        self.data = np.array(data, np.uint16);
        self.edgeMap = np.array(data, np.uint16);
        self.segmentedData = np.array(data);

        # In pyqt widgets must be stacked vertically or horizontally. To achive
        # to achive the desired layout they are stored in larger containers

        ### Basic controls
        # Create widgits
        self.xControl = sliderControl("x", data.shape[0] - 1);
        self.initalThresh = sliderControl("Initial threshold", 255);
        self.finalThresh = sliderControl("Final threshold", 255);

        # Connect widgits
        self.xControl.slider.valueChanged.connect(lambda: self.updateCoords(self.xControl.value));
        self.initalThresh.slider.valueChanged.connect(lambda: self.updateThresholds(self.initalThresh.value, self.finalThresh.value));
        self.finalThresh.slider.valueChanged.connect(lambda: self.updateThresholds(self.initalThresh.value, self.finalThresh.value));

        # Create layout
        self.basicControls = QVBoxLayout();
        self.basicControls.addLayout(self.xControl.layout);
        self.basicControls.addLayout(self.initalThresh.layout);
        self.basicControls.addLayout(self.finalThresh.layout);

        ### Erosion iteration controls (for opencv's fastNlMeansDenoising)
        # Create widgets
        self.kernelSize = labeledEdit("Kernel size");
        self.cannyHiThresh = labeledEdit("Canny edge detection high threshold")
        self.cannyLoThresh = labeledEdit("Canny edge detect low threshold");
        self.erosionCount = labeledEdit("Number of erosion steps")
        self.contourLengthThresh = labeledEdit("Min contour length");
        self.iterations = labeledEdit("Number of iterations");
        self.segmentButton = QPushButton("Segment data");

        #  Connect widgets
        self.segmentButton.clicked.connect(lambda: self.updateEdgeMap( \
        self.kernelSize.getVal(), self.cannyLoThresh.getVal(), self.cannyHiThresh.getVal(), \
        self.erosionCount.getVal(), "Circle", self.iterations.getVal(), \
        self.initalThresh.value, self.finalThresh.value));

        # Create layout
        self.segmentationControls = QVBoxLayout();
        self.segmentationControls.addLayout(self.kernelSize.layout);
        self.segmentationControls.addLayout(self.cannyHiThresh.layout);
        self.segmentationControls.addLayout(self.cannyLoThresh.layout);
        self.segmentationControls.addLayout(self.erosionCount.layout);
        self.segmentationControls.addLayout(self.contourLengthThresh.layout);
        self.segmentationControls.addLayout(self.iterations.layout);
        self.segmentationControls.addWidget(self.segmentButton);

        ### Connect noise filter to saturatoin layout
        self.filterPanel = QHBoxLayout();
        self.filterPanel.addLayout(self.basicControls);
        self.filterPanel.addLayout(self.segmentationControls);

        ### Allow cleaned files to be saved
        # Create widgets
        self.savePathSelect = labeledEdit("Save path");
        self.saveButton = QPushButton("Save");
        self.startPoint = labeledEdit("Start");
        self.endPoint = labeledEdit("End");


        ### Display image
        self.image = QLabel("loop");
        self.pixmap = QPixmap('Flamboyant_Potato.jpg');
        self.image.setPixmap(self.pixmap);

        ### Connect image to control layouts
        self.layout = QVBoxLayout();
        self.layout.addWidget(self.image);
        self.layout.addLayout(self.filterPanel);


    # Updates viewpoint coordinates
    def updateCoords(self, zVal):
        self.z = zVal;
        self.updateImage();

    def updateEdgeMap(self, kernelSize, cannyThreshLo, cannyThreshHi, \
    erosionCount, kernel, iterations, initialThreshold, finalThreshold):
        # Update classes' edgemap
        self.edgeMap = findVessels.generateConfidencemap( \
        self.data, kernelSize, cannyThreshHi, cannyThreshLo, \
        erosionCount, kernel, iterations);
        # Generate new segmented data so image is changed
        self.segmentedData = findVessels.generateSegmentedImage(self.data, self.edgeMap, initialThreshold, finalThreshold);
        self.updateImage();

    def updateThresholds(self, initialThreshold, finalThreshold):
        self.segmentedData = findVessels.generateSegmentedImage(self.data, self.edgeMap, initialThreshold, finalThreshold);
        self.updateImage();

    # Updates the image displayed
    def updateImage(self):
        self.genImage("./", self.z);
        self.pixmap = QPixmap("./workingImg.png");
        self.image.setPixmap(self.pixmap);

    def genImage(self, path, z):
        #try:
        # Create base
        composite = Image.new('RGB', (self.data[z].shape[0]*2, self.data[z].shape[1]))

        # Create images
        originalData = Image.fromarray(self.data[z]);
        originalData = originalData.convert('RGB');
        segmentedLayer = Image.fromarray(self.segmentedData[z]);
        segmentedLayer = segmentedLayer.convert('RGB');
        mask = Image.fromarray(self.segmentedData[z]);
        mask = mask.convert('L');

        # convert segmented layer to red
        matrix = (1.0, 0.0, 0.0, 0.0,   0.0, 0.0, 0.0, 0.0,   0.0, 0.0, 0.0, 0.0);
        segmentedLayer = segmentedLayer.convert('RGB',matrix);

        # paste images together
        composite.paste(originalData, (0, 0));
        composite.paste(originalData, (self.data[z].shape[0], 0));
        composite.paste(segmentedLayer, (self.data[z].shape[0], 0), mask);

        composite.save(path + "workingImg" + ".png");
        #except:
            #print("out of range of images");
            #print(self.data.shape);
