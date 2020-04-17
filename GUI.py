from UI.RAPIDS_mainWindow import Ui_MainWindow
import sys
from PySide2 import QtCore, QtWidgets, QtGui
from PySide2.QtCore import Qt
import json


CONFIG_PATH = "ferret_run.json"
KNOB_LOC = "preferences"
class UI_Controller(QtWidgets.QMainWindow):

    def __init__ (self):
        super(UI_Controller, self).__init__()
        self.ui = Ui_MainWindow()
        self.ui.setupUi(self)

        self.configPath = None
        self.ui.configPathButton.pressed.connect(self.getConfigPath)

        self.ferretPath = None
        self.ui.ferretPathButton.pressed.connect(self.getFerretPath)

        self.resultPath = None
        self.ui.resultPathButton.pressed.connect(self.getResultPath)

        self.ui.doneB.pressed.connect(self.saveConfig)

        self.knobs = list()
        self.knobLabels = list()
        self.submatrixLabels = list()

        self.configs = None


    def updatePrefrences(self):
        if self.configs == None:
            print("load configs first!")
            return
        knob_name = self.sender().objectName()
        self.configs[KNOB_LOC][knob_name] = self.sender().value()


    def saveConfig(self):
        if self.configs == None:
            print("load configs first!")
            return

        with open(self.configDir, 'w') as confFile:
            json.dump(self.configs, confFile)

    def loadKnobs(self):
        if KNOB_LOC not in self.configs:
            return
        MIN_VAL = 1
        MAX_VAL = 100
        self.knobs = list()
        for i, knob_name in enumerate(self.configs[KNOB_LOC]):
            print(knob_name)
            # Labels showing which knob is which prefrence
            self.knobLabels.append(QtWidgets.QLabel())
            self.knobLabels[i].setText(knob_name)
            self.knobLabels[i].setAlignment(Qt.AlignCenter|Qt.AlignBottom)
            # Labels corresponding to submatrics for knobs
            self.submatrixLabels.append(QtWidgets.QLabel())
            self.submatrixLabels[i].setText("{} submatrics: x%".format(knob_name))
            self.submatrixLabels[i].setAlignment(Qt.AlignCenter)

            self.knobs.append(QtWidgets.QDial())
            self.knobs[i].setObjectName(knob_name)   #used to get the object later
            self.knobs[i].setMaximum(MAX_VAL)
            self.knobs[i].setMinimum(MIN_VAL)
            value_in_config = self.configs[KNOB_LOC][knob_name]
            if value_in_config > MAX_VAL:
                self.knobs[i].setValue(MAX_VAL)
            elif value_in_config < MIN_VAL:
                self.knobs[i].setValue(MIN_VAL)
            else:
                self.knobs[i].setValue(value_in_config)
            
            self.knobs[i].valueChanged.connect(self.updatePrefrences)

            self.ui.submetricLayout.addWidget(self.submatrixLabels[i])
            self.ui.knobNameLayout.addWidget(self.knobLabels[i])
            self.ui.knobsLayout.addWidget(self.knobs[i])

            self.knobLabels[i].show()
            self.knobs[i].show()

    def loadConfig(self):
        with open(self.configDir, 'r') as confFile:
            self.configs = json.load(confFile)
            self.loadKnobs()

    # TODO: makesure the returned path is nonempty
    def getFerretPath(self):
        path = QtWidgets.QFileDialog.getExistingDirectory()

        print("ferret directory: " + str(path))
        self.ferretPath = path

    # TODO: makesure the returned path is nonempty
    def getConfigPath(self):
        path = QtWidgets.QFileDialog.getOpenFileName()

        print("config directory: " + str(path))
        if path[0] != "" or path[0] != None:
            self.configDir = path[0]
            self.loadConfig()
        else:
            self.configDir = None


    # TODO: makesure the returned path is nonempty
    def getResultPath(self):
        path = QtWidgets.QFileDialog.getSaveFileName()

        print("result directory: " + str(path))
        self.resultPath = path[0]






if __name__ == "__main__":
    app = QtWidgets.QApplication(sys.argv)

    window = UI_Controller()
    window.show()

    sys.exit(app.exec_())