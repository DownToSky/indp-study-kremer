from UI.RAPIDS_mainWindow import Ui_MainWindow
import sys
from PySide2 import QtCore, QtWidgets, QtGui
from PySide2.QtUiTools import QUiLoader
import json

CONFIG_PATH = "ferret_run.json"
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


    # TODO: makesure the returned path is nonempty
    def getFerretPath(self):
        path = QtWidgets.QFileDialog.getExistingDirectory()

        print("ferret directory: " + str(path))
        self.ferretPath = path

    # TODO: makesure the returned path is nonempty
    def getConfigPath(self):
        path = QtWidgets.QFileDialog.getOpenFileName()

        print("config directory: " + str(path))
        self.configDir = path[0]

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