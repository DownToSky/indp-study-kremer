from UI.RAPIDS_mainWindow import Ui_MainWindow
import sys
from PySide2 import QtCore, QtWidgets, QtGui
from PySide2.QtCore import Qt
import json
import time
import random


class UI_Controller(QtWidgets.QMainWindow):

    def __init__ (self):
        super(UI_Controller, self).__init__()
        self.ui = Ui_MainWindow()
        self.ui.setupUi(self)
        icon = QtGui.QIcon("icons8-open-source.svg")
        self.setWindowIcon(icon)
        self.setWindowTitle("RAPIDS")

        self.configPath = None
        self.ui.configPathButton.pressed.connect(self.getConfigPath)

        self.ferretPath = None
        self.ui.ferretPathButton.pressed.connect(self.getFerretPath)

        self.resultPath = None
        self.ui.resultPathButton.pressed.connect(self.getResultPath)

        self.ui.doneB.pressed.connect(self.saveConfig)

        self.ui.stackedWidget.setCurrentIndex(0)
        self.ui.studyToggleB_product.pressed.connect(self.studyToggled)
        self.ui.studyToggleB_study.pressed.connect(self.productionToggled)
        self.challengePath = None
        self.challenges = None
        self.curr_challenge = None
        self.ui.challengeImportB.pressed.connect(self.getChallengePath)


        self.ui.checkB_study.pressed.connect(self.check)

        self.ui.nextB_study.pressed.connect(self.nextStudy)

        self.knobs = list()
        self.knobLabels = list()
        self.submatrixLabels = list()

        self.disabled_unused()

        self.configs = None

    def nextStudy(self):
        if self.curr_challenge == None:
            return
        self.curr_challenge += 1
        self.loadChallenge()


    def loadChallenge(self):
        self.ui.studyPage.setDisabled(True)
        ch_index = self.curr_challenge
        if ch_index < len(self.challenges["challenge_list"]):
            self.ui.budgetAmountL_study.setText("{}".format(self.challenges["challenge_list"][ch_index]["budget"]))
            self.challenges["challenge_list"][ch_index]["logs"] = dict()
            self.challenges["challenge_list"][ch_index]["logs"]["tries"] = list()
            self.challenges["challenge_list"][ch_index]["logs"]["load_time"] = time.time()
            print("{} load time for challenge#{}".format(self.challenges["challenge_list"][ch_index]["logs"]["load_time"], ch_index))
            challenge = self.challenges["challenge_list"][ch_index]
            self.configDir = challenge["cfg_location"]
            self.loadConfig()
            self.ui.ChallengeInstructions.setText(challenge["desc"])
            self.ui.challengeNumL.setText("({} / {})".format(ch_index + 1, len(self.challenges["challenge_list"])))
            self.ui.appNameL.setText(challenge["name"])
            self.ui.submetricNameL.setText(challenge["sub-metric"])
            self.ui.targetNameL.setText(str(challenge["target"]))
        else:
            self.ui.budgetAmountL_study.setText("")
            self.challenges["completion_time"] = time.time()
            self.ui.InstructionsTextBrowser.setText("Challenges Finished!")
            self.ui.ChallengeInstructions.setText("")
            self.saveStudyLogs()
            self.challenges = None
            self.curr_challenge = None
            for i in reversed(range(len(self.knobs))):
                self.knobLabels[i].deleteLater()
                self.knobs[i].deleteLater()

        self.ui.studyPage.setEnabled(True)

    def saveStudyLogs(self):
        with open("study_logs.json", 'w') as studyFile:
            json.dump(self.challenges, studyFile, indent=4, sort_keys=True)

    def check(self):
        ch_index = self.curr_challenge
        tryInfo = dict()
        tryInfo["time"] = time.time()
        tryInfo["knob_info"] = dict(zip([knob_name.objectName() for knob_name in self.knobs], [knob_val.value() for knob_val in self.knobs]))
        print(str(tryInfo["knob_info"]))
        quality, budget_utilizaiton = self.simulateRandomResult(tryInfo["knob_info"], self.challenges["challenge_list"][ch_index]["budget"])
        self.ui.budgetUtilValL_2.setText("{}%".format(budget_utilizaiton))
        self.ui.qualityValL_2.setText("{}%".format(quality))
        tryInfo["quality_percent"] = quality
        tryInfo["budget_percent"] = budget_utilizaiton
        self.challenges["challenge_list"][ch_index]["logs"]["tries"].append(tryInfo)

    def simulateRandomResult(self, knobDict, budget):
        return random.randint(1,100), random.randint(1, 1000)/budget

    def getChallengePath(self):
        path = QtWidgets.QFileDialog.getOpenFileName()

        print("challenges path: " + str(path))
        if path[0] != "" or path[0] != None:
            self.challengePath = path[0]
            self.initChallenges()
        else:
            self.challengePath = None
            self.challenges = None
            self.curr_challenge = None

    def initChallenges(self):
        with open(self.challengePath, 'r') as chFile:
            self.challenges = json.load(chFile)
            self.ui.InstructionsTextBrowser.setText(self.challenges["overall_desc"])
            self.curr_challenge = 0
            self.loadChallenge()
    
    def toggleKnobType(self):
        pass

    def studyToggled(self):
        self.ui.stackedWidget.setCurrentIndex(1)

    def productionToggled(self):
        self.ui.stackedWidget.setCurrentIndex(0)

    def updatePrefrences(self):
        if self.configs == None:
            print("load configs first!")
            return
        knob_name = self.sender().objectName()
        knob_type = self.challenges["challenge_list"][self.curr_challenge]["knob_type"]
        self.configs[knob_type][knob_name] = self.sender().value()
        print("{} change to {}".format(knob_name, self.sender().value()))


    def saveConfig(self):
        if self.configs == None:
            print("load configs first!")
            return

        with open(self.configDir, 'w') as confFile:
            json.dump(self.configs, confFile)

    def loadKnobs(self):
        if self.challenges["challenge_list"][self.curr_challenge]["knob_type"] not in self.configs:
            return
        MIN_VAL = 1
        MAX_VAL = 100
        for i in reversed(range(len(self.knobs))):
            self.knobLabels[i].deleteLater()
            self.knobs[i].deleteLater()
        self.knobLabels = list()
        self.knobs = list()
        for i, knob_name in enumerate(self.configs[self.challenges["challenge_list"][self.curr_challenge]["knob_type"]]):
            print(knob_name)
            # Labels showing which knob is which prefrence
            self.knobLabels.append(QtWidgets.QLabel())
            self.knobLabels[i].setText(knob_name)
            self.knobLabels[i].setAlignment(Qt.AlignCenter|Qt.AlignBottom)

            self.knobs.append(QtWidgets.QDial())
            self.knobs[i].setObjectName(knob_name)   #used to get the object later
            self.knobs[i].setMaximum(MAX_VAL)
            self.knobs[i].setMinimum(MIN_VAL)
            value_in_config = self.configs[self.challenges["challenge_list"][self.curr_challenge]["knob_type"]][knob_name]
            if value_in_config > MAX_VAL:
                self.knobs[i].setValue(MAX_VAL)
            elif value_in_config < MIN_VAL:
                self.knobs[i].setValue(MIN_VAL)
            else:
                self.knobs[i].setValue(value_in_config)
            
            self.knobs[i].valueChanged.connect(self.updatePrefrences)

            self.ui.knobNameLayout_study.addWidget(self.knobLabels[i])
            self.ui.knobsLayout_study.addWidget(self.knobs[i])

            self.knobLabels[i].show()
            self.knobs[i].show()

    def disabled_unused(self):
        self.ui.retrainButton.setDisabled(True)
        self.ui.productivityBox.setDisabled(True)
        self.ui.missionExecBox.setDisabled(True)
        self.ui.resultBox.setDisabled(True)
        self.ui.postExecBox.setDisabled(True)

    def loadConfig(self):
        with open(self.configDir, 'r') as confFile:
            self.configs = json.load(confFile)
            budget = str(self.configs["mission"]["budget"])
            self.ui.budgetShortText.setText(budget)
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