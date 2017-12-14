import sys
import os
from PyQt4.QtCore import *
from PyQt4.QtGui import *
from PyQt4.uic import *

class EntrancePage(QMainWindow):
    def __init__(self, parent = None, controller = None):
        QMainWindow.__init__(self, parent = None)
        self.parent = parent
        self.controller = controller
        
        #loader = QUiLoader()
        form = loadUi("UI/entrancePage.ui", None)
        self.setCentralWidget(form)

        #set QPushButton
        self.start_bt = form.findChild(QPushButton, "start_bt")
        label = form.findChild(QLabel, "label") 
        label.setPixmap(QPixmap(os.getcwd() + "/UI/r_start.png"))

        #add action
        self.start_bt.clicked.connect(self.nextPage)

    def nextPage(self):
        self.parent.changePage("mainPage")
