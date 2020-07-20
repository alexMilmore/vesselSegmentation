from PyQt5.QtWidgets import *
from PyQt5.QtCore import *

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
