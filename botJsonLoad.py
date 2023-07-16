import json
import pymongo

with open('E:/PROGRAMMING/Major Project/backEnd/skill-Interview_Conversation.json') as f:
    data=json.load(f)


print(data)

con=pymongo.MongoClient('mongodb://localhost:27017/')
db=con['CandidateDetails']
col=db['bot']
result=col.insert_one(data)
