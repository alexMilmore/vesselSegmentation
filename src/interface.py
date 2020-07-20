from PyQt5.QtWidgets import *
from PyQt5.QtCore import *
from PyQt5.QtGui import QPixmap
from viewer import viewer
from PIL import Image

app = QApplication([]);
window = QWidget();

#pyQT compound widget
#A slider with a text box that displays the slider's current value,
#The value can also be set through the text box
class sliderControl:
    def __init__(self, label, max):
        # Value stored by this compound widgit
        self.value = 0;

        # Create slider and text label
        self.slider = QSlider(Qt.Horizontal);
        self.editLabel = QLineEdit();

        # Edit slider
        self.slider.setMaximum(max);

        # Connect slider and label together
        self.slider.valueChanged.connect(self.updateSlider);
        self.editLabel.editingFinished.connect(self.updateLabel);


        # Sets layout of different controls in window
        self.controls = QHBoxLayout();
        self.controls.addWidget(self.slider);
        self.controls.addWidget(self.editLabel);
        self.layout = QVBoxLayout();
        self.layout.addWidget(QLabel(label));
        self.layout.addLayout(self.controls);

    # Allows slider to change view and label
    def updateSlider(self):
        self.value = self.slider.value();
        self.editLabel.setText(str(self.value));

    # Allows label to change view and slider
    def updateLabel(self):
        if (self.editLabel.text() != ''):
            self.value = int(self.editLabel.text());
            self.slider.setValue(self.value);
        else:
            self.value = 0;
            self.slider.setValue(0);

    # Returns the controller's value
    def getVal(self):
        return self.slider.value()

class labeledEdit:
    def __init__(self, text):
        self.label = QLabel(text);
        self.edit = QLineEdit();

        self.layout = QHBoxLayout();
        self.layout.addWidget(self.label);
        self.layout.addWidget(self.edit);

    def getVal(self):
        return int(self.edit.text());

    def getText(self):
        return self.edit.text();

