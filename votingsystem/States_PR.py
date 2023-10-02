from flask import Flask
from bson.objectid import ObjectId
import re
from pymongo import MongoClient 

  
import Credentials

db = Credentials.db
# Access collection of the database 
db_States = db['States']

search_state1 = ''


def search_state(state_id):
     try:
          print(state_id)
          myquery=({ "_id": ObjectId(state_id) })
          global search_state1
          search_state1 = db_States.find_one( myquery ) 
          return search_state1
     except:
          return 0



def delete_state(state_id):
     try:
          myquery = {
                    "_id" : ObjectId(state_id)                  
                       }           
            
          print(myquery)
          res = db_States.find_one_and_delete(myquery)
          
          print(res)
          return 0
     except:
          return 1 







def update_state(state_name,Electoral_Votes,state_id):
     
     try:
          global search_state1
         
         
          myquery = { "_id": ObjectId(state_id) }
          newvalues = { "$set": { "State_name": state_name ,
                                   "Electoral_Votes": Electoral_Votes     } }

          db_States.update_one(myquery, newvalues)
          return 1
     except:
          return 0     













def Check_state_Name_Are_In_String_Avalablity_Of_Area_Name(state_name):
     value=state_name
     regax = re.compile('[!@#$%^&*()_:><}{1234156789]')

     if regax.search(value)==None:
            return False
     else:
            return value


def Add_States(State_name,Electoral_Votes):   
          
     try :
          Checked = Check_state_Name_Are_In_String_Avalablity_Of_Area_Name(State_name)

          val = db_States.find_one( {
                         "State_name": State_name                        
                              } ) 
          print(val)
          print(Checked)      
     
          if  Checked == False:
               if  val == None:                                   # val= none means this state is not created before in the table
                    rec  = {
                    "State_name": State_name,
                    "Electoral_Votes": Electoral_Votes
                     }   
                    rec= db_States.insert(rec) 
                    return  0
               else :
                     return 1 
                         
          else:
               return 2    
     except :
          return 3          

  


















def Insert_States():
     state = ['Alabama','Montana','Alaska','Nebraska','Arizona','Nevada','Arkansas','New Hampshire','California','New Jersey','Colorado','New Mexico','Connecticut','New York','Delaware','North Carolina','District of Columbia','North Dakota','Florida','Ohio','Georgia','Oklahoma','Hawaii','Oregon','Idaho','Pennsylvania','Illinois','Rhode Island','Indiana','South Carolina','Iowa','South Dakota','Kansas','Tennessee','Kentucky','Texas','Louisiana','Utah','Maine','Vermont','Maryland','Virginia','Massachusetts','Washington','Michigan','West Virginia','Minnesota','Wisconsin','Mississippi','Wyoming','Missouri']
     E_votes = [9,3,3,5,11,6,6,4,55,14,9,5,7,29,3,15,3,3,29,18,16,7,4,7,4,20,20,4,11,9,6,3,6,11,8,38,8,6,4,3,10,13,11,12,16,5,10,10,6,3,10]
    
     for i in range(0,51):
          rec = {
               "State_name":state[i],
               "Electoral_Votes" : int(E_votes[i])
          }
          rec= db_States.insert(rec)   
          print(rec)

# Insert_States()

#  stats = {'a':1000, 'b':3000, 'c': 100}
#      print(max(stats, key=stats.get))

 
         
  

