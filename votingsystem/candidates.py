from flask import Flask
import re
from bson.objectid import ObjectId

from pymongo import MongoClient 
import Credentials

db = Credentials.db

# Access collection of the database 
Area = db['Areas']
cand = db['candidates']
parties = db['Parties']
db_candidates = db['Candidates']

def search_candidate(candidate_id):
     try:

          myquery=({ "_id": ObjectId(candidate_id) })
          global candidate1
          candidate1 = db_candidates.find_one( myquery ) 
          
          return candidate1
     except:
          return 0


def delete_candidate(candidate_id,Admin_ID):
     try:
          myquery = {
                    "_id" : ObjectId(candidate_id)                  
                       }           
            
          res = db_candidates.find_one_and_delete(myquery)          
          print(res)
          return 0
     except:
          return 1 




def update_candidate(cand_id,cand_fname,cand_lname,cand_cnic,cand_email,cand_Dob,cand_number,cand_party,cand_constituency,Admin_ID):     
     try:
                  
          myquery = { "_id": ObjectId(cand_id)  }
          newvalues = { "$set": {  "cand_fname": cand_fname,
                                   "cand_lname": cand_lname,
                                   "cand_cnic": cand_cnic,
                                   "cand_email": cand_email,
                                   "cand_Dob": cand_Dob,
                                   "cand_number": cand_number,
                                   "cand_party": cand_party,
                                   "cand_constituency": cand_constituency
                                    } }
          print(myquery, newvalues)
          db_candidates.update_one(myquery, newvalues)
          return 1
     except:
          return 0 


      
          
















def Check_candidates_Name_Are_In_String_Avalablity_Of_Area_Name(cand_cnic):
     value=cand_cnic
     regax = re.compile('[!@#$%^&*()_:><}{]')

     if regax.search(value)==None:
            return False
     else:
            return value

def Add_candidates(cand_fname,cand_lname,cand_cnic,cand_email,cand_Dob,cand_number,cand_party,cand_constituency,Admin_ID):
      
    try :

         Checked = Check_candidates_Name_Are_In_String_Avalablity_Of_Area_Name(cand_cnic)

     #     print(cand_fname,cand_lname,cand_cnic,cand_email,cand_Dob,cand_number,cand_party,Admin_ID)
         val = db_candidates.find_one( {
                         "cand_cnic": cand_cnic,
                         "Admin_Id": Admin_ID
                         } ) 
         print(val)
         print(Checked)      
     
         if  Checked == False:

              if  val == None: 
                   rec  = {
                    "cand_fname": cand_fname,
                    "cand_lname": cand_lname,
                    "cand_cnic": cand_cnic,
                    "cand_email": cand_email,
                    "cand_Dob": cand_Dob,
                    "cand_number": cand_number,
                    "cand_party": cand_party,
                    "cand_constituency":cand_constituency,
                    "Admin_Id": Admin_ID
                    }   
                   rec= db_candidates.insert(rec)
                   return  0       
                                              # val= none means this area is not created before in the table
                    
              else :

                   return 1 
                         
         else:

              return 2 

    except:
                  
         return 3          



