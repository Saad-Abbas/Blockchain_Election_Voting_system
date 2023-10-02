from flask import Flask

from pymongo import MongoClient 
  
# creation of MongoClient 
client=MongoClient() 

                              # mongodb+srv://saad:62908@cluster0.ojeri.mongodb.net/myFirstDatabase?retryWrites=true&w=majority
# Altas_connection_string = 'mongodb+srv://saad:62908@cluster0.ojeri.mongodb.net/myFirstDatabase?authSource=admin&replicaSet=atlas-grm07z-shard-0&w=majority&readPreference=primary&retryWrites=true&ssl=true'
local_connection_string = 'localhost'
local_port_number = 27017
# Connect with the portnumber and host 
client = MongoClient(local_connection_string,local_port_number)
# client = MongoClient(Altas_connection_string)

# Access database
db = client['votingsystem'] 
