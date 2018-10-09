# Trivia_with_Twilio
This Repo consists of two Twilio Apps (one in Java and one in python) to send trivia questions (from opentriviadb API) to users via the Twilio API  . 

## Java version:
It sends a Trivia Q to the registered Twilio phone number via the Twilio API 
      * Sends the answer after a minute
      * Push model just to use the Twilio send SMS feature


## Python version :
Python version of Trivia App using Twilio : 
     * The code is used to create a flask server, that is hooked to the Twilio WebHook via ngrok
     * Whenever the registered phone sends a message with  'q/Q', a question is sent to the user . 
     * User can sms the answer and the app will reply whether or not it was correct !
     * User can request for another question by replying 'y/Y' 
     * User can reply with 'N' to stop playing 
     * The app gives the number of right answers in that session. 
     
