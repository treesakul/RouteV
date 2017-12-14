
import urllib.request 
import json
import re
import sys
import textwrap

from pyswip.prolog import Prolog

class MainSystem:

    def __init__(self):
        self.api_key = "AIzaSyB70wPQAQR-5P86DJ2j1QcAgYVbR0-xD_k"
        self.prolog = Prolog()


    def get_existing_nodes(self):
        self.prolog.consult("nodes_kb.pl")
        try:
            outcomes = list(self.prolog.query("node(P_id,Name,Address)."))
        except:
            outcomes = []
        return outcomes

    def get_distance(self,p1,p2):
        distance = 0
        self.prolog.consult("pairs_kb.pl")
        try:
            distance = list(self.prolog.query("arc("+p1+","+p2+",Distance)."))
            if(distance == []):
                distance = list(self.prolog.query("arc("+p2+","+p1+",Distance)."))
        except:
            distance = 0
        return distance[0]['Distance']        

    def write_node(self, p_id,name, address):

        replace_list = [' ','/',',','-','_']
        f = open('nodes_kb.pl', 'a')
        
        for i in replace_list:
            if(i == '/'):
                p_id = p_id.replace(i, 'xSLASHx')
                name = name.replace(i,'xSLASHx')
                address = address.replace(i,'xSLASHx')
            elif (i == '-'):
                p_id = p_id.replace(i, 'xMINUSx')
                name = name.replace(i, 'xMINUSx')
                address = address.replace(i,'xMINUSx')
            elif (i == '_'):
                p_id = p_id.replace(i, 'xUNDERx')
                name = name.replace(i, 'xUNDERx')
                address = address.replace(i,'xUNDERx')
            elif(i == ','):
                p_id = p_id.replace(i, 'xCOMMAx')
                name = name.replace(i, 'xCOMMAx')
                address = address.replace(i,'xCOMMAx')
            elif(i == ' '):
                p_id = p_id.replace(i, 'xSPACEx')
                name = name.replace(i, 'xSPACEx')
                address = address.replace(i,'xSPACEx')
        address = 'a'+re.sub('[^A-Za-z0-9 _]+', '', address)
        name = 'n'+re.sub('[^A-Za-z0-9 _]+', '', name)
        p_id = 'x'+p_id.replace('-','_')
        
        statement = '\nnode('+p_id+','+name+','+address+').'
        f.write(statement)
        
        f.close()

    def add_stop(self,p_id,name, address):
        
        ex_nodes = self.get_existing_nodes()
        formatted_p_id = 'x'+p_id.replace('-','xMINUSx').replace('_','xUNDERx')
        f = open('pairs_kb.pl', 'a')
        No_duplicate = True
        
        for check in ex_nodes:
            if(formatted_p_id == check['P_id']):
                No_duplicate = False
    
        
        if(No_duplicate == True):
            
            for i in ex_nodes:
                
                existing_p_id = i['P_id']
                formatted_existing_p_id = existing_p_id.replace('xMINUSx','-').replace('xUNDERx','_')[1:]
                
                url = "https://maps.googleapis.com/maps/api/distancematrix/json?origins=place_id:"+p_id+"&destinations=place_id:"+formatted_existing_p_id+"&key="+self.api_key
                
                response = urllib.request.urlopen(url)
                data = json.loads(response.read().decode())
                distance_str = data['rows'][0]['elements'][0]['distance']['text']
                distance = float(re.findall("\d+\.\d+",distance_str)[0])

                f.write('\narc('+formatted_p_id+','+existing_p_id+','+str(distance)+').')
    
            self.write_node(p_id,name, address)
        f.close()

        
    
        
    def get_shortest_path(self,start,nodes):
        
        self.prolog.consult("test_final.pl")
        
        outcomes = list(self.prolog.query("travel("+start+","+nodes+",Path,C)."))
        path_list = []
        
        for i in range(len(outcomes[0]['Path'])): 
            path_list.append(str(outcomes[0]['Path'][i])) 

        f_outcomes = []
        f_outcomes.append(path_list)
        f_outcomes.append(outcomes[0]['C'])

        return f_outcomes


    

#a = MainSystem()
#a.write_node('ChIJ1aHcG-2e4jARdY3X0l-TWeI','The Mark Condo Airport Link, Capital One Real Estate','Chaturathit Khwaeng Makkasan, Khet Ratchathewi, Krung Thep Maha Nakhon 10210, Thailand')
#a.add_stop('ChIJxwUjljVmHTERXN9ls6L6FEQ','Central Library, King Mongkuts Institute of Technology Ladkrabang','Lat Krabang, Bangkok 10520, Thailand')
#a.add_stop('ChIJ93TVWM2e4jARpdOqzD2iNqM','Siam Paragon','991/1 ถนนพระราม 1 แขวงปทุมวัน Khet Pathum Wan, Krung Thep Maha Nakhon 10330, Thailand')
#a.get_existing_nodes()
#a.get_shortest_path('xChIJxwUjljVmHTERXN9ls6L6FEQ', '[xChIJ1aHcGxMINUSx2e4jARdY3X0lxMINUSxTWeI,xChIJqxMINUSxI3V62f4jAR8QRewT7N3to]')
#a.add_stop('kmitl')
