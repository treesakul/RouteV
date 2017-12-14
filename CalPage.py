from PyQt4.QtCore import *
from PyQt4.QtGui import *
from PyQt4.QtWebKit import *
import os

from WriteHTML import *
from CalWidget import *
import urllib.request
import webbrowser

class CalPage(QMainWindow):
    def __init__(self, parent = None, controller = None):
        QMainWindow.__init__(self, parent = None)
        self.parent = parent
        self.controller = controller
        
        self.init()
        
    def reset(self):
        self.init()

    def init(self):
        #Create a new stacked layout
        self.stackedLayout = QStackedLayout()

        #Create the stacked widget
        self.p_id_names = {}
        self.p_id_address = {}
        self.outcomes = []
        self.stackedWidget = QWidget()
        self.mainGridLayout = QGridLayout()
        self.map = CalWidget()###
        self.name_buttons = {}
        self.scroll = QScrollArea()
        self.info_widget = QWidget()
        self.info_layout = QVBoxLayout()
        self.scroll2 = QScrollArea()
        self.info_name = QLabel()
        self.info_address = QLabel()
        self.outcome_names = []
        self.back_bt = QPushButton("Back")
        self.add_bt = QPushButton("Add stops")
        self.cal_bt = QPushButton("Calculate")
        self.map_bt = QPushButton("Show on google map")
        self.labels = []
        self.origin = ""
        self.waypoints = []
        self.rad_buttons = {}
        self.html = ""
        self.final_info = QWidget()
        self.final_info_layout = QVBoxLayout()
        self.boldFont= QFont()
        self.boldFont.setBold(True)
        self.info_name.setFont(self.boldFont)
        self.instruction = QLabel()
        self.pair_distance = []
        self.instruction.setText('Select all the stops that need to be calculated')
        self.final_info.setLayout(self.final_info_layout)
        
        self.stackedWidget.setLayout(self.stackedLayout)
        
        self.info_widget.setStyleSheet("border: 0.5px solid;border-color: grey;")
        self.info_name.setStyleSheet("border: 0px;")
        self.info_address.setStyleSheet("border: 0px;")

        #Set the windows central widget
        self.setCentralWidget(self.stackedWidget)

        #Connections
        self.add_bt.clicked.connect(self.add_mark)
        self.map_bt.clicked.connect(self.show_map)
        self.cal_bt.clicked.connect(self.calculate)
        self.back_bt.clicked.connect(self.back)
        
        #add main widget
        self.mainWidget = QWidget()
        self.mainWidget.setLayout(self.mainGridLayout)
        
        #Add to Stacked Layout
        self.stackedLayout.addWidget(self.mainWidget)

        #self.set_search()
        
        #Generate Initial Layout
        topic = QLabel()
        topic.setText("Stop detail")
        topic.setStyleSheet("border: 0px;")
        topic.setFont(self.boldFont)
        self.info_layout.addWidget(topic)
        
        self.info_layout.addWidget(self.info_name)
        self.info_layout.addWidget(self.info_address)
        self.info_widget.setLayout(self.info_layout)
        
        #add to layout    
        self.mainGridLayout.addWidget(self.map)
        self.mainGridLayout.addWidget(self.instruction)
        self.mainGridLayout.addWidget(self.scroll)
        self.mainGridLayout.addWidget(self.scroll2)
        self.mainGridLayout.addWidget(self.info_widget)
        self.mainGridLayout.addWidget(self.final_info)
        self.mainGridLayout.addWidget(self.map_bt)
        self.mainGridLayout.addWidget(self.add_bt)
        self.mainGridLayout.addWidget(self.cal_bt)
        self.mainGridLayout.addWidget(self.back_bt)

        self.cal_bt.hide()
        self.scroll2.hide()
        self.info_widget.hide()
        self.map_bt.hide()
        self.final_info.hide()
        self.map.hide()
            
        self.set_scroll()


    def set_scroll(self):

        self.widgetS = QWidget()  # create very large + long widget
        self.layoutx = QVBoxLayout()
        
        self.name = self.controller.get_existing_nodes()

        for i in self.name:
            name = i['Name']
            p_id = i['P_id']
            address = i['Address']
            name = name.replace('xSLASHx','/').replace('xMINUSx','-').replace('xUNDERx','_').replace('xCOMMAx',',').replace('xSPACEx',' ')[1:]
            address = address.replace('xSLASHx','/').replace('xMINUSx','-').replace('xUNDERx','_').replace('xCOMMAx',',').replace('xSPACEx',' ')[1:]

            self.p_id_names[p_id] = name
            self.p_id_address[p_id] = address
            
            layouth = QHBoxLayout()
            button = QCheckBox(name)
            self.name_buttons[button] = p_id
       
            layouth.addWidget(button)
            
            self.layoutx.addLayout(layouth)

            
        self.layoutx.setAlignment(Qt.AlignTop)
        self.widgetS.setLayout(self.layoutx)
        self.scroll.setWidget(self.widgetS)

    def calculate(self):
        for r in self.rad_buttons:
            if(r.isChecked()):
                p_id = self.rad_buttons[r]
                self.origin = str(p_id)
                self.waypoints.remove(p_id)
        self.outcomes = self.controller.get_shortest_path(self.origin, str(self.waypoints))
        
        self.html = write_html(self.outcomes[0])
        f = open('route_html.html','w')
        f.write(self.html)
        f.close()
        self.show_output()
    
    def show_output(self):
        self.instruction.setText('The shortest route calculated from the stops (click to see each stop in detail)')
        count = 1
        self.add_bt.hide()
        self.cal_bt.hide()
        self.scroll.hide()
        self.map.hide()
        self.info_buttons = {}
        self.widgetS = QWidget()  # create very large + long widget
        self.layoutx = QVBoxLayout()
        
        for b in self.outcomes[0]:
            layouth = QHBoxLayout()
            bt = QPushButton('Destination '+str(count)+': '+self.p_id_names[b])
            bt.setStyleSheet("QPushButton { text-align: left; }")
            self.outcome_names.append(self.p_id_names[b])
            self.info_buttons[bt] = b
            layouth.addWidget(bt)
            bt.clicked.connect(self.show_info)
            self.layoutx.addLayout(layouth)
            count += 1

        for d in range(len(self.outcomes[0])):
            num = d
            num2 = (d+1)%(len(self.outcomes[0]))
            distance = self.controller.get_distance(str(self.outcomes[0][num]),str(self.outcomes[0][num2]))
            self.pair_distance.append(distance)
        
        self.final_info.setStyleSheet("border: 0.5px solid; border-color: grey;")

        #add topic
        topic = QLabel()
        topic.setText("Distance between stops")
        topic.setStyleSheet("border: 0px;")
        topic.setFont(self.boldFont)
        self.final_info_layout.addWidget(topic)
        
        for p in range(len(self.pair_distance)):
            num = p
            num2 = (num+1)%(len(self.pair_distance))
            text = str(self.pair_distance[num])+" km from "+str(self.outcome_names[num])+" to "+str(self.outcome_names[num2])
            label = QLabel()
            label.setText(text)
            label.setStyleSheet("border: 0px;")
            self.final_info_layout.addWidget(label)
            
        self.layoutx.setAlignment(Qt.AlignTop)
        self.widgetS.setLayout(self.layoutx)
        self.scroll2.setWidget(self.widgetS)
        final = QLabel()
        final.setText("Total distance : "+str(self.outcomes[1]))
        final.setStyleSheet("border: 0px;")
        final.setFont(self.boldFont)
        self.final_info_layout.addWidget(final)
        self.scroll2.show()
        self.info_widget.show()
        self.map_bt.show()
        self.final_info.show()

    def show_info(self):
        
        sender = self.sender()
        p_id = self.info_buttons[sender]
        self.info_name.setText(self.p_id_names[p_id])
        self.info_address.setText(self.p_id_address[p_id])
    
    def show_map(self):
        #print(os.getcwd()+"\route_html.html")
        url = os.path.realpath("route_html.html")
        webbrowser.open(url)
        
    def add_mark(self):
        
        self.instruction.setText('Select the origin')
        self.widgetS = QWidget()  # create very large + long widget
        self.layoutx = QVBoxLayout()
        
        for b in self.name_buttons:
            if(b.isChecked()): 
                layouth = QHBoxLayout()
                bt = QRadioButton(b.text())
                self.waypoints.append(self.name_buttons[b])
                self.rad_buttons[bt] = self.name_buttons[b]
                layouth.addWidget(bt)
        
                self.layoutx.addLayout(layouth)

        self.layoutx.setAlignment(Qt.AlignTop)
        self.widgetS.setLayout(self.layoutx)
        self.scroll.setWidget(self.widgetS)
        
     
        self.add_bt.hide()
        self.cal_bt.show()
        

                
    def set_search(self):
        #search init
        self.model = QStringListModel()

        nodes = self.controller.get_existing_nodes()
        nodes_dict = {}
        name_list = []
        for i in nodes:
            name = i['Name'].replace('_',' ')[1:]
            p_id = i['P_id'].replace('_','-')[1:]
            name_list.append(name)
            nodes_dict[name] = p_id
            
        self.model.setStringList(name_list)

        self.completer = QCompleter()
        self.completer.setModel(self.model)

        self.lineedit = QLineEdit()
        self.lineedit.setCompleter(self.completer)
        
        self.lineedit.show()
        self.mainGridLayout.addWidget(self.lineedit)

    def back(self):
        self.parent.changePage("mainPage")
