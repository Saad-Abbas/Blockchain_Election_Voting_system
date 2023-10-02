from flask import Flask
from pymongo import MongoClient 
import re
from bson.objectid import ObjectId
import Credentials

db = Credentials.db
# Access collection of the database 
db_Presidential_voter = db['Presidential_Voter']


search_voter1 = ''

def search_voter(voter_id):
     try:
          # print(voter_id)
          myquery=({ "_id": ObjectId(voter_id) })
          global search_voter1
          search_voter1 = db_Presidential_voter.find_one( myquery ) 
          return search_voter1
     except:
          return 0



def delete_voter(voter_id,Admin_Id):
     try:
          myquery = {
                    "_id" : ObjectId(voter_id)                           
                       }           
            
          print(myquery)
          
          res = db_Presidential_voter.find_one_and_delete(myquery)
          
          print(res)
          return 0
     except:
          return 1 


def update_voter(voter_fname,voter_lname,voter_cnic,voter_Father_cnic,voter_email,voter_Dob,voter_number,voter_state,Admin_ID,voter_id):
     # print(Party_name,Party_country)
     try:
          global search_voter1
         
          myquery = { "_id": ObjectId(search_voter1['_id']) }
          newvalues = { "$set": { 
                              "Voter_Fname": voter_fname,
                              "Voter_Lname": voter_lname,
                              "Voter_CNIC": voter_cnic,
                              "Voter_Father_CNIC": voter_Father_cnic,
                              "Voter_Email": voter_email,
                              "Voter_DOB": voter_Dob,                         
                              "Voter_Pno": voter_number,                             
                              "Voter_State": voter_state
                              
                                } }

          db_Presidential_voter.update_one(myquery, newvalues)
          return 1
     except:
          return 0     










def Check_Name_Are_In_String_And_Avalablity_Of_Name(name):
     value=name
     regax = re.compile('[!@#$%^&*()_:><}{]')

     if regax.search(value)==None:
            return False
     else:
            return value
        

def Add_voter(voter_fname,voter_lname,voter_cnic,voter_Father_cnic,voter_email,voter_Dob,voter_number,voter_state,Admin_ID):
     
     try :
          Checked = Check_Name_Are_In_String_And_Avalablity_Of_Name(voter_cnic)

          # print(Voter_fname,Voter_lname,Voter_cnic,Voter_email,Voter_party,Voter_dob,Voter_province,Voter_pno,Voter_type,Admin_ID)
          val = db_Presidential_voter.find_one( {
                             "Admin_ID": Admin_ID,                             
                             "Voter_CNIC": voter_cnic                        

                         } ) 
          print(val)
          print(Checked)     
          
     
          if  Checked == False:
               if  val == None:                                  
                    rec  =  {  
                              "Admin_ID": Admin_ID,
                              "Voter_Fname": voter_fname,
                              "Voter_Lname": voter_lname,
                              "Voter_CNIC": voter_cnic,
                              "Voter_Father_CNIC": voter_Father_cnic,
                              "Voter_Email": voter_email,
                              "Voter_DOB": voter_Dob,                         
                              "Voter_Pno": voter_number,                             
                              "Voter_State": voter_state
                              
                                }
                    rec= db_Presidential_voter.insert(rec)   
                    return  0
               else :
                     return 1 
                         
          else:
               return 2    
     except :
          return 3


