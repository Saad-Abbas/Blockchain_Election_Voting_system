from flask import Flask
from bson.objectid import ObjectId
import re
from pymongo import MongoClient 
import Credentials

db = Credentials.db
# Access collection of the database 
db_Presidential_candid  = db['db_Presidential_Candidates']
db_Presidential_parties = db['Presidential_Parties']
search_party1 = ''

def search_party(Party_id):
     try:
          print(Party_id)
          myquery=({ "_id": ObjectId(Party_id) })
          global search_party1
          search_party1 = db_Presidential_parties.find_one( myquery ) 
          return search_party1
     except:
          return 0



def delete_party(Party_id):
     try:
          myquery = {
                    "_id" : ObjectId(Party_id)                  
                       }           
            
          print(myquery)
          res = db_Presidential_parties.find_one_and_delete(myquery)
          
          print(res)
          return 0
     except:
          return 1 







def update_party(Party_name,Party_Image,party_id):
     
     try:
          global search_party1
         
         
          myquery = { "_id": ObjectId(party_id) }
          newvalues = { "$set": { "Party_name": Party_name,'Party_Image':Party_Image } }

          db_Presidential_parties.update_one(myquery, newvalues)
          return 1
     except:
          return 0     




def Check_Party_Name_Are_In_String_Avalablity_Of_Area_Name(Party_name):
     value=Party_name
     regax = re.compile('[!@#$%^&*()_:><}{1234156789]')

     if regax.search(value)==None:
            return False
     else:
            return value


def Add_Party(Party_name,Party_Image,Admin_ID):   
          
     try :
          Checked = Check_Party_Name_Are_In_String_Avalablity_Of_Area_Name(Party_name)

          val = db_Presidential_parties.find_one( {
                         "Party_name": Party_name,
                         'Party_Image':Party_Image,
                         "Admin_Id": Admin_ID
                              } ) 
          print(val)
          print(Checked)      
     
          if  Checked == False:
               if  val == None:                                   # val= none means this area is not created before in the table
                    rec  = {
                    "Party_name": Party_name,
                    'Party_Image':Party_Image,
                    "Admin_Id": Admin_ID
                     }   
                    rec= db_Presidential_parties.insert(rec) 
                    return  0
               else :
                     return 1 
                         
          else:
               return 2    
     except :
          return 3          

  