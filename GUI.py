from UI.RAPIDS_mainWindow import Ui_MainWindow
import sys
from PySide2 import QtCore, QtWidgets, QtGui
from PySide2.QtUiTools import QUiLoader
import json

CONFIG_PATH = "ferret_run.json"
class UI_Controller(QtWidgets.QMainWindow):


    def __init__ (self, config_path):
        super(UI_Controller, self).__init__()
        self.ui = Ui_MainWindow()
        self.ui.setupUi(self)
        self.config = self.loadConfig(config_path)



    def loadConfig(self, path):
        content = dict()
        with open(path, 'r') as f:
            content = json.load(f)
        return content





if __name__ == "__main__":
    app = QtWidgets.QApplication(sys.argv)

    window = UI_Controller(CONFIG_PATH)
    window.show()

    sys.exit(app.exec_())