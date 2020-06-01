from UI.RAPIDS_mainWindow import Ui_MainWindow
import sys
from PySide2 import QtCore, QtWidgets, QtGui
from PySide2.QtCore import Qt
import json
import time
import random


class UI_Controller(QtWidgets.QMainWindow):

    def __init__ (self, user_study = False):
        """
        Parameters
        ----------
        user_study : boolean, optional
            determins if the class starts in user study mode
        """

        # Hooking the class to designed template
        super(UI_Controller, self).__init__()
        self.ui = Ui_MainWindow()
        self.ui.setupUi(self)

        # Initial layout values set
        self.ui.stackedWidget.setCurrentIndex(0)    # Start in production mode
        self.setWindowTitle("RAPIDS")
        self.configs = None

            # Production:
        # Connecting the buttons
        self.ui.studyToggleB_product.clicked.connect(self.studyToggled)

        self.configPath = None
        self.ui.configPathButton.clicked.connect(self.getConfigPath)

        self.programPath = None
        self.ui.programPathButton.clicked.connect(self.getProgramPath)

        self.resultPath = None
        self.ui.resultPathButton.clicked.connect(self.getResultPath)

        self.ui.doneB.clicked.connect(self.saveConfig)
        self.disabled_unused() # Temporary production widgets disabled


            # User Study:
        # Connecting buttons
        self.ui.studyToggleB_study.clicked.connect(self.productionToggled)
        self.challengePath = None
        self.challenges = None
        self.curr_challenge = None
        self.curr_knob_type = None
        self.ui.challengeImportB.clicked.connect(self.getChallengePath)

        self.ui.checkB_study.clicked.connect(self.check)
        self.ui.nextB_study.clicked.connect(self.loadNextChallenge)
        self.ui.knobTypeToggleB.clicked.connect(self.toggleKnobType)

        
        if user_study:
            self.setUserstudy() 


            
         
    def setUserstudy(self):
        """
        Hides certain widgets for user study
        """
        self.ui.stackedWidget.setCurrentIndex(1)    # Start in user study mode
        self.ui.studyToggleB_study.hide()
        self.ui.knobTypeToggleB.hide()
        self.ui.budgetL_study.hide()
        self.ui.budgetAmountL_study.hide()


    def loadNextChallenge(self):
        if self.curr_challenge == None:
            return
        self.loadChallenge(self.curr_challenge["id"] + 1)



    def loadChallenge(self, challange_id):
        """
        This function is only called after challenges are loaded.
        """
        self.ui.studyPage.setDisabled(True)
        total_challenges = len(self.challenges["challenge_list"])
        if challange_id < total_challenges:
            self.curr_challenge = self.challenges["challenge_list"][challange_id]
            self.curr_knob_type = self.curr_challenge["knob_type"]
            self.ui.budgetAmountL_study.setText("{}".format(self.curr_challenge["budget"]))
            self.curr_challenge["logs"] = dict()
            self.curr_challenge["logs"]["tries"] = list()
            self.curr_challenge["logs"]["load_time"] = time.time()
            self.configDir = self.curr_challenge["cfg_location"]
            self.loadConfig()
            self.ui.ChallengeInstructions.setText(self.curr_challenge["desc"])
            self.ui.challengeNumL.setText("({} out of {})".format(challange_id + 1, total_challenges))
            self.ui.appNameL.setText(self.curr_challenge["name"])
            self.ui.submetricNameL.setText(self.curr_challenge["sub-metric"])
            self.ui.targetNameL.setText(str(self.curr_challenge["target"]))
            self.ui.checkB_study.setDisabled(False)
            self.ui.nextB_study.setText("Next Challenge")
            self.ui.nextB_study.setDisabled(False)
            self.ui.successValL_study.setText("")
            self.ui.qualityValL_study.setText("")
        else:
            self.ui.budgetAmountL_study.setText("")
            self.challenges["completion_time"] = time.time()
            self.ui.InstructionsTextBrowser.setText("Challenges Finished!")
            self.ui.ChallengeInstructions.setText("")
            self.saveStudyLogs()
            self.challengePath = None
            self.challenges = None
            self.curr_knob_type = None
            self.curr_challenge = None

            self.ui.successValL_study.setText("")
            self.ui.qualityValL_study.setText("")

            self.ui.appNameL.setText("")
            self.ui.submetricNameL.setText("")
            self.ui.targetNameL.setText("")
            self.ui.nextB_study.setText("Done!")
            self.ui.checkB_study.setDisabled(True)
            self.ui.nextB_study.setDisabled(True)
            for i in reversed(range(self.ui.knobNameLayout_study.count())): 
                self.ui.knobNameLayout_study.itemAt(i).widget().deleteLater()
            for i in reversed(range(self.ui.knobsLayout_study.count())): 
                self.ui.knobsLayout_study.itemAt(i).widget().deleteLater()
            for i in reversed(range(self.ui.knobValueLayout_study.count())): 
                self.ui.knobValueLayout_study.itemAt(i).widget().deleteLater()
            for i in reversed(range(self.ui.submetricsResultLayout_study.count())): 
                self.ui.submetricsResultLayout_study.itemAt(i).widget().deleteLater()

        self.ui.studyPage.setEnabled(True)

    def saveStudyLogs(self):
        with open("study_logs{}.json".format(time.time()), 'w') as studyFile:
            json.dump(self.challenges, studyFile, indent=4, sort_keys=True)

    def check(self):
        if self.curr_challenge == None:
            return
        tryInfo = dict()
        tryInfo["time"] = time.time()
        tryInfo["knob_type"] = self.curr_knob_type
        knob_names = [self.ui.knobsLayout_study.itemAt(i).widget().objectName() for i in range(self.ui.knobsLayout_study.count())]
        knob_values = [self.ui.knobsLayout_study.itemAt(i).widget().value() for i in range(self.ui.knobsLayout_study.count())]
        tryInfo["knob_info"] = dict(zip(knob_names, knob_values))

        quality, budget_utilizaiton, success = self.simulateRandomResult(tryInfo["knob_info"], self.curr_challenge["budget"])
        if success:
            self.ui.successValL_study.setText("Success!")
            self.ui.successValL_study.setStyleSheet("color: green;")
            tryInfo["if_success"] = True
        else:
            self.ui.successValL_study.setText("Fail!")
            self.ui.successValL_study.setStyleSheet("color: red;")
            tryInfo["if_success"] = False
        self.ui.qualityValL_study.setText("{}".format(quality))
        tryInfo["quality_percent"] = quality
        tryInfo["budget_percent"] = budget_utilizaiton
        self.curr_challenge["logs"]["tries"].append(tryInfo)

    def simulateRandomResult(self, knobDict, budget):
        return random.randint(1,100), random.randint(1, 1000)/budget, True

    def getChallengePath(self):
        path = QtWidgets.QFileDialog.getOpenFileName()

        if path[0] != None and path[0].strip() != '':
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
            self.loadChallenge(0)
    
    def toggleKnobType(self):
        if self.curr_knob_type == None:
             return
        elif self.curr_knob_type == "virtual":
            self.curr_knob_type = "concrete"
        else:
            self.curr_knob_type = "virtual"
        self.loadKnobs()


    def studyToggled(self):
        self.ui.stackedWidget.setCurrentIndex(1)

    def productionToggled(self):
        self.ui.stackedWidget.setCurrentIndex(0)

    def updatePrefrences(self):
        if self.configs == None:
            print("load configs first!")
            return
        knob_name = self.sender().objectName()
        knob_type = self.curr_knob_type
        self.configs[knob_type][knob_name] = self.sender().value()
        knobValueLabel = None
        for i in range(self.ui.knobValueLayout_study.count()): 
            if self.ui.knobValueLayout_study.itemAt(i).widget().objectName() == knob_name:
                knobValueLabel = self.ui.knobValueLayout_study.itemAt(i).widget()
        assert knobValueLabel != None, "knob value label with proper object file not found"
        knobValueLabel.setText(str(self.sender().value()))


    def saveConfig(self):
        if self.configs == None:
            print("load configs first!")
            return

        with open(self.configDir, 'w') as confFile:
            json.dump(self.configs, confFile)

    def loadKnobs(self):
        MIN_VAL = 1
        MAX_VAL = 100
        for i in reversed(range(self.ui.knobNameLayout_study.count())): 
            self.ui.knobNameLayout_study.itemAt(i).widget().deleteLater()
        for i in reversed(range(self.ui.knobsLayout_study.count())): 
            self.ui.knobsLayout_study.itemAt(i).widget().deleteLater()
        for i in reversed(range(self.ui.knobValueLayout_study.count())): 
            self.ui.knobValueLayout_study.itemAt(i).widget().deleteLater()
        for i in reversed(range(self.ui.submetricsResultLayout_study.count())): 
            self.ui.submetricsResultLayout_study.itemAt(i).widget().deleteLater()
        for knob_name in self.configs[self.curr_knob_type]:
            # Labels showing which knob is which prefrence
            knobLabel = QtWidgets.QLabel()
            knobLabel.setObjectName(knob_name)   #used to get the object later
            knobLabel.setText(knob_name)
            knobLabel.setAlignment(Qt.AlignCenter|Qt.AlignBottom)

            knob = QtWidgets.QDial()
            knob.setObjectName(knob_name)   #used to get the object later
            knob.setMaximum(MAX_VAL)
            knob.setMinimum(MIN_VAL)
            value_in_config = self.configs[self.curr_knob_type][knob_name]
            knobValueLabel = QtWidgets.QLabel()
            knobValueLabel.setObjectName(knob_name)   #used to get the object later
            knobValueLabel.setAlignment(Qt.AlignCenter|Qt.AlignBottom)
            if value_in_config > MAX_VAL:
                knob.setValue(MAX_VAL)
                knobValueLabel.setText(str(MAX_VAL))
            elif value_in_config < MIN_VAL:
                knob.setValue(MIN_VAL)
                knobValueLabel.setText(str(MIN_VAL))
            else:
                knob.setValue(value_in_config)
                knobValueLabel.setText(str(value_in_config))
            
            knob.valueChanged.connect(self.updatePrefrences)

            self.ui.knobNameLayout_study.addWidget(knobLabel)
            self.ui.knobsLayout_study.addWidget(knob)
            self.ui.knobValueLayout_study.addWidget(knobValueLabel)

            knobLabel.show()
            knob.show()
            knobValueLabel.show()

    def disabled_unused(self):
        self.ui.retrainButton.setDisabled(True)
        self.ui.productivityBox.setDisabled(True)
        self.ui.missionExecBox.setDisabled(True)
        self.ui.resultBox.setDisabled(True)
        self.ui.postExecBox.setDisabled(True)

    def loadConfig(self):
        with open(self.configDir, 'r') as confFile:
            self.configs = json.load(confFile)
            budget = self.configs["mission"]["budget"]
            self.ui.budgetShortText.setText(str(budget))
            self.loadKnobs()

    # TODO: makesure the returned path is nonempty
    def getProgramPath(self):
        path = QtWidgets.QFileDialog.getExistingDirectory()

        print("ferret directory: " + str(path))
        self.programPath = path

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
    user_study = False
    if "--user-study" in sys.argv:
        user_study = True
    window = UI_Controller(user_study=user_study)
    window.show()

    sys.exit(app.exec_())