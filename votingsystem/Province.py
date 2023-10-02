from flask import Flask
import re
from bson.objectid import ObjectId
from pymongo import MongoClient 

import Credentials

db = Credentials.db

# Access collection of the database 

db_Province = db['Province']
db_PA = db['PA']
province1 =''

def search_province(Province_id):
     try:

          myquery=({ "_id": ObjectId(Province_id) })
          global province1
          province1 = db_Province.find_one( myquery ) 
          
          return province1
     except:
          return 0


def delete_province(Province_id):
     try:
          myquery = {
                    "_id" : ObjectId(Province_id)                  
                       }           
            
          print(myquery)
          res = db_Province.find_one_and_delete(myquery)
          
          print(res)
          return 0
     except:
          return 1 




def update_province(Province_id,Province_Name,Admin_ID):     
     try:
         
        
          Checked = Check_Province_Name_Are_In_String_Avalablity_Of_Area_Name(Province_Name)
          val = db_Province.find_one( {
                         "Province_Name": Province_Name,
                         "Admin_ID": Admin_ID
                         } ) 
          print(val)
          print(Checked)      
     
          if  Checked == False:
               if  val == None:                                   # val= none means this area is not created before in the table With this admin ID
                    
                    myquery = { "_id": ObjectId(Province_id)  }
                    newvalues = { "$set": {  "Province_Name": Province_Name } }
                    print(myquery, newvalues)
                    db_Province.update_one(myquery, newvalues)
                    return  0
               else :
                    return 1 
                         
          else:
               return 2    
     except :
          return 3           


      
          
          
     


def Check_Province_Name_Are_In_String_Avalablity_Of_Area_Name(Province_name):
     value=Province_name
     regax = re.compile('[!@#$%^&*()_:><}{1234156789]')

     if regax.search(value)==None:
          return False
     else:
          return value

def Add_province(Province_name,Admin_ID):
     
     try :
          Checked = Check_Province_Name_Are_In_String_Avalablity_Of_Area_Name(Province_name)
          val = db_Province.find_one( {
                         "Province_Name": Province_name,
                         "Admin_ID": Admin_ID
                         } ) 
          print(val)
          print(Checked)      
     
          if  Checked == False:
               if  val == None:                                   # val= none means this area is not created before in the table With this admin ID
                    
                    rec  = {
                         "Province_Name": Province_name,
                         "Admin_ID": Admin_ID
                         }
                    rec= db_Province.insert(rec)   
                    return  0
               else :
                     return 1 
                         
          else:
               return 2    
     except :
          return 3          

                  

                     
# check for Area list remove those areas whose names are already selected in another NA-Seat
     

def check_province(PA_id,Admin_ID):   #AdminID
     Province_name_in_PA = []
     A_name = []

     # Election_ID = db_PA.find_one({'_id':ObjectId(PA_id), 'Admin_ID':Admin_ID})
     # print(Election_ID['Election_ID'])

     # for i in db_PA.find({'Election_ID': ObjectId( Election_ID['Election_ID']),'Admin_ID':ObjectId(Admin_ID)}):#AdminID
     #      Province_name_in_PA.append(i['Province_Name'])
     
     # print('province name in PA  table:')
     # print(Province_name_in_PA)

     for i in db_Province.find({'Admin_ID':ObjectId(Admin_ID)}): #AdminID
          A_name.append(i['Province_Name'])

     # print('Province name in  table')
     # print(A_name)

     # for element in Province_name_in_PA:
     #      if element in A_name:
     #           A_name.remove(element)
     # print('final list of Province_name')
     print(A_name)
     return A_name
    
    
    