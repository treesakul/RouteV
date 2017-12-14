import sys
import os
from PyQt4.QtCore import *
from PyQt4.QtGui import *
from PyQt4.uic import *

class MainPage(QMainWindow):
    def __init__(self, parent = None, controller = None):
        QMainWindow.__init__(self, None) 
        self.parent = parent
        self.system = controller
        
        #loader = QUiLoader()
        form = loadUi("./UI/mainPage.ui", None)
        self.setCentralWidget(form)

        #set QPushButton
        self.stop_bt = form.findChild(QPushButton, "stop_bt")
        self.cal_bt = form.findChild(QPushButton, "cal_bt")
        label = form.findChild(QLabel, "label") 
        label.setPixmap(QPixmap(os.getcwd() + "/UI/r_main.png"))
        #add action
        self.stop_bt.clicked.connect(self.callStopPage)
        self.cal_bt.clicked.connect(self.callCalPage)

    def callStopPage(self):
        self.parent.changePage("stopPage")

    def callCalPage(self):
        self.parent.changePage("calPage")
