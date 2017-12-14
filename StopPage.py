from PyQt4.QtCore import *
from PyQt4.QtGui import *
from PyQt4.QtWebKit import *

from MapWidget import *
import urllib.request

class StopPage(QMainWindow):
    def __init__(self, parent = None, controller = None):
        QMainWindow.__init__(self, parent = None)
        self.parent = parent
        self.controller = controller
        

        #Create a new stacked layout
        self.stackedLayout = QStackedLayout()

        #Create the stacked widget
        self.stackedWidget = QWidget()
        self.widgetS = QWidget()
        self.layoutx = QVBoxLayout()
        self.instruction  = QLabel()
        self.instruction.setText('Search for a stop in google map and click Add to add to the database')
        
        
        
        #necessary items
        self.mainGridLayout = QGridLayout()
        self.map = MapWidget()
        self.add_bt = QPushButton("Add")
        self.back_bt = QPushButton("Back")
        self.scroll = QScrollArea()
        #self.scroll.setHorizontalScrollBarPolicy(Qt.ScrollBarAlwaysOff)
        self.stackedWidget.setLayout(self.stackedLayout)
        self.info_layout = QVBoxLayout()
        self.info_name = QLabel()
        self.info_buttons = {}
        self.info = {}
        self.info_address = QLabel()
        self.info_widget = QWidget()
        self.boldFont= QFont()
        self.boldFont.setBold(True)
        self.info_name.setFont(self.boldFont)
       
        
        #Generate Initial Layout
        
        self.info_layout.addWidget(self.info_name)
        self.info_layout.addWidget(self.info_address)
        self.info_widget.setLayout(self.info_layout)
        self.layout()

        #Set the windows central widget
        self.setCentralWidget(self.stackedWidget)


    def layout(self):

        #add to layout
        self.mainGridLayout.addWidget(self.instruction,1,1,1,6)
        self.mainGridLayout.addWidget(self.map,2,1,4,4)
        self.mainGridLayout.addWidget(self.add_bt, 2,5,1,2)
        self.mainGridLayout.addWidget(self.scroll,3,5,3,2)
        self.mainGridLayout.addWidget(self.info_widget,6,1,2,4)
        self.mainGridLayout.addWidget(self.back_bt,7,5,1,2)
        
     
        #Connections
        self.add_bt.clicked.connect(self.getLocationData)
        self.back_bt.clicked.connect(self.back)
       
        self.mainWidget = QWidget()
        self.mainWidget.setLayout(self.mainGridLayout)
        
        #Add to Stacked Layout
        self.stackedLayout.addWidget(self.mainWidget)

        self.set_scroll()

    def set_scroll(self):

        self.widgetS = QWidget()  # create very large + long widget
        self.layoutx = QVBoxLayout()
        
        self.name = self.controller.get_existing_nodes()

        for i in self.name:
            name = i['Name']
            p_id = i['P_id']
            #address = i['Address']
            name = name.replace('xSLASHx','/').replace('xMINUSx','-').replace('xUNDERx','_').replace('xCOMMAx',',').replace('xSPACEx',' ')[1:]
            #address = address.replace('xSLASHx','/').replace('xMINUSx','-').replace('xUNDERx','_').replace('xCOMMAx',',').replace('xSPACEx',' ')[1:]
            
            layouth = QHBoxLayout()
            button = QPushButton(name)
            button.setStyleSheet("QPushButton { text-align: left; }")
            #button.setSizePolicy(QSizePolicy.Expanding,QSizePolicy.Expanding)
            #button.setFixedHeight(1)
            #button.setFixedWidth(140)
            self.info_buttons[button] = p_id
            self.info[p_id] = i
               
            button.clicked.connect(self.show_info)
            layouth.addWidget(button)
            
            self.layoutx.addLayout(layouth)

            
        self.layoutx.setAlignment(Qt.AlignTop)
        self.widgetS.setLayout(self.layoutx)
        self.scroll.setWidget(self.widgetS)

    def show_info(self):
        sender = self.sender()
        p_id = self.info_buttons[sender]
        info = self.info[p_id]
        self.info_name.setText(info['Name'].replace('xSLASHx','/').replace('xMINUSx','-').replace('xUNDERx','_').replace('xCOMMAx',',').replace('xSPACEx',' ')[1:])
        self.info_address.setText(info['Address'].replace('xSLASHx','/').replace('xMINUSx','-').replace('xUNDERx','_').replace('xCOMMAx',',').replace('xSPACEx',' ')[1:])
    
    def getLocationData(self):

        p_id = self.map.page().mainFrame().evaluateJavaScript("get_placeid()")
        p_name = self.map.page().mainFrame().evaluateJavaScript("get_name()")
        p_location = self.map.page().mainFrame().evaluateJavaScript("get_location()")

        self.controller.add_stop(p_id, p_name, p_location)

        self.set_scroll()

    def back(self):
        self.parent.changePage("mainPage")
