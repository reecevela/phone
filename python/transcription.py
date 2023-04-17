import openai
import os
openai.api_key = os.getenv("OPENAI_API_KEY")

def transcribe_audio(file_path):
    with open(file_path, "rb") as audio_file:
        transcript = openai.Audio.transcribe("whisper-1", audio_file)
    return transcript["text"]
