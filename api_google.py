import urllib.request 
import json
import re
url = "https://maps.googleapis.com/maps/api/distancematrix/json?origins=FriedDays&destinations=Esplanad+Ratchada&key=AIzaSyDtQ4hljXbyANCl36oy89j7g_NRuQRUziM"
response = urllib.request.urlopen(url)
data = json.loads(response.read().decode())
d = data['rows'][0]['elements'][0]['distance']['text']
dis = float(re.findall("\d+\.\d+",d)[0])
print(dis)
