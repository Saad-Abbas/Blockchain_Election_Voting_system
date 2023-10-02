from flask import Flask, render_template,request,redirect,flash,url_for,session,g
import hashlib
import json
import os
import base64
from time import time
from datetime import datetime
from pymongo import MongoClient 
# import Signup_verification

client=MongoClient() 

# Connect with the portnumber and host 
client = MongoClient('localhost', 27017)
# Access database
db = client['votingsystem'] 

# Access collection of the database 
cand = db['candidates']
# cand = mydatabase['candidates']

from werkzeug.utils import secure_filename
app = Flask(__name__)
app.secret_key=os.urandom(24)


@app.route('/index')
def div():
     candidates_record =[]
     for x in cand.find():
        candidates_record.append(x)      
     return render_template('index.html',results=candidates_record)  

if __name__ == '__main__':
 app.run(debug=True)
    