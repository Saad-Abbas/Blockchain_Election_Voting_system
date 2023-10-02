import hashlib
import json
from time import time
from bson.objectid import ObjectId
from pymongo import MongoClient 
import jwt
import random
import Credentials

db = Credentials.db 

# Access collection of the database 
# ballot = db["Presidential_Ballot"]
# h = db["Hash"]
MB = db["Presidential_Mined_Block"]
PB = db["Presidential_Ballot"]
PWT = db["Presidential_Ballot_Web_Token"]
PM = db["Presidential_Mined_Block"]


# Genesis_nounce = 0
# Remaining_nouce = Genesis_nounce

def proof_of_work():
    proof = random.randint(139587,99865127)
    return proof

class genisis:
    def __init__(self,nonce,Election_name,previous_hash="",Admin_ID=""):
        self.Nonce = nonce
        self.Admin_ID = Admin_ID
        self.Election_Name = Election_name
        self.Time_Stamp = time()
        self.Previous_Hash = previous_hash
        self.Block_Hash = self.Calculate_hash()

    def Calculate_hash(self):
        block_string = json.dumps({
            "Nonce": self.Nonce,
            "Admin_ID": self.Admin_ID,   #str(self.Admin_ID)
            "Election_name": self.Election_Name,
            "Time_Stamp":self.Time_Stamp,
            "Previous_Hash":self.Previous_Hash


        },sort_keys=True)

        block_hash = hashlib.sha256(block_string.encode()).hexdigest()
        return block_hash

    def Minning_Block(self,difficulty):
        while(self.Block_Hash[:difficulty] != str('').zfill(difficulty)):                                     #Mining Block
            self.Nonce += 1
            self.Block_Hash = self.Calculate_hash()

        Insert_to_Mined_Block = {

            "Blocked_Mined": self.Block_Hash,
            
        }

        PM.insert_one(Insert_to_Mined_Block)        
    

    def __str__(self):

        Insert_rec_to_Ballot = {
            
            "Admin_ID": self.Admin_ID,   #str(self.Admin_ID)
            "Nonce": self.Nonce,
            "Election_name": self.Election_Name,
            "Time_Stamp":self.Time_Stamp,
            "Previous_Hash":self.Previous_Hash,
            "Block_Hash": self.Block_Hash
            
        }

        web_token = jwt.encode(Insert_rec_to_Ballot, "62908", algorithm="HS256")
        
        Insert_web_Token = {
            'Web_Token' : web_token
        }

        PB.insert(Insert_rec_to_Ballot)
        PWT.insert(Insert_web_Token)
        string = "Previous_Hash: " + str(self.Previous_Hash) + "\n"
        string = string + "Block_hash: " + str(self.Block_Hash) + "\n\n"
        string = string + "Web_Token: " + str(web_token) + "\n"
        

        return string

class block():

    def __init__(self,nonce,Election_name,State_name,Voter_Cnic,Candidate_Cnic,vote,Admin_ID="",previous_hash=""):
        self.Admin_ID = Admin_ID
        self.Nonce = nonce
        self.Time_Stamp = time()
        self.Election_Name = Election_name
        self.State_Name = State_name
        self.Voter_CNIC = Voter_Cnic
        self.Candidate_CNIC = Candidate_Cnic
        self.Vote = vote
        self.Previous_Hash = previous_hash
        self.Block_Hash = self.Calculate_hash()

    def Calculate_hash(self):
        block_string = json.dumps({
            "Nonce": self.Nonce,
            "Admin_ID": self.Admin_ID,   #str(self.Admin_ID)
            "Election_name": self.Election_Name,
            "Time_Stamp":self.Time_Stamp,
            "State_Name":self.State_Name,
            "Voter_CNIC": self.Voter_CNIC,
            "Candidate_CNIC": self.Candidate_CNIC,
            "Vote": self.Vote,
            "Previous_Hash":self.Previous_Hash

        },sort_keys=True)

        block_hash = hashlib.sha256(block_string.encode()).hexdigest()
        
        return block_hash

    def Minning_Block(self,difficulty):
        while(self.Block_Hash[:difficulty] != str('').zfill(difficulty)):                                     #Mining Block
            self.Nonce += 1
            self.Block_Hash = self.Calculate_hash()

        Insert_to_Mined_Block = {

            "Blocked_Mined": self.Block_Hash,
            
        }

        PM.insert(Insert_to_Mined_Block)

    def __str__(self):

        Insert_rec_to_Ballot = {
            "Admin_ID":  self.Admin_ID,    #ObjectId(self.Admin_ID) 
            "Nonce": self.Nonce,
            "Election_name": self.Election_Name,
            "Time_Stamp":self.Time_Stamp,
            "State_Name":self.State_Name,
            "Voter_CNIC": self.Voter_CNIC,
            "Candidate_CNIC": self.Candidate_CNIC,
            "Vote": self.Vote,
            "Previous_Hash":self.Previous_Hash,
            "Block_Hash": self.Block_Hash
            
        }
        
        web_token = jwt.encode(Insert_rec_to_Ballot, "62908", algorithm="HS256")
        
        Insert_web_Token = {
            'Web_Token' : web_token
        }

        PB.insert(Insert_rec_to_Ballot)
        PWT.insert(Insert_web_Token)

        string = "Previous_Hash: " + str(self.Previous_Hash) + "\n"
        string = string + "Block_hash: " + str(self.Block_Hash) + "\n\n" 
        string = string + "Web_Token: " + str(web_token) + "\n"  
        

        return string 


class Blockchain():
    def __init__(self):
        self.difficulty = 3
        self.chain=[]
        self.check = []
        self.Last_Document = {}

        for i in PB.find({}):
            self.check.append(i)

        if self.check == []:
            self.chain.append(self.Generate_genisis_Block())
        else:
            for i in range(0,len(self.check)):
                self.chain.append(self.check[i])


    def Generate_genisis_Block(self):
        genisis_block = genisis(proof_of_work(),"PRESIDENTIAL-2020","GENISIS BLOCK")
        genisis_block.Minning_Block(self.difficulty)
        return genisis_block

    def Last_block(self):
       return self.chain[-1]
    
    def Add_new_block(self,new_block):
    
        self.Last_Document = self.Last_block()

        if self.check == []:
            self.New_Document = self.Last_Document.Block_Hash
        else:
            self.New_Document = self.Last_Document['Block_Hash']

        new_block.Previous_Hash = self.New_Document
        new_block.Minning_Block(self.difficulty)
        self.chain.append(new_block)

        
def creat_chain(block_chain1):
    for i in block_chain1.chain:
        print(i)


# block_chain = Blockchain()
# block_chain.Add_new_block(block(proof_of_work(),"Pak-2020","COlombia","42201-1111111-5","42201-2222222-5","Green"))
# creat_chain(block_chain)    
