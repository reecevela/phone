from transcription import Transcriber
from troubleshooting import Troubleshooter
from audio_recorder import AudioRecorder

class Assistant:
    def __init__(self):
        self.transcriber = Transcriber()
        self.troubleshooter = Troubleshooter()

    def process_audio(self, file_path):
        transcribed_text = self.transcriber.transcribe_audio(file_path)

        user_text = transcribed_text.strip()
        if user_text:
            print("User:", user_text)
            suggestion = self.troubleshooter.get_troubleshooting_suggestion(user_text)
            print("Troubleshooting Suggestion:", suggestion)

if __name__ == "__main__":
    assistant = Assistant()
    audio_recorder = AudioRecorder()
    audio_file = audio_recorder.record_audio() #record_audio returns a file path, will work on a better implementation soon
    if audio_file:
        assistant.process_audio(audio_file)
