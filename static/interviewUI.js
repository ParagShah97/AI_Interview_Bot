function startTimer(duration, display) {
    var timer = duration, minutes, seconds;
    setInterval(function () {
        minutes = parseInt(timer / 60, 10);
        seconds = parseInt(timer % 60, 10);

        minutes = minutes < 10 ? "0" + minutes : minutes;
        seconds = seconds < 10 ? "0" + seconds : seconds;

        display.textContent = 'Timer : '+ minutes + ":" + seconds;

        if (--timer < 0) {
            //timer = duration;
            display.textContent = 'fuck off';
            
        }
    }, 1000);
}

window.onload = function () {
    var fiveMinutes = 60 * 1,
        display = document.querySelector('#timer');
    startTimer(fiveMinutes, display);
};

function wayToInterviewResponse()
{
    var questionID=document.getElementById('questionArea');
    var answerID=document.getElementById('answerArea');
    alert(questionID.value);
    alert(answerID.value);
    var xhttp= new XMLHttpRequest();
    xhttp.onreadystatechange=function(){
        if(this.readyState==4 && this.status==200)
        {
            varDataToPrint = this.responseText;
            alert("Response me aaya he :: "+varDataToPrint)
            dataReturnFromServer=JSON.parse(varDataToPrint);
            questionID.innerHTML=dataReturnFromServer['question'];
            answerID.value="Write your answer here // erase this line first. ";          
            //document.getElementById('answerArea').innerHTML=dataReturnFromServer['answer'];
            document.getElementById('answerArea').focus();
        }
        
    };
    questionID.value.trim();
    answerID.value.trim();
    xhttp.open('POST','http://localhost:5000/interviewResponse',false);
    xhttp.setRequestHeader('Content-type','application/x-www-form-urlencoded');
    //xhttp.send(JSON.stringify({'question':question,'answer':answer}));
    xhttp.send('answer='+answerID.value)
}