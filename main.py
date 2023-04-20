from flask import Flask, request, send_from_directory, session, send_file
from flask_session import Session
from twilio.twiml.voice_response import Gather, VoiceResponse
from transcription import Transcriber
from troubleshooting import Troubleshooter
import os

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
        self.troubleshooter = Troubleshooter()

    def process_audio(self, transcribed_text):
        user_text = transcribed_text.strip()
        if user_text:
            print("User:", user_text)
            suggestion = self.troubleshooter.get_troubleshooting_suggestion(user_text)
            print("Troubleshooting Suggestion:", suggestion)
            return suggestion

assistants = {}

@app.route("/start_call", methods=["POST"])
def start_call():
    call_sid = request.form.get("CallSid")
    session['call_sid'] = call_sid

    response = VoiceResponse()
    response.say("Hi how can I help you?")
    gather = Gather(input='speech', action='/process_speech', speechTimeout="4", speechModel='default')
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
        if os.path.exists(os.path.join(f"conversations/{call_sid}", "transcript.txt")):
            with open(os.path.join(f"conversations/{call_sid}", "transcript.txt"), "r") as f:
                history = f.read()
        else:
            history = ""

        user_text = request.form.get("SpeechResult")

        context = history + " " + user_text

        # Process the audio and get the suggestion
        suggestion = assistants[call_sid].process_audio(context)

        # Save the user and AI messages in the transcript.txt file
        with open(os.path.join(f"conversations/{call_sid}", "transcript.txt"), "a") as f:
            f.write(f"\nUser: {user_text}\nAI: {suggestion}")

        response = VoiceResponse()
        response.say(suggestion)

        gather = Gather(input='speech', timeout=1.5, action='/process_speech', method='POST')
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
