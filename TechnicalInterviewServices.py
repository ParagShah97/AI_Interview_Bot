from flask import Flask,redirect,request,url_for,render_template,session,jsonify
import pymongo
from flask_cors import CORS
from flask_cors import cross_origin
import re
import smtplib
import config
import json


import finalPreprocessing as fp
import fuzzyBasedDistance as fbd
import fuzzyWuzzy as fw
import cosineSimilarity as cs
import math


app=Flask('__name__')
app.secret_key="MyMajorProject"


@app.route('/demo',methods=['POST','GET'])
@cross_origin()
def demo():
    if request.method=='POST':
        value=request.form
        find=value['text']      # data from client stored in find variable
        con=pymongo.MongoClient('mongodb://localhost:27017/')
        db=con['CandidateDetails']
        coll=db['bot']
        result=coll.find()
        list1=[]
        for obj in result:
            list1.append(obj)
        data=list1[0]
        var=data.get('intents')
        finalIntent=''
        # loop for searching intent
        for i in var:
            #print('dictionary is --->',i.get('examples'))
            intent=i.get('intent')
            example=i.get('examples')
            found=False
            for j in example:
                #print('inner dictionary -***->',j.get('text'))
                text=j.get('text')
                print('text here--> ',text)
                newTexts=re.split(',| ',find)
                print('New Texts :--->',newTexts)
                for x in newTexts:
                    if x==' ':
                        continue
                    print('x ki value kya h bhai : -->',x)
                    if(x in text):
                        print('iss k karan match hua he : ',x,text)
                        found=True
                        finalIntent='#'+intent
                        #print('loop me intent kya he : ',finalIntent)
                        break
            if found==True:
                break
        print('This is what i want to find *****',finalIntent)
        var2=data.get('dialog_nodes')
        textToReply=''
        for i in var2:
            if finalIntent==i.get('conditions'):
                print('** ** \n',i.get('conditions'))
                outputDict=i.get('output')
                genericList= outputDict.get('generic')
                for k in genericList:
                    valuesList=k.get('values')
                    for t in valuesList:
                        textToReply=t.get('text')
                        print('\nRepy from bot *** *',textToReply)
        return textToReply
                        

@app.route('/interviewUI')
def interviewUI():
    return render_template("InterviewUI.html",text1="This is your qustion area and on top-right there is a timer according to which you have to attempt the test, \nIn right section there are two clickables next and submit test.",text2="This is your answer area, write your answer in theory format don't write code.\nTo score better the answer should be to the point.")

@app.route('/interviewResponse',methods=['POST','GET'])
def interviewResponse():
    if request.method=='POST':
        data=request.form 
        mutableDict=data.to_dict()       
        print(mutableDict) # iss se aane wali dict print ho jayegi       
        '''for i in mutableDict:
            print("*** key , value is 8**** ",i)
            print(i['answer'])'''
        
        answerFromCandidate=data['answer']
        
        if "question_id" in session:
            
            print('\n if session present *** ',session['question_id'])
            con=pymongo.MongoClient('mongodb://localhost:27017/')
            db=con['CandidateDetails']
            coll=db['questions']
            coll2=db['AnsweredQuestions']
            print("*** 1 ***")
            result_Session=coll.find_one({'id':session['question_id']})
            print("*** 2 ***")
            result_Session.update({'Candidate_Answer':answerFromCandidate})
            print("*** 3 ***")
            result_of_insert=coll2.insert_one(result_Session)
            print("*** 4 ***")
            session['question_id']=session['question_id']+1
            print("*** 5 ***")
            print('\n if session present *** ',session['question_id'])
            if session['question_id'] > 4:
                print('Done with Questions')
                dd={'question':"We done with your interview, you can submit your test now.All The best!",'answer':""}
                dd1=json.dumps(dd)
                return dd1

            result_next_question=coll.find_one({'id':session['question_id']})
            dd={'question':result_next_question['question'],'answer':"Answer Here!!"}
            dd1=json.dumps(dd)
            print('\njson returning is(if wala) **** ',dd1)
            return dd1       

        else:            
            session['question_id']=1
            print('\nif session does not exist *** ',session['question_id'])
            con=pymongo.MongoClient('mongodb://localhost:27017/')
            db=con['CandidateDetails']
            coll=db['questions']
            result_noSession=coll.find_one({'id':session['question_id']})
            con.close()
            dd={'question':result_noSession['question'],'answer':"Answer Here!!"}
            dd1=json.dumps(dd)
            print('\njson returning is(else wala) **** ',dd1)
            return dd1

        
        return "Some error occure!!"
        

