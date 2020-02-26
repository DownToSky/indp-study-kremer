from UI.RAPIDS_mainWindow import Ui_MainWindow
import sys
from PySide2 import QtCore, QtWidgets, QtGui
from PySide2.QtUiTools import QUiLoader

class UI_Controller(QtWidgets.QMainWindow):
    def __init__ (self):
        super(UI_Controller, self).__init__()
        self.ui = Ui_MainWindow()
        self.ui.setupUi(self)

if __name__ == "__main__":
    app = QtWidgets.QApplication(sys.argv)

    window = UI_Controller()
    window.show()

    sys.exit(app.exec_())