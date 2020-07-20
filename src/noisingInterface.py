from PyQt5.QtWidgets import *
from PyQt5.QtCore import *
from PyQt5.QtGui import QPixmap
from PIL import Image
import numpy as np
from commonInterface import *
import noising


def runInterface(data):
    app = QApplication([]);
    window = QWidget();

    inter = interface(data);
    window.setLayout(inter.layout);
    window.resize(1480, 720)

    window.show();
    app.exec_();
    return inter.noisedData;

class interface:
    def __init__(self, data):
        # Current coords
        self.z = 0;
        self.imagesLoaded = 300
        self.data = np.array(data, np.uint16);
        self.noisedData = np.array(data);

        # In pyqt widgets must be stacked vertically or horizontally. To achive
        # to achive the desired layout they are stored in larger containers


        ### Basic saturaton controls
        # Create widgits
        self.xControl = sliderControl("x", data.shape[0] - 1);

        # Connect widgits
        self.xControl.slider.valueChanged.connect(lambda: self.updateCoords(self.xControl.value));

        ### Noise filtering controls (for opencv's fastNlMeansDenoising)
        # Create widgets
        self.noiseHVal = labeledEdit("h value");
        self.noiseTemplateWindowSize = labeledEdit("Template window size")
        self.noiseSearchWindowSize = labeledEdit("Search window size");
        self.denoiseButton = QPushButton("denoise");

        #  Connect widgets
        self.denoiseButton.clicked.connect(lambda: self.updateFilter(self.noiseHVal.getVal(), self.noiseTemplateWindowSize.getVal(), self.noiseSearchWindowSize.getVal()));

        # Create layout
        self.noiseControls = QVBoxLayout();
        self.noiseControls.addLayout(self.noiseHVal.layout);
        self.noiseControls.addLayout(self.noiseTemplateWindowSize.layout);
        self.noiseControls.addLayout(self.noiseSearchWindowSize.layout);
        self.noiseControls.addWidget(self.denoiseButton);

        ### Connect noise filter to saturatoin layout
        self.filterPanel = QVBoxLayout();
        self.filterPanel.addLayout(self.xControl.layout);
        self.filterPanel.addLayout(self.noiseControls);

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
        self.z = zVal
        self.updateImage();

    # applies noise cut filter to images
    def updateFilter(self, hVal, noiseTemplateSize, noiseSearchSize):
        self.noisedData = noising.noiseFilter(self.data, hVal, noiseTemplateSize, noiseSearchSize);
        self.updateImage();

    # Updates the image displayed
    def updateImage(self):
        self.genImage("./", self.z);
        self.pixmap = QPixmap("./workingImg.png");
        self.image.setPixmap(self.pixmap);

    def genImage(self, path, z):
        try:
            noisedLayer = self.noisedData[z];
            im = Image.fromarray(np.concatenate([self.data[z], noisedLayer], axis = 1));

            if im.mode != 'RGB':
                im = im.convert('RGB');
            im.save(path + "workingImg" + ".png");
        except:
            print("out of range of images");
