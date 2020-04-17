# -*- coding: utf-8 -*-

################################################################################
## Form generated from reading UI file 'RAPIDS_GUI.ui'
##
## Created by: Qt User Interface Compiler version 5.14.1
##
## WARNING! All changes made in this file will be lost when recompiling UI file!
################################################################################

from PySide2.QtCore import (QCoreApplication, QMetaObject, QObject, QPoint,
    QRect, QSize, QUrl, Qt)
from PySide2.QtGui import (QBrush, QColor, QConicalGradient, QCursor, QFont,
    QFontDatabase, QIcon, QLinearGradient, QPalette, QPainter, QPixmap,
    QRadialGradient)
from PySide2.QtWidgets import *


class Ui_MainWindow(object):
    def setupUi(self, MainWindow):
        if MainWindow.objectName():
            MainWindow.setObjectName(u"MainWindow")
        MainWindow.resize(860, 543)
        MainWindow.setStyleSheet(u"QToolTip\n"
"{\n"
"     border: 1px solid black;\n"
"     background-color: #ffa02f;\n"
"     padding: 1px;\n"
"     border-radius: 3px;\n"
"     opacity: 100;\n"
"}\n"
"\n"
"QWidget\n"
"{\n"
"    color: #b1b1b1;\n"
"    background-color: #323232;\n"
"}\n"
"\n"
"QWidget:item:hover\n"
"{\n"
"    background-color: QLinearGradient( x1: 0, y1: 0, x2: 0, y2: 1, stop: 0 #ffa02f, stop: 1 #ca0619);\n"
"    color: #000000;\n"
"}\n"
"\n"
"QWidget:item:selected\n"
"{\n"
"    background-color: QLinearGradient( x1: 0, y1: 0, x2: 0, y2: 1, stop: 0 #ffa02f, stop: 1 #d7801a);\n"
"}\n"
"\n"
"QMenuBar::item\n"
"{\n"
"    background: transparent;\n"
"}\n"
"\n"
"QMenuBar::item:selected\n"
"{\n"
"    background: transparent;\n"
"    border: 1px solid #ffaa00;\n"
"}\n"
"\n"
"QMenuBar::item:pressed\n"
"{\n"
"    background: #444;\n"
"    border: 1px solid #000;\n"
"    background-color: QLinearGradient(\n"
"        x1:0, y1:0,\n"
"        x2:0, y2:1,\n"
"        stop:1 #212121,\n"
"        stop:0.4 #343434/*,\n"
"        stop:0.2 #3"
                        "43434,\n"
"        stop:0.1 #ffaa00*/\n"
"    );\n"
"    margin-bottom:-1px;\n"
"    padding-bottom:1px;\n"
"}\n"
"\n"
"QMenu\n"
"{\n"
"    border: 1px solid #000;\n"
"}\n"
"\n"
"QMenu::item\n"
"{\n"
"    padding: 2px 20px 2px 20px;\n"
"}\n"
"\n"
"QMenu::item:selected\n"
"{\n"
"    color: #000000;\n"
"}\n"
"\n"
"QWidget:disabled\n"
"{\n"
"    color: #404040;\n"
"    background-color: #323232;\n"
"}\n"
"\n"
"QAbstractItemView\n"
"{\n"
"    background-color: QLinearGradient( x1: 0, y1: 0, x2: 0, y2: 1, stop: 0 #4d4d4d, stop: 0.1 #646464, stop: 1 #5d5d5d);\n"
"}\n"
"\n"
"QWidget:focus\n"
"{\n"
"    /*border: 2px solid QLinearGradient( x1: 0, y1: 0, x2: 0, y2: 1, stop: 0 #ffa02f, stop: 1 #d7801a);*/\n"
"}\n"
"\n"
"QLineEdit\n"
"{\n"
"    background-color: QLinearGradient( x1: 0, y1: 0, x2: 0, y2: 1, stop: 0 #4d4d4d, stop: 0 #646464, stop: 1 #5d5d5d);\n"
"    padding: 1px;\n"
"    border-style: solid;\n"
"    border: 1px solid #1e1e1e;\n"
"    border-radius: 5;\n"
"}\n"
"\n"
"QPushButton\n"
"{\n"
"    color: #b1b1b"
                        "1;\n"
"    background-color: QLinearGradient( x1: 0, y1: 0, x2: 0, y2: 1, stop: 0 #565656, stop: 0.1 #525252, stop: 0.5 #4e4e4e, stop: 0.9 #4a4a4a, stop: 1 #464646);\n"
"    border-width: 1px;\n"
"    border-color: #1e1e1e;\n"
"    border-style: solid;\n"
"    border-radius: 6;\n"
"    padding: 3px;\n"
"    font-size: 12px;\n"
"    padding-left: 5px;\n"
"    padding-right: 5px;\n"
"}\n"
"\n"
"QPushButton:pressed\n"
"{\n"
"    background-color: QLinearGradient( x1: 0, y1: 0, x2: 0, y2: 1, stop: 0 #2d2d2d, stop: 0.1 #2b2b2b, stop: 0.5 #292929, stop: 0.9 #282828, stop: 1 #252525);\n"
"}\n"
"\n"
"QComboBox\n"
"{\n"
"    selection-background-color: #ffaa00;\n"
"    background-color: QLinearGradient( x1: 0, y1: 0, x2: 0, y2: 1, stop: 0 #565656, stop: 0.1 #525252, stop: 0.5 #4e4e4e, stop: 0.9 #4a4a4a, stop: 1 #464646);\n"
"    border-style: solid;\n"
"    border: 1px solid #1e1e1e;\n"
"    border-radius: 5;\n"
"}\n"
"\n"
"QComboBox:hover,QPushButton:hover\n"
"{\n"
"    border: 2px solid QLinearGradient( x1: 0, y1: 0,"
                        " x2: 0, y2: 1, stop: 0 #ffa02f, stop: 1 #d7801a);\n"
"}\n"
"\n"
"\n"
"QComboBox:on\n"
"{\n"
"    padding-top: 3px;\n"
"    padding-left: 4px;\n"
"    background-color: QLinearGradient( x1: 0, y1: 0, x2: 0, y2: 1, stop: 0 #2d2d2d, stop: 0.1 #2b2b2b, stop: 0.5 #292929, stop: 0.9 #282828, stop: 1 #252525);\n"
"    selection-background-color: #ffaa00;\n"
"}\n"
"\n"
"QComboBox QAbstractItemView\n"
"{\n"
"    border: 2px solid darkgray;\n"
"    selection-background-color: QLinearGradient( x1: 0, y1: 0, x2: 0, y2: 1, stop: 0 #ffa02f, stop: 1 #d7801a);\n"
"}\n"
"\n"
"QComboBox::drop-down\n"
"{\n"
"     subcontrol-origin: padding;\n"
"     subcontrol-position: top right;\n"
"     width: 15px;\n"
"\n"
"     border-left-width: 0px;\n"
"     border-left-color: darkgray;\n"
"     border-left-style: solid; /* just a single line */\n"
"     border-top-right-radius: 3px; /* same radius as the QComboBox */\n"
"     border-bottom-right-radius: 3px;\n"
" }\n"
"\n"
"QComboBox::down-arrow\n"
"{\n"
"     image: url(:/down_arrow.png"
                        ");\n"
"}\n"
"\n"
"QGroupBox:focus\n"
"{\n"
"border: 2px solid QLinearGradient( x1: 0, y1: 0, x2: 0, y2: 1, stop: 0 #ffa02f, stop: 1 #d7801a);\n"
"}\n"
"\n"
"QTextEdit:focus\n"
"{\n"
"    border: 2px solid QLinearGradient( x1: 0, y1: 0, x2: 0, y2: 1, stop: 0 #ffa02f, stop: 1 #d7801a);\n"
"}\n"
"\n"
"QScrollBar:horizontal {\n"
"     border: 1px solid #222222;\n"
"     background: QLinearGradient( x1: 0, y1: 0, x2: 0, y2: 1, stop: 0.0 #121212, stop: 0.2 #282828, stop: 1 #484848);\n"
"     height: 7px;\n"
"     margin: 0px 16px 0 16px;\n"
"}\n"
"\n"
"QScrollBar::handle:horizontal\n"
"{\n"
"      background: QLinearGradient( x1: 0, y1: 0, x2: 1, y2: 0, stop: 0 #ffa02f, stop: 0.5 #d7801a, stop: 1 #ffa02f);\n"
"      min-height: 20px;\n"
"      border-radius: 2px;\n"
"}\n"
"\n"
"QScrollBar::add-line:horizontal {\n"
"      border: 1px solid #1b1b19;\n"
"      border-radius: 2px;\n"
"      background: QLinearGradient( x1: 0, y1: 0, x2: 1, y2: 0, stop: 0 #ffa02f, stop: 1 #d7801a);\n"
"      width: 14px;\n"
"      subcon"
                        "trol-position: right;\n"
"      subcontrol-origin: margin;\n"
"}\n"
"\n"
"QScrollBar::sub-line:horizontal {\n"
"      border: 1px solid #1b1b19;\n"
"      border-radius: 2px;\n"
"      background: QLinearGradient( x1: 0, y1: 0, x2: 1, y2: 0, stop: 0 #ffa02f, stop: 1 #d7801a);\n"
"      width: 14px;\n"
"     subcontrol-position: left;\n"
"     subcontrol-origin: margin;\n"
"}\n"
"\n"
"QScrollBar::right-arrow:horizontal, QScrollBar::left-arrow:horizontal\n"
"{\n"
"      border: 1px solid black;\n"
"      width: 1px;\n"
"      height: 1px;\n"
"      background: white;\n"
"}\n"
"\n"
"QScrollBar::add-page:horizontal, QScrollBar::sub-page:horizontal\n"
"{\n"
"      background: none;\n"
"}\n"
"\n"
"QScrollBar:vertical\n"
"{\n"
"      background: QLinearGradient( x1: 0, y1: 0, x2: 1, y2: 0, stop: 0.0 #121212, stop: 0.2 #282828, stop: 1 #484848);\n"
"      width: 7px;\n"
"      margin: 16px 0 16px 0;\n"
"      border: 1px solid #222222;\n"
"}\n"
"\n"
"QScrollBar::handle:vertical\n"
"{\n"
"      background: QLinearGradi"
                        "ent( x1: 0, y1: 0, x2: 0, y2: 1, stop: 0 #ffa02f, stop: 0.5 #d7801a, stop: 1 #ffa02f);\n"
"      min-height: 20px;\n"
"      border-radius: 2px;\n"
"}\n"
"\n"
"QScrollBar::add-line:vertical\n"
"{\n"
"      border: 1px solid #1b1b19;\n"
"      border-radius: 2px;\n"
"      background: QLinearGradient( x1: 0, y1: 0, x2: 0, y2: 1, stop: 0 #ffa02f, stop: 1 #d7801a);\n"
"      height: 14px;\n"
"      subcontrol-position: bottom;\n"
"      subcontrol-origin: margin;\n"
"}\n"
"\n"
"QScrollBar::sub-line:vertical\n"
"{\n"
"      border: 1px solid #1b1b19;\n"
"      border-radius: 2px;\n"
"      background: QLinearGradient( x1: 0, y1: 0, x2: 0, y2: 1, stop: 0 #d7801a, stop: 1 #ffa02f);\n"
"      height: 14px;\n"
"      subcontrol-position: top;\n"
"      subcontrol-origin: margin;\n"
"}\n"
"\n"
"QScrollBar::up-arrow:vertical, QScrollBar::down-arrow:vertical\n"
"{\n"
"      border: 1px solid black;\n"
"      width: 1px;\n"
"      height: 1px;\n"
"      background: white;\n"
"}\n"
"\n"
"\n"
"QScrollBar::add-page:vertical,"
                        " QScrollBar::sub-page:vertical\n"
"{\n"
"      background: none;\n"
"}\n"
"\n"
"QTextEdit\n"
"{\n"
"    background-color: #242424;\n"
"}\n"
"\n"
"QPlainTextEdit\n"
"{\n"
"    background-color: #242424;\n"
"}\n"
"\n"
"QHeaderView::section\n"
"{\n"
"    background-color: QLinearGradient(x1:0, y1:0, x2:0, y2:1, stop:0 #616161, stop: 0.5 #505050, stop: 0.6 #434343, stop:1 #656565);\n"
"    color: white;\n"
"    padding-left: 4px;\n"
"    border: 1px solid #6c6c6c;\n"
"}\n"
"\n"
"QCheckBox:disabled\n"
"{\n"
"color: #414141;\n"
"}\n"
"\n"
"QDockWidget::title\n"
"{\n"
"    text-align: center;\n"
"    spacing: 3px; /* spacing between items in the tool bar */\n"
"    background-color: QLinearGradient(x1:0, y1:0, x2:0, y2:1, stop:0 #323232, stop: 0.5 #242424, stop:1 #323232);\n"
"}\n"
"\n"
"QDockWidget::close-button, QDockWidget::float-button\n"
"{\n"
"    text-align: center;\n"
"    spacing: 1px; /* spacing between items in the tool bar */\n"
"    background-color: QLinearGradient(x1:0, y1:0, x2:0, y2:1, stop:0 #323232"
                        ", stop: 0.5 #242424, stop:1 #323232);\n"
"}\n"
"\n"
"QDockWidget::close-button:hover, QDockWidget::float-button:hover\n"
"{\n"
"    background: #242424;\n"
"}\n"
"\n"
"QDockWidget::close-button:pressed, QDockWidget::float-button:pressed\n"
"{\n"
"    padding: 1px -1px -1px 1px;\n"
"}\n"
"\n"
"QMainWindow::separator\n"
"{\n"
"    background-color: QLinearGradient(x1:0, y1:0, x2:0, y2:1, stop:0 #161616, stop: 0.5 #151515, stop: 0.6 #212121, stop:1 #343434);\n"
"    color: white;\n"
"    padding-left: 4px;\n"
"    border: 1px solid #4c4c4c;\n"
"    spacing: 3px; /* spacing between items in the tool bar */\n"
"}\n"
"\n"
"QMainWindow::separator:hover\n"
"{\n"
"\n"
"    background-color: QLinearGradient(x1:0, y1:0, x2:0, y2:1, stop:0 #d7801a, stop:0.5 #b56c17 stop:1 #ffa02f);\n"
"    color: white;\n"
"    padding-left: 4px;\n"
"    border: 1px solid #6c6c6c;\n"
"    spacing: 3px; /* spacing between items in the tool bar */\n"
"}\n"
"\n"
"QToolBar::handle\n"
"{\n"
"     spacing: 3px; /* spacing between items in the t"
                        "ool bar */\n"
"     background: url(:/images/handle.png);\n"
"}\n"
"\n"
"QMenu::separator\n"
"{\n"
"    height: 2px;\n"
"    background-color: QLinearGradient(x1:0, y1:0, x2:0, y2:1, stop:0 #161616, stop: 0.5 #151515, stop: 0.6 #212121, stop:1 #343434);\n"
"    color: white;\n"
"    padding-left: 4px;\n"
"    margin-left: 10px;\n"
"    margin-right: 5px;\n"
"}\n"
"\n"
"QProgressBar\n"
"{\n"
"    border: 2px solid grey;\n"
"    border-radius: 5px;\n"
"    text-align: center;\n"
"}\n"
"\n"
"QProgressBar::chunk\n"
"{\n"
"    background-color: #d7801a;\n"
"    width: 2.15px;\n"
"    margin: 0.5px;\n"
"}\n"
"\n"
"QTabBar::tab {\n"
"    color: #b1b1b1;\n"
"    border: 1px solid #444;\n"
"    border-bottom-style: none;\n"
"    background-color: #323232;\n"
"    padding-left: 10px;\n"
"    padding-right: 10px;\n"
"    padding-top: 3px;\n"
"    padding-bottom: 2px;\n"
"    margin-right: -1px;\n"
"}\n"
"\n"
"QTabWidget::pane {\n"
"    border: 1px solid #444;\n"
"    top: 1px;\n"
"}\n"
"\n"
"QTabBar::tab:last\n"
"{\n"
" "
                        "   margin-right: 0; /* the last selected tab has nothing to overlap with on the right */\n"
"    border-top-right-radius: 3px;\n"
"}\n"
"\n"
"QTabBar::tab:first:!selected\n"
"{\n"
" margin-left: 0px; /* the last selected tab has nothing to overlap with on the right */\n"
"\n"
"\n"
"    border-top-left-radius: 3px;\n"
"}\n"
"\n"
"QTabBar::tab:!selected\n"
"{\n"
"    color: #b1b1b1;\n"
"    border-bottom-style: solid;\n"
"    margin-top: 3px;\n"
"    background-color: QLinearGradient(x1:0, y1:0, x2:0, y2:1, stop:1 #212121, stop:.4 #343434);\n"
"}\n"
"\n"
"QTabBar::tab:selected\n"
"{\n"
"    border-top-left-radius: 3px;\n"
"    border-top-right-radius: 3px;\n"
"    margin-bottom: 0px;\n"
"}\n"
"\n"
"QTabBar::tab:!selected:hover\n"
"{\n"
"    /*border-top: 2px solid #ffaa00;\n"
"    padding-bottom: 3px;*/\n"
"    border-top-left-radius: 3px;\n"
"    border-top-right-radius: 3px;\n"
"    background-color: QLinearGradient(x1:0, y1:0, x2:0, y2:1, stop:1 #212121, stop:0.4 #343434, stop:0.2 #343434, stop:0.1 #ffaa00);\n"
""
                        "}\n"
"\n"
"QRadioButton::indicator:checked, QRadioButton::indicator:unchecked{\n"
"    color: #b1b1b1;\n"
"    background-color: #323232;\n"
"    border: 1px solid #b1b1b1;\n"
"    border-radius: 6px;\n"
"}\n"
"\n"
"QRadioButton::indicator:checked\n"
"{\n"
"    background-color: qradialgradient(\n"
"        cx: 0.5, cy: 0.5,\n"
"        fx: 0.5, fy: 0.5,\n"
"        radius: 1.0,\n"
"        stop: 0.25 #ffaa00,\n"
"        stop: 0.3 #323232\n"
"    );\n"
"}\n"
"\n"
"QCheckBox::indicator{\n"
"    color: #b1b1b1;\n"
"    background-color: #323232;\n"
"    border: 1px solid #b1b1b1;\n"
"    width: 9px;\n"
"    height: 9px;\n"
"}\n"
"\n"
"QRadioButton::indicator\n"
"{\n"
"    border-radius: 6px;\n"
"}\n"
"\n"
"QRadioButton::indicator:hover, QCheckBox::indicator:hover\n"
"{\n"
"    border: 1px solid #ffaa00;\n"
"}\n"
"\n"
"QCheckBox::indicator:checked\n"
"{\n"
"    image:url(:/images/checkbox.png);\n"
"}\n"
"\n"
"QCheckBox::indicator:disabled, QRadioButton::indicator:disabled\n"
"{\n"
"    border: 1px solid #444;\n"
""
                        "}")
        self.centralwidget = QWidget(MainWindow)
        self.centralwidget.setObjectName(u"centralwidget")
        self.gridLayout = QGridLayout(self.centralwidget)
        self.gridLayout.setObjectName(u"gridLayout")
        self.resultPathButton = QPushButton(self.centralwidget)
        self.resultPathButton.setObjectName(u"resultPathButton")

        self.gridLayout.addWidget(self.resultPathButton, 0, 4, 1, 1)

        self.productivityBox = QGroupBox(self.centralwidget)
        self.productivityBox.setObjectName(u"productivityBox")
        sizePolicy = QSizePolicy(QSizePolicy.Preferred, QSizePolicy.Preferred)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.productivityBox.sizePolicy().hasHeightForWidth())
        self.productivityBox.setSizePolicy(sizePolicy)
        self.verticalLayout_2 = QVBoxLayout(self.productivityBox)
        self.verticalLayout_2.setObjectName(u"verticalLayout_2")

        self.gridLayout.addWidget(self.productivityBox, 1, 0, 2, 1)

        self.resultBox = QGroupBox(self.centralwidget)
        self.resultBox.setObjectName(u"resultBox")
        self.verticalLayout_4 = QVBoxLayout(self.resultBox)
        self.verticalLayout_4.setObjectName(u"verticalLayout_4")
        self.budgetUtilL = QLabel(self.resultBox)
        self.budgetUtilL.setObjectName(u"budgetUtilL")
        self.budgetUtilL.setAlignment(Qt.AlignCenter)

        self.verticalLayout_4.addWidget(self.budgetUtilL)

        self.budgetUtilValL = QLabel(self.resultBox)
        self.budgetUtilValL.setObjectName(u"budgetUtilValL")
        self.budgetUtilValL.setAlignment(Qt.AlignCenter)

        self.verticalLayout_4.addWidget(self.budgetUtilValL)

        self.verticalSpacer_1 = QSpacerItem(20, 40, QSizePolicy.Minimum, QSizePolicy.Expanding)

        self.verticalLayout_4.addItem(self.verticalSpacer_1)

        self.successL = QLabel(self.resultBox)
        self.successL.setObjectName(u"successL")
        self.successL.setAlignment(Qt.AlignCenter)

        self.verticalLayout_4.addWidget(self.successL)

        self.successValL = QLabel(self.resultBox)
        self.successValL.setObjectName(u"successValL")
        self.successValL.setAlignment(Qt.AlignCenter)

        self.verticalLayout_4.addWidget(self.successValL)

        self.verticalSpacer_2 = QSpacerItem(20, 40, QSizePolicy.Minimum, QSizePolicy.Expanding)

        self.verticalLayout_4.addItem(self.verticalSpacer_2)

        self.qualityL = QLabel(self.resultBox)
        self.qualityL.setObjectName(u"qualityL")
        self.qualityL.setAlignment(Qt.AlignCenter)

        self.verticalLayout_4.addWidget(self.qualityL)

        self.qualityValL = QLabel(self.resultBox)
        self.qualityValL.setObjectName(u"qualityValL")
        self.qualityValL.setAlignment(Qt.AlignCenter)

        self.verticalLayout_4.addWidget(self.qualityValL)

        self.verticalSpacer_3 = QSpacerItem(20, 40, QSizePolicy.Minimum, QSizePolicy.Expanding)

        self.verticalLayout_4.addItem(self.verticalSpacer_3)

        self.submetricsL = QLabel(self.resultBox)
        self.submetricsL.setObjectName(u"submetricsL")
        self.submetricsL.setAlignment(Qt.AlignCenter)

        self.verticalLayout_4.addWidget(self.submetricsL)

        self.submetricsValL = QLabel(self.resultBox)
        self.submetricsValL.setObjectName(u"submetricsValL")
        self.submetricsValL.setAlignment(Qt.AlignCenter)

        self.verticalLayout_4.addWidget(self.submetricsValL)


        self.gridLayout.addWidget(self.resultBox, 1, 5, 2, 1)

        self.missionExecBox = QGroupBox(self.centralwidget)
        self.missionExecBox.setObjectName(u"missionExecBox")
        self.gridLayout_3 = QGridLayout(self.missionExecBox)
        self.gridLayout_3.setObjectName(u"gridLayout_3")
        self.startB = QPushButton(self.missionExecBox)
        self.startB.setObjectName(u"startB")

        self.gridLayout_3.addWidget(self.startB, 0, 0, 1, 1)

        self.pauseB = QPushButton(self.missionExecBox)
        self.pauseB.setObjectName(u"pauseB")

        self.gridLayout_3.addWidget(self.pauseB, 2, 0, 1, 1)

        self.consumptionL = QLabel(self.missionExecBox)
        self.consumptionL.setObjectName(u"consumptionL")

        self.gridLayout_3.addWidget(self.consumptionL, 0, 1, 1, 1)

        self.predictionErrorL = QLabel(self.missionExecBox)
        self.predictionErrorL.setObjectName(u"predictionErrorL")
        self.predictionErrorL.setAlignment(Qt.AlignLeading|Qt.AlignLeft|Qt.AlignTop)

        self.gridLayout_3.addWidget(self.predictionErrorL, 3, 1, 1, 1)

        self.perUnitConsumptionL = QLabel(self.missionExecBox)
        self.perUnitConsumptionL.setObjectName(u"perUnitConsumptionL")

        self.gridLayout_3.addWidget(self.perUnitConsumptionL, 2, 1, 1, 1)

        self.executionProgressBar = QProgressBar(self.missionExecBox)
        self.executionProgressBar.setObjectName(u"executionProgressBar")
        self.executionProgressBar.setValue(24)

        self.gridLayout_3.addWidget(self.executionProgressBar, 4, 0, 1, 2)

        self.remainingBudgetL = QLabel(self.missionExecBox)
        self.remainingBudgetL.setObjectName(u"remainingBudgetL")
        self.remainingBudgetL.setAlignment(Qt.AlignLeading|Qt.AlignLeft|Qt.AlignTop)

        self.gridLayout_3.addWidget(self.remainingBudgetL, 1, 1, 1, 1)


        self.gridLayout.addWidget(self.missionExecBox, 3, 0, 1, 1)

        self.postExecBox = QGroupBox(self.centralwidget)
        self.postExecBox.setObjectName(u"postExecBox")
        self.gridLayout_4 = QGridLayout(self.postExecBox)
        self.gridLayout_4.setObjectName(u"gridLayout_4")
        self.postExecTable = QTableWidget(self.postExecBox)
        if (self.postExecTable.columnCount() < 2):
            self.postExecTable.setColumnCount(2)
        __qtablewidgetitem = QTableWidgetItem()
        self.postExecTable.setHorizontalHeaderItem(0, __qtablewidgetitem)
        __qtablewidgetitem1 = QTableWidgetItem()
        self.postExecTable.setHorizontalHeaderItem(1, __qtablewidgetitem1)
        if (self.postExecTable.rowCount() < 2):
            self.postExecTable.setRowCount(2)
        __qtablewidgetitem2 = QTableWidgetItem()
        self.postExecTable.setVerticalHeaderItem(0, __qtablewidgetitem2)
        __qtablewidgetitem3 = QTableWidgetItem()
        self.postExecTable.setVerticalHeaderItem(1, __qtablewidgetitem3)
        __qtablewidgetitem4 = QTableWidgetItem()
        self.postExecTable.setItem(1, 0, __qtablewidgetitem4)
        __qtablewidgetitem5 = QTableWidgetItem()
        self.postExecTable.setItem(1, 1, __qtablewidgetitem5)
        self.postExecTable.setObjectName(u"postExecTable")

        self.gridLayout_4.addWidget(self.postExecTable, 0, 0, 1, 1)


        self.gridLayout.addWidget(self.postExecBox, 3, 2, 1, 4)

        self.retrainButton = QPushButton(self.centralwidget)
        self.retrainButton.setObjectName(u"retrainButton")

        self.gridLayout.addWidget(self.retrainButton, 0, 0, 1, 1)

        self.ferretPathButton = QPushButton(self.centralwidget)
        self.ferretPathButton.setObjectName(u"ferretPathButton")

        self.gridLayout.addWidget(self.ferretPathButton, 0, 2, 1, 1)

        self.configPathButton = QPushButton(self.centralwidget)
        self.configPathButton.setObjectName(u"configPathButton")

        self.gridLayout.addWidget(self.configPathButton, 0, 3, 1, 1)

        self.setupBox = QGroupBox(self.centralwidget)
        self.setupBox.setObjectName(u"setupBox")
        self.gridLayout_2 = QGridLayout(self.setupBox)
        self.gridLayout_2.setObjectName(u"gridLayout_2")
        self.overalL = QLabel(self.setupBox)
        self.overalL.setObjectName(u"overalL")

        self.gridLayout_2.addWidget(self.overalL, 8, 1, 1, 1)

        self.budgetShortText = QLineEdit(self.setupBox)
        self.budgetShortText.setObjectName(u"budgetShortText")
        sizePolicy1 = QSizePolicy(QSizePolicy.Preferred, QSizePolicy.Fixed)
        sizePolicy1.setHorizontalStretch(0)
        sizePolicy1.setVerticalStretch(0)
        sizePolicy1.setHeightForWidth(self.budgetShortText.sizePolicy().hasHeightForWidth())
        self.budgetShortText.setSizePolicy(sizePolicy1)

        self.gridLayout_2.addWidget(self.budgetShortText, 4, 1, 1, 1)

        self.doneB = QPushButton(self.setupBox)
        self.doneB.setObjectName(u"doneB")

        self.gridLayout_2.addWidget(self.doneB, 9, 1, 1, 1)

        self.line = QFrame(self.setupBox)
        self.line.setObjectName(u"line")
        self.line.setFrameShape(QFrame.HLine)
        self.line.setFrameShadow(QFrame.Sunken)

        self.gridLayout_2.addWidget(self.line, 5, 0, 1, 3)

        self.budgetL = QLabel(self.setupBox)
        self.budgetL.setObjectName(u"budgetL")

        self.gridLayout_2.addWidget(self.budgetL, 4, 0, 1, 1)

        self.qualityEstimateL = QLabel(self.setupBox)
        self.qualityEstimateL.setObjectName(u"qualityEstimateL")

        self.gridLayout_2.addWidget(self.qualityEstimateL, 6, 0, 1, 1)

        self.checkB = QPushButton(self.setupBox)
        self.checkB.setObjectName(u"checkB")

        self.gridLayout_2.addWidget(self.checkB, 4, 2, 1, 1)

        self.knobNameLayout = QHBoxLayout()
        self.knobNameLayout.setSpacing(0)
        self.knobNameLayout.setObjectName(u"knobNameLayout")
        self.knobNameLayout.setSizeConstraint(QLayout.SetDefaultConstraint)

        self.gridLayout_2.addLayout(self.knobNameLayout, 1, 0, 1, 3)

        self.submetricLayout = QHBoxLayout()
        self.submetricLayout.setObjectName(u"submetricLayout")

        self.gridLayout_2.addLayout(self.submetricLayout, 7, 0, 1, 3)

        self.knobsLayout = QHBoxLayout()
        self.knobsLayout.setObjectName(u"knobsLayout")

        self.gridLayout_2.addLayout(self.knobsLayout, 3, 0, 1, 3)


        self.gridLayout.addWidget(self.setupBox, 1, 2, 2, 3)

        MainWindow.setCentralWidget(self.centralwidget)

        self.retranslateUi(MainWindow)

        QMetaObject.connectSlotsByName(MainWindow)
    # setupUi

    def retranslateUi(self, MainWindow):
        MainWindow.setWindowTitle(QCoreApplication.translate("MainWindow", u"MainWindow", None))
        self.resultPathButton.setText(QCoreApplication.translate("MainWindow", u"Results Location", None))
        self.productivityBox.setTitle(QCoreApplication.translate("MainWindow", u"Productivity Preview", None))
        self.resultBox.setTitle(QCoreApplication.translate("MainWindow", u"Result Summary Panel", None))
        self.budgetUtilL.setText(QCoreApplication.translate("MainWindow", u"Budget Utilization:", None))
        self.budgetUtilValL.setText(QCoreApplication.translate("MainWindow", u"X%", None))
        self.successL.setText(QCoreApplication.translate("MainWindow", u"Sucess:", None))
        self.successValL.setText(QCoreApplication.translate("MainWindow", u"True/False", None))
        self.qualityL.setText(QCoreApplication.translate("MainWindow", u"Overall Quality:", None))
        self.qualityValL.setText(QCoreApplication.translate("MainWindow", u"X%", None))
        self.submetricsL.setText(QCoreApplication.translate("MainWindow", u"Sub-metrics:", None))
        self.submetricsValL.setText(QCoreApplication.translate("MainWindow", u"x_1, x_2, x_3", None))
        self.missionExecBox.setTitle(QCoreApplication.translate("MainWindow", u"Mission Execution Panel", None))
        self.startB.setText(QCoreApplication.translate("MainWindow", u"Start", None))
        self.pauseB.setText(QCoreApplication.translate("MainWindow", u"Pause", None))
        self.consumptionL.setText(QCoreApplication.translate("MainWindow", u"Consumption: X Seconds", None))
        self.predictionErrorL.setText(QCoreApplication.translate("MainWindow", u"Prediction Error: X%", None))
        self.perUnitConsumptionL.setText(QCoreApplication.translate("MainWindow", u"Per Unit Consumption: X Seconds", None))
        self.remainingBudgetL.setText(QCoreApplication.translate("MainWindow", u"Remaining Budget: X Seconds", None))
        self.postExecBox.setTitle(QCoreApplication.translate("MainWindow", u"Post-Execution Panel", None))
        ___qtablewidgetitem = self.postExecTable.horizontalHeaderItem(0)
        ___qtablewidgetitem.setText(QCoreApplication.translate("MainWindow", u"Stuff", None));
        ___qtablewidgetitem1 = self.postExecTable.horizontalHeaderItem(1)
        ___qtablewidgetitem1.setText(QCoreApplication.translate("MainWindow", u"More Stuff", None));
        ___qtablewidgetitem2 = self.postExecTable.verticalHeaderItem(0)
        ___qtablewidgetitem2.setText(QCoreApplication.translate("MainWindow", u"Things", None));
        ___qtablewidgetitem3 = self.postExecTable.verticalHeaderItem(1)
        ___qtablewidgetitem3.setText(QCoreApplication.translate("MainWindow", u"Some more Things", None));

        __sortingEnabled = self.postExecTable.isSortingEnabled()
        self.postExecTable.setSortingEnabled(False)
        ___qtablewidgetitem4 = self.postExecTable.item(1, 0)
        ___qtablewidgetitem4.setText(QCoreApplication.translate("MainWindow", u"stuff has things", None));
        ___qtablewidgetitem5 = self.postExecTable.item(1, 1)
        ___qtablewidgetitem5.setText(QCoreApplication.translate("MainWindow", u"Things has stuff", None));
        self.postExecTable.setSortingEnabled(__sortingEnabled)

        self.retrainButton.setText(QCoreApplication.translate("MainWindow", u"Re-Train", None))
        self.ferretPathButton.setText(QCoreApplication.translate("MainWindow", u"Import Ferret", None))
        self.configPathButton.setText(QCoreApplication.translate("MainWindow", u"Import Config Files", None))
        self.setupBox.setTitle(QCoreApplication.translate("MainWindow", u"Mission Setup Panel", None))
        self.overalL.setText(QCoreApplication.translate("MainWindow", u"Overall: xx%", None))
        self.budgetShortText.setText(QCoreApplication.translate("MainWindow", u"Enter your budget", None))
        self.doneB.setText(QCoreApplication.translate("MainWindow", u"Done", None))
        self.budgetL.setText(QCoreApplication.translate("MainWindow", u"Budget:", None))
        self.qualityEstimateL.setText(QCoreApplication.translate("MainWindow", u"Estimated Quality", None))
        self.checkB.setText(QCoreApplication.translate("MainWindow", u"Check", None))
    # retranslateUi

