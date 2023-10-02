from pymongo import MongoClient 
from flask import Flask
from bson.objectid import ObjectId
import Credentials

db = Credentials.db

# Access collection of the database 
db_ballot = db['Presidential_Ballot']
db_election = db['Create_Presidential_Election']
db_na = db['PR']
db_candidates = db['Presidential_Candidates']
db_party = db['Presidential_Parties']
db_States = db['States']
Total_Votes = 0
E_Record= '' 


def vote_Count(election_id,Admin_ID): #-----------insert Admin_Id parameter
    result =[]
    vote = dict()
    Win_rec =dict()
    NA_list = []
    

    
    global E_Record
    E_Record = db_election.find_one({'_id': ObjectId(election_id)}) #insert AdminID Parameter here
    if E_Record != None:

        Election_Name = E_Record['Election_Name']
        # Admin_ID = Election_Record["Admin_ID"]


        for i in db_na.find({'Election_ID': ObjectId(election_id),'Admin_ID': ObjectId(Admin_ID) }): #insert AdminID Parameter here 
            NA_list.append(i) 

        if NA_list != "":

            for i in range(0,len(NA_list)):
                # vote['NA_No'] = NA_list[i]['NA_No']
                vote['State_Name'] = NA_list[i]['State_Name']
                # print('----------------state name---------',vote['State_Name'] )
                        
                # vote.append('NA_No : ' +  str(NA_list[i]['NA_No']))
                length = len(NA_list[i]['Cand_list'])
                # print('loop length---------------------------------',length)

                for j in range(0,length):
                 
                    if NA_list[i]['Cand_list'][j] != "":

                        Candidate_Record = db_candidates.find_one({'cand_cnic': NA_list[i]['Cand_list'][j]})  #insert AdminID Parameter here

                        if Candidate_Record != "" and Candidate_Record !=None:
                            Party_Name = Candidate_Record['cand_party']
                            Cand_CNIC = Candidate_Record['cand_cnic']
                            cand_fname = Candidate_Record['cand_fname']
                                    
                                    
                                    
                            count = db_ballot.count_documents({'Candidate_CNIC': Cand_CNIC,'Vote':Party_Name,'State_Name': NA_list[i]['State_Name'],'Election_name':NA_list[i]['Election_Name'],'Admin_ID': str(Admin_ID)})
                            global Total_Votes
                            Total_Votes = Total_Votes + count
                                    # count = db_ballot.count_documents((rec))
                                    
                                    # vote.append(" " + Party_Name + ": " + str(count))
                            
                            # vote['Area Name'] = NA_list[i]['Area_Name']
                            vote['cand '+str(j)] = cand_fname
                            vote[Party_Name] = count
                            Win_rec[Party_Name] =count
                          

                        else:
                            print("\n\n*************This Candidateis not Voted by Anyone!!!!!!**************\n")
                            print('Candidate Name: ',Candidate_Record['cand_fname'])
                            # print('Candidate CNIC: ',NA_list[i]['State_Name'])
                    # else:

                        # print('\2 The seat of Candidate NO: ' + str(j) + ' of NA_No: ' + str(NA_list[i]['State_Name']) + ' is Empty')

                print("\nTotal Votes: " , Total_Votes  ,"\n")
                # val = max(vote['Party_Name'],key=vote['Party_Name'].get)
                E_vote = db_States.find_one({'State_name' : NA_list[i]['State_Name']})
               
                electoral_party = max(Win_rec, key=Win_rec.get)
                # vote['electoral_'+electoral_party] = E_vote['Electoral_Votes']
                vote['electoral_Vote'] = E_vote['Electoral_Votes']
                # Win_rec.clear()
                # vote.update([max(Win_rec.items(), key = lambda x: x[1])])
                vote['Total Votes'] = Total_Votes
               
                Total_Votes = 0
                # print(vote)
                dispaly(vote)
                dictionary_copy = vote.copy()
                result.append(dictionary_copy)
                # result.append(vote)
                vote.clear()

            return result
            

        else:
            print("there is no NA in: " ,Election_Name)



       
    
    else:
        print("\n\nElection Are not Exist")

# def dispaly(vote):
#     for key, value in vote.items():
#         print(key, ' : ', value)


# voute_Count('NA-PAK-2020')

def Total_party_vote_Count(Admin_ID,election_id):
    party_list = []
    state_list = []
    party_votes = dict()
    Election_Name = db_election.find_one({'_id': ObjectId(election_id) ,'Admin_ID':ObjectId(Admin_ID)})  #insert AdminID Parameter here

    for i in db_party.find({'Admin_Id': ObjectId(Admin_ID) }): #insert AdminID Parameter here 
        party_list.append(i['Party_name'])
    
    for i in db_States.find({}): #insert AdminID Parameter here 
        state_list.append(i['State_name'])     

    for party in party_list:
        for state in state_list:

            count = db_ballot.count_documents({'Admin_ID': str(Admin_ID) ,'State_Name':state ,'Vote': party   })  ##,'Election_name': Election_Name['Election_Name']
            # print(party + ' '+ str(count))        
            party_votes[party] = count 
    Wining_Party =max(party_votes,key=party_votes.get)
    dispaly(party_votes)       
    return party_votes , Wining_Party
        # for party_count in db_ballot.find({'Admin_Id': ObjectId(Admin_ID) ,'Election_Name': E_Record['Election_Name'],'Vote': party   }): #insert AdminID Parameter here 
        # party_list.append(i['Party_name']) 

def dispaly(vote):
    for key, value in vote.items():
        print(key, ' : ', value)
# Total_party_vote_Count('602e0936b39fb0f1537ef3c3')


# vote_Count(ObjectId('6062be448e7cf82fec4b80fd'),str('602e0936b39fb0f1537ef3c3'))















def Vote_Count(state_name,Admin_ID): #Admin_ID,Election_Name
    party = []
    vote = dict()
    
    for i in db_party.find({}):
        party.append(i['Party_name'])
    print(party)

    for i in range(0,len(party)):
        count = db_ballot.count_documents({'Admin_ID': str(Admin_ID),'Vote': party[i] ,'State_Name':state_name}) #ObjectId(AdminID) , Election_Name,State_Name
        vote[party[i]]= count

    check = check_all_parties_vote_are_same_or_not(vote)
    if check != True:

        wining_party = Who_Win(vote)
        vote['Wining_Party'] = wining_party

        find_state_name = db_States.find_one({'State_name' : state_name})
        E_vote = find_state_name['Electoral_Votes']
        print(find_state_name)
        print(find_state_name['Electoral_Votes'])
        vote['E_' + str(wining_party)] = E_vote

        vote['State_Name'] = state_name
        # vote['Election_Name'] = Election_Name
        # vote['Admin_ID'] = ObjectId(Admin_ID)
        
        dispaly(vote)
        return vote

    else:
        print("*************All Parties Vote Are Same************")

def Who_Win(Vote):   
    max_key = max(Vote, key=Vote.get)
    print(max_key)
    return max_key


# vote = {"Gfg" : 5, "is" : 3, "Best" : 5}
def check_all_parties_vote_are_same_or_not(vote):
    test_val = list(vote.values())[0]
  
    res = True
    for ele in vote:
        if vote[ele] != test_val:
            res = False 
            break

    return res

# a = Vote_Count('North Carolina')
# print(a)