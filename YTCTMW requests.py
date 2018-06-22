# -*- coding: utf-8 -*-
from pprint import pprint
import base64
import json
import requests #Python/Restapi package
#import urllib

#headers = {'Authorization':'token %s' % token}
#params  = {'page': 2, 'per_page': 100}
#auth=('user', 'pass')
#r = requests.get(url, params=params, headers=headers)

IP = "192.168.225.81"
Port = "3000"

def encodeb64(file): 
    #output a string from a jpg file, encode into b64 from jpg
    with open(file, "rb") as image_file:
        encoded_image = base64.b64encode(image_file.read())
    return encoded_image


def decodeb64(string, file): 
    #output a file from a string, decode from b64 to jpg
    imgdata = base64.b64decode(string)
    with open(file, 'wb') as f:
        f.write(imgdata)
    return file


class Yitu(object):
    
    def __init__(self, IP, Port):
        self.IP = IP
        self.Port = Port
        self.URL = "http://" + IP + ":" + Port
    
    def send(self, request): 
        #custom request in the form of "/fr/??"
        send = requests.get(self.URL + request)
        return send
    
    def ping(self): 
        #Get status of middleware
        send = requests.get(self.URL + "/fr/ping")
        return send
  
    def config(self): 
        #Get configuration of middleware
        send = requests.get(self.URL + "/fr/config")
        return send

    def tracking(self, identity, building=None, begintime=None, endtime=None): 
        #identity (compulsory), building (all or commonwealth), begintime (yyyymmdd_hhmmss), endtime (yyyymmdd_hhmmss)
        #Get alerts given person's identity. Filter by building, begintime, endtime
        URL = self.URL + "/fr/tracking?identity=" + identity
        
        if building != None:
            URL += '&building=' + building
        if begintime != None:
            URL += '&begintime=' + building
        if endtime != None:
            URL += '&endtime=' + building
        send = requests.get(URL)
        return send

    def logdetection	(self, category=None, building=None, begintime=None, endtime=None):
        #category (employee, visitor, blacklist, unidentified, all), building (all or commonwealth), begintime (yyyymmdd_hhmmss), endtime (yyyymmdd_hhmmss)
        #Get all alerts. Filter by building, category, begintime, endtime
        URL = self.URL + "/fr/logdetection?"
        if category != None:
            URL += 'category=' + category
        if building != None:
            if building != None and category == None:
                URL += 'building=' + building
            else:
                URL += '&building=' + building
        if begintime != None:
            if begintime != None and category == None and building == None:
                URL += 'begintime=' + begintime
            else:
                URL += '&begintime=' + begintime
        if endtime != None:
            if endtime != None and category == None and building == None and begintime == None:
                URL += 'endtime=' + endtime
            else:
                URL += '&endtime=' + endtime        
        send = requests.get(URL)
        return send

    def addmaster(self, identity, category, image, building=None, name=None):
        #Add a photo record given person's name, identity, image, category, building.
        image = encodeb64(image)
        URL = self.URL + "/fr/addmaster?image={}&category={}".format(identity, category, image) #employee, visitor, blacklist
        if building != None: #all or commonwealth
            URL += '&building=' + building
        if name != None:
            URL += '&name=' + name      
        send = requests.post(URL)
        return send

    def addmasterdata(self, category, building):
        #Get all photo records. Filter by category, building.
        send = requests.get(self.URL + "/fr/masterdata?category={}&building={}".format(category, building))
        return send

    def delmasterdata(self, identity, category, building):
        #Remove all photo records given person's identity, category and building
        send = requests.delete(self.URL + "/fr/masterdata?identity={}&category={}&building={}".format(identity, category, building))
        return send

'''
    def alertblacklist(self):
        #To provide blacklisted person detected and unidentified person detected.  
        #Alert to be provided immediately after the detection.
        send = requests.get("http://192.168.225.88:80/fr/alert/")
        return send
    
    def alertebc(self):
        #To provide the person or group of person (as a list) detected in front 
        #of the command-centre entrance door immediately after detection. 
        #If uncategorized, just return the person as unidentified.
        send = requests.get("http://192.168.225.88/fr/ebc/")
        return send
    
    def alertdetection(self):
        #To provide any person detection.  Alert to be provided immediately 
        #after the detection.
        send = requests.get("http://192.168.225.88:80/fr/detection/")
        return send
'''


Y = Yitu(IP, Port)
r = Y.config()
rt = r.text # Output as string
rs = r.json() # Output a json as dictionary
#pprint(rs)
print(rt)
print(json.dumps(rs, indent = 4))








