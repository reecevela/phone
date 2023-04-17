import time
import transcription
import troubleshooting
from audio_recorder import AudioRecorder

# Transcribe audio to text
def process_audio(file_path):
    transcribed_text = transcription.transcribe_audio(file_path)
    print("Transcribed Text:", transcribed_text)

    # Detect pauses and get troubleshooting suggestions
    pause_duration = 1.5
    transcription_start_time = time.time()
    last_word_timestamp = None
    words = []

    for word in transcribed_text.split():
        current_time = time.time()
        if last_word_timestamp and current_time - last_word_timestamp > pause_duration:
            print("User:", ' '.join(words))
            suggestion = troubleshooting.get_troubleshooting_suggestion(' '.join(words))
            print("Troubleshooting Suggestion:", suggestion)
            words = []
        words.append(word)
        last_word_timestamp = current_time

    # Final suggestion after the last pause or end of the transcription
    if words:
        print("User:", ' '.join(words))
        suggestion = troubleshooting.get_troubleshooting_suggestion(' '.join(words))
        print("Troubleshooting Suggestion:", suggestion)

if __name__ == "__main__":
    audio_recorder = AudioRecorder()
    audio_recorder.record_audio()
    audio_file = audio_recorder.get_saved_audio_path()
    if audio_file:
        process_audio(audio_file)
