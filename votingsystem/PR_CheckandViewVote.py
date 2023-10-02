from flask import Flask
from bson.objectid import ObjectId
import re
from pymongo import MongoClient 
import PR_B_chain
import Credentials

db = Credentials.db
# Access collection of the database 

db_Cand = db['Presidential_Candidates']
db_parties = db['Presidential_Parties']

db_PA_Elections = db['Create_Presidential_Election']
db_voter = db['Presidential_Voter']
db_PR = db['PR']

db_ballot = db['Presidential_Ballot']
record =''
Search_PR = ''
rec = ''



def check_election(Admin_ID,Voter_ID):            # check by ADmin and voter ID and Status = Ready 
     try : 
          Voter_ID = ObjectId(Voter_ID)
          Admin_ID = ObjectId(Admin_ID)
         
          global record
          for record in db_PA_Elections.find({"Admin_ID": Admin_ID,"Status" : 'Running' }):
               print(record)                  
               return record
               

     except:
          print('Not found')










def elect(election_rec,Voter_ID,Admin_ID):
     # try:
          Voter_ID = ObjectId(Voter_ID)                   
          
          print(election_rec['Status'])

          global rec
          rec = db_voter.find_one({'_id':Voter_ID})

          Voter_State = rec['Voter_State']
          print(Voter_State)

          election_name = election_rec['Election_Name']
          print(election_name)

          global Search_PR
          Search_PR = db_PR.find_one({'State_Name':Voter_State,'Election_Name': election_name })
          
          Voter_CNIC = rec['Voter_CNIC']
          # check = check_for_voter_already_voted(election_name,Admin_ID,Voter_CNIC)
          # check1 = check_empty_candidates(Search_PR)
          print(Search_PR)
          print('length of candidate list ---',len(Search_PR['Cand_list']))
          if Search_PR != None:
               check1 = check_empty_candidates(Search_PR)        
               check_for_vote = check_for_voter_already_voted(election_name,Admin_ID,Voter_CNIC)

               if check1 == 0:   # if check1== 0 no candidate is elected from your state
                    return  0  

               elif  check_for_vote == 0 and check1 == 1:  # if check_for_vote== 0 means voter is not voted yet...
                    return Search_PR                       # check1 == 1 means candidate is availabe from this state
                    
               elif  check_for_vote == 1: # if check_for_vote == 1 means voter already voted.. 
                    return  1  
          else :                                  #  Search_PR ==  None: means not filled this seat with state name or area name
               return 0          
     # except:
     #      print("error") 

def check_for_voter_already_voted(election_name,Admin_ID,Voter_CNIC):
     Search_vote = db_ballot.find_one({'Admin_ID':str(Admin_ID),'Election_name': election_name , 'Voter_CNIC':Voter_CNIC })
     print('Vote-------------------------------------',Search_vote)
     if Search_vote == None :
          return 0                           #it means Voter Vote for the First Time
     else :
          return 1                           #it means Voter Voted Already in this Election




def Search_each_candidate_record(PR_seat):               # search each candidate record by CNIC who is elected in that specific NA Seat
    
     Admin_ID = ObjectId(PR_seat['Admin_ID'])
     candidates_list = []
     party_logo_path =[]     
     election_votes = db_PA_Elections.find_one({'Admin_ID':ObjectId(Admin_ID) ,'Status' :'Running' })
     datetime_end_of_election  = election_votes['Election_End_Time'] 
     
     for candidate_cnic in PR_seat['Cand_list']:
          if candidate_cnic != '' : 
               cand_data = db_Cand.find_one({"Admin_Id": Admin_ID,"cand_cnic" : candidate_cnic })          # search all candidates record using CNIC that are stored in NA-No (seat)
               party_image = db_parties.find_one({'Party_name':cand_data['cand_party'],'Admin_Id': ObjectId(Admin_ID)})                
               party_logo_path.append(party_image['Party_Image'])
               candidates_list.append(cand_data)
     return candidates_list,party_logo_path,datetime_end_of_election

def generate_vote_record(Admin_ID,Voter_ID,cand_cnic):

     vote= []
     block_chain = PR_B_chain.Blockchain()
     candiate_record = db_Cand.find_one({"Admin_Id": Admin_ID,"cand_cnic" : cand_cnic })


     vote.extend((record['Election_Name'],Search_PR['State_Name'],rec['Voter_CNIC'],cand_cnic,candiate_record['cand_party'],ObjectId(Admin_ID)))  # Search_PR['Area_Name']
     
     print("-----------------------Vote--------------------------------\n")
     print(vote)
      # this if condition verify that one voter cast it's vote only once
     check = check_voter_in_Ballot_Box(vote[2])
     print("-----------------------Check--------------------------------\n")
     print(check)

     if check == 0:
          nonce = PR_B_chain.proof_of_work()

          print("-----------------------nonce--------------------------------\n")
          print(nonce)
          
          # print("-----------ada----------",vote)
          block_chain.Add_new_block(PR_B_chain.block(nonce,vote[0],vote[1],vote[2],vote[3],vote[4],str(vote[5])))
          PR_B_chain.creat_chain(block_chain)
     
     else:
          print("voter is already exist")

    
    
     return vote                                                                                                                                 #complete data that shoud be mined for a vote

def check_voter_in_Ballot_Box(voter_cnic):
     global search
     # block_chain = PR_B_chain.Blockchain()
     if db_ballot.find_one({"Voter_CNIC" : voter_cnic} == voter_cnic) :
          print("voter is already exist")
          return 1
     else:
          print("not exist")
          return 0


def check_empty_candidates(record):   #check for cand list if and cnic is fill than allow to pass that record to front-end otherwise no candidate is elected from your State
     count = 0
     if record != None:
          for i in record['Cand_list']:
               if i == '':
                    count = count + 1
               else:
                    return 1
          return 0
     else :
          return 1





