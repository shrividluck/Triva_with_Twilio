from flask import Flask, request, session
from twilio.twiml.messaging_response import MessagingResponse
import requests
import json
import time
from twilio.rest import Client

# The session object makes use of a secret key.
SECRET_KEY = 'a secret key'
app = Flask(__name__)
app.config.from_object(__name__)

# Try adding your own number to this list!
callers = {
    "+xxxxxxxxxx": "Shri"
}



url = "https://opentdb.com/api.php?amount=1&category=9&type=boolean"
my_num = "+140xxxxxxxxx"

def html_decode(s):
    """
    Returns the ASCII decoded version of the given HTML string. This does
    NOT remove normal HTML tags like <p>.
    """
    htmlCodes = (
            ("'", '&#39;'),
            ('"', '&quot;'),
            ('>', '&gt;'),
            ('<', '&lt;'),
            ('&', '&amp;')
        )
    for code in htmlCodes:
        s = s.replace(code[1], code[0])
    return s


def get_q_and_answer():
    response = requests.get(url,None)
    stt = response.content.decode('utf-8')
    jtt = json.loads(stt)
    q = jtt['results'][0]['question']
    #ans = [jtt['results'][0]['correct_answer']
    #ans = [[jtt['results'][0]['correct_answer']], jtt['results'][0]['wrong_answers']]
    #ans = [ tt for pp in ans for tt in pp]
    #ans = my_shuffle(ans)
    q = html_decode(q)
    return [q,jtt['results'][0]['correct_answer']]


def pre_process_body(body):
    if len(body) >= 1:
        body = body[0].lower()
        if body == 'y':
            body = 't'
        if body == 'n':
            body = 'f'
    return body

@app.route("/sms", methods=['GET', 'POST'])
def hello():
    """Respond with the number of text messages sent between two parties."""
    # Increment the counter
    counter = session.get('counter', 0)
    correct_ans = session.get('correct', 0)
    
    body = request.values.get('Body', None)
    message =""
    
    print("before: "+body)
    body = pre_process_body(body)
    print("after: "+body)
    
    from_number = request.values.get('From')
    if from_number in callers:
        name = callers[from_number]
    else:
        name = "Friend"
            
    
    if 'question' in session:
        print("Coming to the question part")
        answer = session.get('question')
        session.pop('question')
        print("correct answer from session is "+answer+" from the body "+body)
        if answer[0].lower() == body: 
            correct_ans += 1
            # Build our reply
            message += "That is correct !!! Well Done !!!\n"           
        else:
            message += "Incorrect, sorry :-(\n"
        message += "Do you want another question ? (Y/N)"
        session['correct'] = correct_ans    
    elif body == 't' or body == 'q':
        print("Coming to body == 't'")
        qAnda = get_q_and_answer()
        counter += 1
        message += 'Next question is -' + qAnda[0]
        # Save the new counter value in the session
        session['question'] = qAnda[1]
        session['counter'] = counter    
    else :
        message += '{} has answered correctly {} out of {} times.\n'.format(name, correct_ans, counter)
        message += 'It was fun playing ! See you next time !'
        session.pop('counter')
        session.pop('correct')
        
    

    
    
    
    # Put it in a TwiML response
    resp = MessagingResponse()
    resp.message(message)


    return str(resp)


if __name__ == "__main__":
     app.run(debug=True, host='0.0.0.0', port=4567)
