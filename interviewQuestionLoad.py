import json
import pymongo

#opening the file
with open("E:/PROGRAMMING/Major Project/backEnd/interviewQuestions.json",encoding="utf8") as s:
    data=json.load(s) #converting json to dictionary
    #print(type(data))

con=pymongo.MongoClient('mongodb://localhost:27017/')  
db=con['CandidateDetails'] #db getting database
coll=db['questions'] #coll getting access to table
finalResult=coll.insert_many(data) #inserting extracted dictonary to finalResult 
