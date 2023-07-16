import json
import pymongo
import finalPreprocessing as fp
import fuzzyWuzzy as fw
import cosineSimilarity as cs
import math


con=pymongo.MongoClient('mongodb://localhost:27017')
db=con['CandidateDetails']
coll=db['AnsweredQuestions']
result=coll.find()

    #print('The actual collection from AnsweredQuestions Collection is *** ',result)
for i in result:
    cosineScore=-1
    cosineTemp=0
    fuzzScore=-1
    fuzzTemp=0
    #print('Collections one by one :*** ',i)
    print(type(i))
    answer1=i['answer-1']
    answer2=i['answer-2']
    answer3=i['answer-3']
    candidateAnswer=i['Candidate_Answer']
    answerList=[answer1,answer2,answer3]
    print(answer1,' ** ',answer2,' ** ',answer3,' ** ',candidateAnswer)
    j=0
    while j<3:
        cosineTemp=cs.cosineSimilarity(answerList[j],candidateAnswer)
        print('cosine score is ->',cosineTemp)
        if cosineTemp > cosineScore:
            cosineScore=cosineTemp
        fuzzTemp=fw.fuzzSimilarity(answerList[j],candidateAnswer)
        print('Fuzzy score is ->',fuzzTemp['fuzzyWRatio'])
        if int(fuzzTemp['fuzzyWRatio']) > fuzzScore:
            fuzzScore=int(fuzzTemp['fuzzyWRatio'])
        j+=1
    print('\n\nFinal score of cosineSimilarity is ->',fuzzScore)
    print('\n\nFinal score of fuzzyWuzzy is ->',cosineScore)
    finalScore=((cosineScore*0.75)+(fuzzScore*1.75))
    finalScore=finalScore/2
    print("********************* final Score is ***** ",finalScore)