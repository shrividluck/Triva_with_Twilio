package getTest;
import java.io.BufferedReader;

import org.json.simple.parser.*; 

import java.io.IOException;
import java.io.InputStreamReader;
import java.net.HttpURLConnection;
import java.net.MalformedURLException;
import java.net.ProtocolException;
import java.net.URL;
import java.util.Iterator;
import java.util.concurrent.TimeUnit;

import org.json.*;

import com.twilio.Twilio;
import com.twilio.rest.api.v2010.account.Message;
import com.twilio.type.PhoneNumber;

import org.json.simple.JSONArray; 
import org.json.simple.JSONObject; 
public class CallApi {
	// Find your Account Sid and Token at twilio.com/user/account
	public static final String ACCOUNT_SID = "ACCOUNT_SID"; //account sid from twilio
	public static final String AUTH_TOKEN = "Auth_token"; //from twilio
	
	public static String[] getQuestionAndAnswer() throws IOException, ParseException {
		//Establish connection with triviaDB API
				URL url = new URL("https://opentdb.com/api.php?amount=1&category=9&type=boolean");
				HttpURLConnection con = (HttpURLConnection) url.openConnection();
				con.setRequestMethod("GET");
				con.setRequestProperty("Content-Type", "application/json");
				String contentType = con.getHeaderField("Content-Type");
				// set timeout 
				con.setConnectTimeout(5000);
				con.setReadTimeout(5000);
				//read the response
				int status = con.getResponseCode();
				BufferedReader in = new BufferedReader(
						new InputStreamReader(con.getInputStream()));
				String inputLine;
				StringBuffer content = new StringBuffer();
				while ((inputLine = in.readLine()) != null) {
					content.append(inputLine);
				}
				String jsonResponse = content.toString();
				
				//System.out.println(content.toString());
				in.close();
				Object obj = new JSONParser().parse(jsonResponse); 
				// typecasting obj to JSONObject 
		        JSONObject jo = (JSONObject) obj; 
		        JSONArray ja = (JSONArray) jo.get("results"); 
		        //String lastName = (String) jo.get("lastName"); 
		        Iterator itr = ja.iterator(); 
		        JSONObject q = null;
		        while(itr.hasNext()) {
		        	 q = (JSONObject)itr.next();
		        }
		        String question = (String) q.get("question");
		        String answer = (String) q.get("correct_answer");
		        question.replaceAll("&quot;"," ");
		        System.out.println(question);
		        System.out.println(answer);
		        
		        return new String[]{question,answer};
	}

	public static void main(String[] args) throws IOException, ParseException, InterruptedException {
		String[] qAnda = getQuestionAndAnswer();
		
		sendSMS(qAnda[0]);
		TimeUnit.MINUTES.sleep(1);
		sendSMS(qAnda[1]);
	}

	public static void sendSMS(String qA) {
		Twilio.init(ACCOUNT_SID, AUTH_TOKEN);
		Message message = Message.creator(new PhoneNumber("+xxxxxxxxxx"),
				new PhoneNumber("+140xxxx9103"), 
				qA).create();

		System.out.println(message.getSid());
	}
}
