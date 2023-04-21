from flask import Flask, request, send_from_directory, session, send_file
from flask_session import Session
from twilio.twiml.voice_response import Gather, VoiceResponse
from transcription import Transcriber
from bot import Bot
import os
import json

app = Flask(__name__)
app.secret_key = os.urandom(24)

# Configure session to use filesystem (instead of signed cookies)
app.config['SESSION_TYPE'] = 'filesystem'
app.config['SESSION_FILE_DIR'] = './sessions'
Session(app)

class Assistant:
    def __init__(self, call_sid):
        self.call_sid = call_sid
        self.transcriber = Transcriber()
        self.bot = Bot()

    def process_audio(self, conversation):
        if conversation:
            print("User:", conversation[-1]['content'])
            suggestion = self.bot.get_suggestion(conversation)
            print("Response:", suggestion)
            return suggestion

assistants = {}

@app.route("/start_call", methods=["POST"])
def start_call():
    call_sid = request.form.get("CallSid")
    session['call_sid'] = call_sid

    response = VoiceResponse()
    response.say("Hi, I'm Ruby the AI! If I get stuck, just say continue. How can I help you today?")
    gather = Gather(input='speech', action='/process_speech', speechTimeout="auto", speechModel="phone_call")
    response.append(gather)
    response.redirect('/process_speech')

    return str(response)

@app.route("/process_speech", methods=["POST"])
def process_speech():
    try:
        call_sid = session.get('call_sid')
        print("Call SID:", call_sid)

        # If assistant doesn't exist, create one
        if call_sid not in assistants:
            assistants[call_sid] = Assistant(call_sid)

        # Create a folder for the conversation
        if not os.path.exists(f"conversations/{call_sid}"):
            os.makedirs(f"conversations/{call_sid}")
      
        #if transcript file exists, read it
        limit = 8

        if os.path.exists(os.path.join(f"conversations/{call_sid}", "transcript.txt")):
            with open(os.path.join(f"conversations/{call_sid}", "transcript.txt"), "r") as f:
                lines = f.readlines()
                conversation = [json.loads(line) for line in lines[-limit:]]
        else:
            conversation = []

        user_text = request.form.get("SpeechResult")

        if not user_text:

            # If the user didn't say anything, log it in the transcript.txt file
            user_message = {"role": "user", "content": "No speech detected."}
            ai_message = {"role": "system", "content": "I'm sorry, I didn't quite catch that."}
            with open(os.path.join(f"conversations/{call_sid}", "transcript.txt"), "a") as f:
                f.write(json.dumps(user_message) + "\n")
                f.write(json.dumps(ai_message) + "\n")

            response = VoiceResponse()
            response.say("I'm sorry, I didn't quite catch that.")
            gather = Gather(input='speech', speechTimeout='auto', action='/process_speech', method='POST', speechModel="phone_call")
            response.append(gather)
            response.redirect(f'/process_speech')
            return str(response)
        
        # Add the user message to the conversation
        conversation.append({"role": "user", "content": user_text})

        # Process the audio and get the suggestion
        suggestion = assistants[call_sid].process_audio(conversation)

        # Summarize the AI response
        summary = assistants[call_sid].bot.summarize(suggestion)

        # Save the user and AI messages in the transcript.txt file
        user_message = {"role": "user", "content": user_text}
        ai_message = {"role": "system", "content": summary}
        with open(os.path.join(f"conversations/{call_sid}", "transcript.txt"), "a") as f:
            f.write(json.dumps(user_message) + "\n")
            f.write(json.dumps(ai_message) + "\n")

        response = VoiceResponse()
        response.say(suggestion)

        gather = Gather(input='speech', speechTimeout='auto', action='/process_speech', method='POST', speechModel="phone_call")
        response.append(gather)
        response.redirect(f'/process_speech')

        print("Response:", response)
        return str(response)
    
    except Exception as e:
        print("Error:", e)
        response = VoiceResponse()
        response.say("Sorry, there was an error processing your request. Please try again later.")
        return str(e)

if __name__ == "__main__":
    app.run(debug=True)
