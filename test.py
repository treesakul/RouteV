import sys

from pyswip.prolog import Prolog

prolog = Prolog()
prolog.consult("test_final.pl")
start = 'c'
nodes = '[b,a,d,e]'
outcomes = list(prolog.query("travel("+start+","+nodes+",Path,C)."))
path_list = [] 
for i in range(len(outcomes[0]['Path'])): 
    path_list.append(str(outcomes[0]['Path'][i])) 

print(path_list)
print(outcomes[0]['C'])

prolog.assertz("arc(d,f, 10)")

#f = open('prologtest.pl', 'w')
#f = open('prologtest.pl', 'a')
#f.write('\nmother(c,b)')
#f.close()
