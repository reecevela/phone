from twilio.twiml.voice_response import VoiceResponse
from flask import Flask, request
import os

class Caller:
    def __init__(self):
        self.app = Flask(__name__)

    def play_audio(self):
        response = VoiceResponse()
        response.play('test.mp3')
        return str(response)

    def run(self):
        self.app.run(host='0.0.0.0', port=os.environ.get('PORT', 8080))

if __name__ == "__main__":
    caller = Caller()
    caller.app.add_url_rule("/", "play_audio", caller.play_audio, methods=['POST'])
    caller.run()
