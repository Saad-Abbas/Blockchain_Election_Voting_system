from flask import Flask
from bson.objectid import ObjectId
from pymongo import MongoClient 
import Credentials

db = Credentials.db

# Access collection of the database 
signups_block = db['signups']
Presidential_signups_block = db['presidential_signups']
cand = db['candidates']
db_Voter = db['Voter']
db_Presidential_Voter = db['Presidential_Voter']

def search_cnic(cnic):
     try:
          for singlerecord in db_Voter.find({'Voter_CNIC': cnic}):
               email = singlerecord
          return email
     except:
          return 0     
    


def Internationa_Voter_Signin(cnic):
     try:
          for singlerecord in db_Presidential_Voter.find({'Voter_CNIC': cnic}):
               email = singlerecord
          return email
     except:
          return 0  




def Local_admin_signin(admin_cnic,admin_pass):
     try:
          for singlerecord in signups_block.find({'admin_cnic': admin_cnic ,'admin_pass': admin_pass}):
               # cnic = singlerecord['admin_cnic']
               # password = singlerecord['admin_cnic']
               # admin_id = singlerecord['_id']
               # if cnic == admin_cnic and password == admin_pass :
               #      return cnic              #  means admin successfully login
               # else:
               #      return 1   
               return singlerecord
                          
     except:
          return 0     


def International_admin_signin(admin_cnic,admin_pass):
     try:
          for singlerecord in Presidential_signups_block.find({'admin_cnic': admin_cnic ,'admin_pass': admin_pass}):
               # cnic = singlerecord['admin_cnic']
               # password = singlerecord['admin_cnic']
               # admin_id = singlerecord['_id']
               # if cnic == admin_cnic and password == admin_pass :
               #      return cnic              #  means admin successfully login
               # else:
               #      return 1   
               return singlerecord
                          
     except:
          return 0           
        
    
def Local_signup_verify(admin_username,admin_cnic,admin_fname,admin_lname,admin_email,admin_gender,admin_phone,admin_pass,admin_repass):
      
     #  value = db.cand.find( {'admin_cnic': admin_cnic } ).limit(1)

     try:
          rec  = {
                    "admin_username": admin_username,
                    "admin_fname": admin_fname,
                    "admin_lname": admin_lname,
                    "admin_email": admin_email,
                    "admin_phone": admin_phone,
                    "admin_cnic": admin_cnic,
                    "admin_gender": admin_gender,
                    "admin_pass": admin_pass,
                    "admin_repass": admin_repass
                    
                         }   
          rec= signups_block.insert(rec)
          return 0

     except:
          return 1
                       
  
    
        


def International_signup_verify(admin_username,admin_cnic,admin_fname,admin_lname,admin_email,admin_gender,admin_phone,admin_pass,admin_repass):
      
     #  value = db.cand.find( {'admin_cnic': admin_cnic } ).limit(1)

     try:
          rec  = {
                    "admin_username": admin_username,
                    "admin_fname": admin_fname,
                    "admin_lname": admin_lname,
                    "admin_email": admin_email,
                    "admin_phone": admin_phone,
                    "admin_cnic": admin_cnic,
                    "admin_gender": admin_gender,
                    "admin_pass": admin_pass,
                    "admin_repass": admin_repass
                    
                         }   
          rec= Presidential_signups_block.insert(rec)
          return 0

     except:
          return 1
            