@app.route('/interviewAnalysis')
def interviewAnalysis():
    con=pymongo.MongoClient('mongodb://localhost:27017')
    db=con['CandidateDetails']
    coll=db['AnsweredQuestions']
    result=coll.find()
    finalScoreList=[]
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
        #print(answer1,' ** ',answer2,' ** ',answer3,' ** ',candidateAnswer)
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
        print('\n\nFinal score of fuzzyWuzzy is ->',fuzzScore)
        print('\n\nFinal score of cosineSimilarity is ->',cosineScore)
        finalScore=((cosineScore*0.75)+(fuzzScore*1.75))
        finalScore=finalScore/2
        print("********************* final Score is ***** ",finalScore)
        finalScoreList.append(finalScore)
    return render_template("interviewAnalysis.html",returnList=finalScoreList)

@app.route('/',methods=['GET'])
def index():
    print("Kuch hua")
    return render_template("index.html")

@app.route('/register',methods=['GET'])
def register():    
    return render_template("CandidateForm.html")

@app.route('/interview',methods=['GET'])
def interview():    
    return "Interview Started"

@app.route('/feedback',methods=['GET'])
def feedback():    
    return render_template("FeedbackForm.html")


# service to server registerId page
@app.route("/registerIdVerify",methods=['GET'])
def registerIdVerify():
    return render_template('RegisterIdVerify.html')
    
# service to serve ChatUI html page
@app.route("/hrInteractionPage",methods=['GET','POST'])
def hrInteractionPage():
    if request.method=='POST':
        form_data=request.form
        uId=int(form_data['uniqueCode'])
        print('ye wo wali id he jis k piche bohot magaj mari hui->',uId)
        con=pymongo.MongoClient('mongodb://localhost:27017/')
        db=con['CandidateDetails']
        col=db['Candidates']
        result=col.find_one({'id':uId})
        print(result)
    return render_template("chatBotUI.html",userFirstName=result['first_Name'],userLastName=result['last_Name'],enroll=result['enroll'],dob=result['dob'],clgName=result['institute'],emailId=result['email'])

    
## Registration page data reach here as response.
@app.route('/candidate',methods=['POST','GET'])
def candidate():
    if request.method=='POST':
        form_data=request.form
        form_d=form_data.to_dict()
        
        '''print(form_data)
        print("\n ",type(form_data))
        print("\n ",type(form_d))
        print(form_d)'''
        ## Mongodb connection start...
        con=pymongo.MongoClient("mongodb://localhost:27017/")  #127.0.0.1
        db=con['CandidateDetails']
        collection=db['Candidates']
        form_d.update({'id':db.Candidates.find().count()+1})
        result=collection.insert_one(form_d)
        ## Mongodb connection end... data-stored.

        ## session work here starts
        localId=str(form_d['id'])
        #session["candidate_id"]=form_d['id']
        #print('ye candidate() function me id session wali print karega->',form_d['id'])


        ## session work here ends

        ## Mail id retrival...
        mailToSend=str(form_data['email'])
        print('hhhe',mailToSend,'hihi')
        ## Mail sending work start...
        subject="Confirmation Mail for A.I based Interview."
        msg="This is a confirmation mail, to continue with the interview process,\nwe request you to click the link given below\n\nhttp://localhost:5000/registerIdVerify\n\nYour personal test id is: "+localId+"\nIt is a python generated automated mail. \nPlease don't reply. "
        try:
            server=smtplib.SMTP('smtp.gmail.com:587')
        
            server.ehlo()
        
            server.starttls()
        
            server.login(config.EMAIL_ADDRESS,config.PASSWORD)
        
            message='Subject: {}\n\n{}'.format(subject,msg)
            
            server.sendmail(config.EMAIL_ADDRESS,mailToSend,message)
            server.quit()
        
            print('Success! email send.')
        except:
            print('unable to send mail.')
        ## Mail sending work ends...

        #return render_template("chatBotUI.html",userFirstName=form_data['first_Name'],userLastName=form_data['last_Name'],enroll='0827CS161153',dob=form_data['dob'],clgName=form_data['institute'],emailId=form_data['email'])
        return render_template("emailValidationPage.html")
    return "hello"
        
    

if __name__=='__main__':
    app.run(debug=True)