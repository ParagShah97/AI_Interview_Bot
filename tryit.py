import json
import re


with open('E:/PROGRAMMING/Major Project/backEnd/skill-Interview_Conversation.json') as f:
    data=json.load(f)

var=data.get('intents')
#print(var)
#find='great, and fine too'
finalIntent=''
while True:
    find=input('You say : ')
    if find=='quit':
        break
    finalIntent=''
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
                #print('x ki value kya h bhai : -->',x)
                if(x in text):
                    found=True
                    finalIntent='#'+intent
                    print('loop me intent kya he : ',finalIntent)
                    break
        if found==True:
            break

    print('This is what i want to find *****',finalIntent)

    var2=data.get('dialog_nodes')
    #print('*********************\n\n\n',var2)
    for i in var2:
        if finalIntent==i.get('conditions'):
            print('** ** \n',i.get('conditions'))
            outputDict=i.get('output')
            genericList= outputDict.get('generic')
            for k in genericList:
                valuesList=k.get('values')
                for t in valuesList:
                    text=t.get('text')
                    print('\nRepy from bot *** *',text)