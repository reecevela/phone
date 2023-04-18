from transcription import Transcriber
from troubleshooting import Troubleshooter
from audio_recorder import AudioRecorder
from text_to_speech import TextToSpeech
from pydub import AudioSegment
from pydub.playback import play

class Assistant:
    def __init__(self):
        self.transcriber = Transcriber()
        self.troubleshooter = Troubleshooter()
        self.text_to_speech = TextToSpeech()

    def process_audio(self, file_path):
        transcribed_text = self.transcriber.transcribe_audio(file_path)

        user_text = transcribed_text.strip()
        if user_text:
            print("User:", user_text)
            suggestion = self.troubleshooter.get_troubleshooting_suggestion(user_text)
            print("Troubleshooting Suggestion:", suggestion)
            self.speak_suggestion(suggestion)
    
    def speak_suggestion(self, text):
        output_file = "current.mp3"
        if self.text_to_speech.text_to_audio(text, output_file):
            # Play the audio
            audio = AudioSegment.from_mp3(output_file)
            play(audio)
            pass

if __name__ == "__main__":
    assistant = Assistant()
    audio_recorder = AudioRecorder()
    audio_file = audio_recorder.record_audio() #record_audio returns a file path, will work on a better implementation soon
    if audio_file:
        assistant.process_audio(audio_file)
