from flask import Flask

from pymongo import MongoClient 

from bson.objectid import ObjectId
import Credentials
# creation of MongoClient 
# client=MongoClient() 

local_connection_string = 'localhost'
local_port_number = 27017
# Connect with the portnumber and host 
client = MongoClient(local_connection_string,local_port_number)
# client = MongoClient(Altas_connection_string)

# Access database
db = client['votingsystem'] 
dicttt =dict()
records = db['States']
for i in records.find({}):
    dicttt[i['State_name']] = int(i['Electoral_Votes'])
    
print(dicttt)
