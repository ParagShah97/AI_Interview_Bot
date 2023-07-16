import json


with open('E:/PROGRAMMING/Major Project/backEnd/skill-Interview_Conversation.json') as f:
    data=json.load(f)

var=data.get('intents')
#print(var)
#find='great, and fine too'

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
            #print('text here--> ',text)
            newTexts=find.split(' ')
            #print('New Texts :--->',newTexts)
            for x in newTexts:
                #print('x ki value kya h bhai : -->',x)
                if(x in text):
                    found=True
                    finalIntent='#'+intent
                    #print('loop me intent kya he : ',finalIntent)
                    break
        if found==True:
            break

    print('This is what i want to find *****',finalIntent)