class interface:
    def __init__(self):
        # Current coords
        self.z = 0;
        self.imagesLoaded = 300


        # In pyqt widgets must be stacked vertically or horizontally. To achive
        # to achive the desired layout they are stored in larger containers

        ### Create viewport
        self.viewport = viewer("/home/alex/Documents/Uni/Project/data/HV01/HV01-B1_800nm_sweep006.tiff", self.imagesLoaded);

        ### Basic saturaton controls
        # Create widgits
        self.saturationControl = QVBoxLayout();
        self.xControl = sliderControl("x", self.viewport.layers - 1);
        self.alphaControl = sliderControl("Saturaton", 100);
        self.betaControl = sliderControl("Brightness", 100);

        # Connect widgits
        self.xControl.slider.valueChanged.connect(lambda: self.updateCoords(self.xControl.value));
        self.alphaControl.slider.valueChanged.connect(lambda: self.updateSaturation(self.alphaControl.value, self.betaControl.value));
        self.betaControl.slider.valueChanged.connect(lambda: self.updateSaturation(self.alphaControl.value, self.betaControl.value));

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
        self.xScaleControl.slider.valueChanged.connect(lambda: self.updateCircularSaturation(self.circularAlphaControl.value, self.circularBetaControl.value, self.xScaleControl.value, self.yScaleControl.value));
        self.yScaleControl.slider.valueChanged.connect(lambda: self.updateCircularSaturation(self.circularAlphaControl.value, self.circularBetaControl.value, self.xScaleControl.value, self.yScaleControl.value));
        self.circularAlphaControl.slider.valueChanged.connect(lambda: self.updateCircularSaturation(self.circularAlphaControl.value, self.circularBetaControl.value, self.xScaleControl.value, self.yScaleControl.value));
        self.circularBetaControl.slider.valueChanged.connect(lambda: self.updateCircularSaturation(self.circularAlphaControl.value, self.circularBetaControl.value, self.xScaleControl.value, self.yScaleControl.value));

        # Create layout
        self.circularSaturationControl.addLayout(self.xScaleControl.layout);
        self.circularSaturationControl.addLayout(self.yScaleControl.layout);
        self.circularSaturationControl.addLayout(self.circularAlphaControl.layout);
        self.circularSaturationControl.addLayout(self.circularBetaControl.layout);

        ### Connect saturation and circular saturation layouts
        self.allSaturations = QHBoxLayout();
        self.allSaturations.addLayout(self.saturationControl);
        self.allSaturations.addLayout(self.circularSaturationControl);

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
        self.filterPanel.addLayout(self.allSaturations);
        self.filterPanel.addLayout(self.noiseControls);

        ### Allow files to be loaded
        # Create widgets
        self.loadPath = QLineEdit();
        self.loadButton = QPushButton("load");
        self.loadLabel = QLabel("Images filepath");

        # Connect widgets
        self.loadButton.clicked.connect(lambda: self.load(self.loadPath.text(), self.imagesLoaded))

        # Create layout
        self.loadLayout = QHBoxLayout();
        self.loadLayout.addWidget(self.loadLabel);
        self.loadLayout.addWidget(self.loadPath);
        self.loadLayout.addWidget(self.loadButton);

        ### Allow cleaned files to be saved
        # Create widgets
        self.savePathSelect = labeledEdit("Save path");
        self.saveButton = QPushButton("Save");
        self.startPoint = labeledEdit("Start");
        self.endPoint = labeledEdit("End");

        # Connect widgets
        self.saveButton.clicked.connect(lambda: self.saveImages(self.savePathSelect.getText(), self.startPoint.getVal(), self.endPoint.getVal()))


        # Create layout
        self.saveControlLayout = QHBoxLayout();
        self.saveControlLayout.addLayout(self.startPoint.layout);
        self.saveControlLayout.addLayout(self.endPoint.layout);
        self.saveControlLayout.addWidget(self.saveButton);

        self.saveLayout = QVBoxLayout();
        self.saveLayout.addLayout(self.savePathSelect.layout);
        self.saveLayout.addLayout(self.saveControlLayout);

        ### Display image
        self.image = QLabel("loop");
        self.pixmap = QPixmap('Flamboyant_Potato.jpg');
        self.image.setPixmap(self.pixmap);

        ### Connect image to control layouts
        self.imgControl = QHBoxLayout();
        self.imgControl.addWidget(self.image);
        self.imgControl.addLayout(self.filterPanel);

        # Full interface layout
        self.layout = QVBoxLayout();
        self.layout.addLayout(self.loadLayout);
        self.layout.addLayout(self.imgControl);
        self.layout.addLayout(self.saveLayout);


    # applies noise cut filter to images
    def updateFilter(self, hVal, noiseTemplateSize, noiseSearchSize):
        self.viewport.updateNoiseFilter(hVal, noiseTemplateSize, noiseSearchSize);
        self.updateImage();

    # Updates viewpoint coordinates
    def updateCoords(self, zVal):
        self.z = zVal
        self.updateImage();

    def updateSaturation(self, alpha, beta):
        self.viewport.updateSaturation(alpha, beta);
        self.updateImage();

    def updateCircularSaturation(self, circularAlpha, circularBeta, xScale, yScale):
        self.viewport.updateCircularSaturation(circularAlpha, circularBeta, xScale, yScale);
        self.updateImage();

    def thresholdSwitch(self):
        self.viewport.filter.thresholdSwitch();
        self.updateImage();

    # Updates the image displayed
    def updateImage(self):
        self.viewport.genImage("./", self.z);
        self.pixmap = QPixmap("./workingImg.png");
        self.image.setPixmap(self.pixmap);

    # Loads new images
    def load(self,path, maxImages):
        self.viewport.load(self.loadPath.text(), self.imagesLoaded);
        self.xControl.slider.setMaximum(self.viewport.layers - 1);

    # Saves the cleaned images
    def saveImages(self, path, start, end):
        for i in range(start, end):
            print("Saved " + str(i));
            im = Image.fromarray(self.viewport.filter.getLayerData(i));

            if im.mode != 'RGB':
                im = im.convert('RGB');
            im.save(path + "/layer_" + str(i) + ".png");

    # Changes the display mode of the viewer
    # 0) regular
    # 1) edge detect
    def changeMode(self):
        self.mode = self.mode + 1;
        if (self.mode > 1):
            self.mode = 0;

def runInterface():
    inter = interface();
    window.setLayout(inter.layout);
    window.resize(720, 360)

    window.show();
    app.exec_();
