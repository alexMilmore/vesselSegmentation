from PyQt5.QtWidgets import *
from PyQt5.QtCore import *
from PyQt5.QtGui import QPixmap
from PIL import Image
from commonInterface import *
import scaling
import numpy as np

def runInterface(data):
    app = QApplication([]);
    window = QWidget();

    inter = interface(data);
    window.setLayout(inter.layout);
    window.resize(1480, 720)

    window.show();
    app.exec_();
    return inter.scaledData;

class interface:
    def __init__(self, data):
        # Current coords
        self.z = 0;
        self.imagesLoaded = 300
        self.data = np.array(data);
        self.scaledData = np.array(data);

        # In pyqt widgets must be stacked vertically or horizontally. To achive
        # to achive the desired layout they are stored in larger containers

        ### Basic saturaton controls
        # Create widgits
        self.saturationControl = QVBoxLayout();
        self.xControl = sliderControl("x", data.shape[0] - 1);
        self.alphaControl = sliderControl("Saturaton", 100);
        self.betaControl = sliderControl("Brightness", 100);

        # Connect widgits
        self.xControl.slider.valueChanged.connect(lambda: self.updateCoords(self.xControl.value));

        self.alphaControl.slider.valueChanged.connect( \
        lambda: self.updateSaturation(self.alphaControl.value, self.betaControl.value, \
         self.circularAlphaControl.value, self.circularBetaControl.value, self.xScaleControl.value, self.yScaleControl.value));

        self.betaControl.slider.valueChanged.connect( \
        lambda: self.updateSaturation(self.alphaControl.value, self.betaControl.value, \
         self.circularAlphaControl.value, self.circularBetaControl.value, self.xScaleControl.value, self.yScaleControl.value));

        # Create layout
        self.saturationControl.addLayout(self.xControl.layout);
        self.saturationControl.addLayout(self.alphaControl.layout);
        self.saturationControl.addLayout(self.betaControl.layout);

        ### Circular saturaton controls
        # Create widgets
        self.circularSaturationControl = QVBoxLayout();
        self.xScaleControl = sliderControl("xScale", 100);
        self.yScaleControl = sliderControl("yScale", 100);
        self.circularAlphaControl = sliderControl("Circular Saturaton", 100);
        self.circularBetaControl = sliderControl("Circular Brightness", 100);

        # Connect widgits
        self.xScaleControl.slider.valueChanged.connect( \
        lambda: self.updateSaturation(self.alphaControl.value, self.betaControl.value, \
         self.circularAlphaControl.value, self.circularBetaControl.value, self.xScaleControl.value, self.yScaleControl.value));

        self.yScaleControl.slider.valueChanged.connect( \
        lambda: self.updateSaturation(self.alphaControl.value, self.betaControl.value, \
         self.circularAlphaControl.value, self.circularBetaControl.value, self.xScaleControl.value, self.yScaleControl.value));

        self.circularAlphaControl.slider.valueChanged.connect( \
        lambda: self.updateSaturation(self.alphaControl.value, self.betaControl.value, \
         self.circularAlphaControl.value, self.circularBetaControl.value, self.xScaleControl.value, self.yScaleControl.value));

        self.circularBetaControl.slider.valueChanged.connect( \
        lambda: self.updateSaturation(self.alphaControl.value, self.betaControl.value, \
         self.circularAlphaControl.value, self.circularBetaControl.value, self.xScaleControl.value, self.yScaleControl.value));

        # Create layout
        self.circularSaturationControl.addLayout(self.xScaleControl.layout);
        self.circularSaturationControl.addLayout(self.yScaleControl.layout);
        self.circularSaturationControl.addLayout(self.circularAlphaControl.layout);
        self.circularSaturationControl.addLayout(self.circularBetaControl.layout);

        ### Connect saturation and circular saturation layouts
        self.allSaturations = QHBoxLayout();
        self.allSaturations.addLayout(self.saturationControl);
        self.allSaturations.addLayout(self.circularSaturationControl);

        ### Display image
        self.image = QLabel("loop");
        self.pixmap = QPixmap('Flamboyant_Potato.jpg');
        self.image.setPixmap(self.pixmap);

        ### Connect image to control layouts
        self.layout= QVBoxLayout();
        self.layout.addWidget(self.image);
        self.layout.addLayout(self.allSaturations);

    # Updates viewpoint coordinates
    def updateCoords(self, zVal):
        self.z = zVal
        self.updateImage();

    def updateSaturation(self, alpha, beta, radAlpha, radBeta, xScale, yScale):
        self.scaledData = scaling.changeSaturation(self.data, alpha, beta, radAlpha, radBeta, xScale, yScale);
        self.updateImage();

    # Updates the image displayed
    def updateImage(self):
        self.genImage("./", self.z);
        self.pixmap = QPixmap("./workingImg.png");
        self.image.setPixmap(self.pixmap);

    def genImage(self, path, z):
        try:
            scaledLayer = self.scaledData[z];
            im = Image.fromarray(np.concatenate([self.data[z], scaledLayer], axis = 1));

            if im.mode != 'RGB':
                im = im.convert('RGB');
            im.save(path + "workingImg" + ".png");
        except:
            print("out of range of images");
