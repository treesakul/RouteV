import sys

#from PySide.QtCore import *
#from PySide.QtGui import *
#from PySide.QtUiTools import *

from MainPage import *
from EntrancePage import *
from StopPage import *
from CalPage import *

from MainSystem import *
from PyQt4.QtCore import *
from PyQt4.QtGui import *

class UI_Manager(QMainWindow):
    
    def __init__(self, parent = None):
        QWidget.__init__(self, None)
        self.parent = parent
        self.setWindowTitle("RouteV")
        self.controller = MainSystem() 

        self.central_widget = QStackedWidget()
        self.setCentralWidget(self.central_widget)

        #place widgets
        self.entrancePage = EntrancePage(self, self.controller)
        self.mainPage = MainPage(self, self.controller)
        self.stopPage = StopPage(self, self.controller)
        self.calPage = CalPage(self, self.controller)

        #set first page
        self.central_widget.addWidget(self.entrancePage)

        # set central widget
        self.central_widget.addWidget(self.mainPage)
        self.central_widget.addWidget(self.stopPage)
        self.central_widget.addWidget(self.calPage)

    
    def changePage(self, toPage):
        if (toPage == "entrancePage"):
            self.centralWidget().setCurrentWidget(self.entrancePage)

        elif (toPage == "stopPage"):
            self.centralWidget().setCurrentWidget(self.stopPage)

        elif (toPage == "calPage"):
            self.centralWidget().setCurrentWidget(self.calPage)
            self.calPage.reset()
            
        elif (toPage == "mainPage"):
            self.centralWidget().setCurrentWidget(self.mainPage)


def main():
        app = QApplication(sys.argv)

        w = UI_Manager()
        w.resize(800,600)
        w.show()
        return app.exec_()

if __name__ == "__main__":
        sys.exit(main())
