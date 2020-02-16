import sys
from PySide2 import QtCore, QtWidgets, QtGui
import random




#  Randomly generates an input senario for our program
#  This function is only useful until we get our hand on 
#  RAPIDS to test the GUI direclty
def gen_option_inputs(knob_num_min, knob_num_max, knob_budget_max):
    # Randomly picking the number of knobs
    knob_num = random.randint(knob_num_min , knob_num_max)

    #Randomly pick budget vs performace prediction for each
    knobs = list()
    for _ in range(knob_num):
        knob_values = list()
        for j in range(knob_budget_max):
            if j == 0:
                knob_values.append(random.randint(0 , 1))
            else:
                knob_values.append(random.randint(knob_values[j-1], 
                                    knob_values[j-1] + 1))
        knobs.append(knob_values)

    # Pick the random budget from  the range of total needed for
    # everything max and half of that
    total_budget = random.randint(knob_num * knob_budget_max//2,
                             knob_num * knob_budget_max)
    return knobs, total_budget




class MyWidget(QtWidgets.QWidget):
    def __init__(self, knobs, total_budget):
        super().__init__()
        self.layout = QtWidgets.QVBoxLayout()

        self.knobs = list()
        for knob in knobs:
            label = QtWidgets.QLabel()
            slider = QtWidgets.QSlider()
            label.setAlignment(QtCore.Qt.AlignCenter)
            self.layout.addWidget(label)
            self.layout.addWidget(slider)
        
            self.knobs.append((label, slider, knob))
            


        self.setLayout(self.layout)





if __name__ == "__main__":
    # read_config_file_function()
    # connect to the estimation funcitons
    app = QtWidgets.QApplication([])
    knobs_vals, total_budget = gen_option_inputs(2,5,10)
    widget = MyWidget(knobs_vals, total_budget)
    widget.resize(800,600)
    widget.show()

    sys.exit(app.exec_())