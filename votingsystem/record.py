from flask import Flask, render_template,request,redirect
from hashlib import sha256
import hashlib
import json
import os
from time import time
from datetime import datetime
import record
import json


from werkzeug.utils import secure_filename
BLOCKCHAIN_DIR = os.curdir + '/requirements/'


data = {}
    


def add_into_list(candidate_Area,candidate_Cnic,candidate_name,candidate_Party,counter):
    global data
# Main Function  
    data['candidate_'+str(counter)+' Area '] = candidate_Area
    data['candidate_'+str(counter)+' CNIC '] =candidate_Cnic
    data['candidate_'+str(counter)+' Name  '] =candidate_name
    data['candidate_'+str(counter)+' Party '] =candidate_Party
    return data

# Taking input key = 1, value = Geek 
    # data = {
    #             'candidate_'+str(counter) : candidate_Cnic,
    #             'Party_name': candidate_name,
    # }
    

    # with open(BLOCKCHAIN_DIR +"sample.json", "r+") as file:
    #     data = json.load(file)
    #     data.update(data1)
    #     file.seek(0)
    #     json.dumps(data, file)

    # with open(BLOCKCHAIN_DIR +"sample.json") as json_file: #load existing data
    #     json_data = json.load(json_file)
    #     result =json_file.update(data)
    # with open('sample.json', 'a') as outfile:
    #     json.dump(result, outfile)
    
    # dictionary_records["candidate_"+str(counter)] = candidate_Cnic 
    # dictionary_records["candidate_name"] = candidate_name 
    # with open(BLOCKCHAIN_DIR +  'sample.json', 'W') as file:
    #      json.dump(data, file, indent=2, ensure_ascii=False)
    #      print(candidate_Cnic+'  '+candidate_name)
    

    
    
    # return dictionary_records