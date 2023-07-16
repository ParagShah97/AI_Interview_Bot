from flask import Flask,render_template,request

app=Flask('__name__')

@app.route('/demoPractice')
def demoPractice():
    return render_template('InterviewUI.html',text='this is my first work on demo2')

@app.route('/kuchKaro',methods=['GET','POST'])
def kuchKaro():
    if request.method=='POST':
        data=request.form
        print(data)
        return 'kaam ho gaya'
    



if __name__=='__main__':
    app.run(debug=True)