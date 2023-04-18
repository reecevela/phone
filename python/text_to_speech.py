import requests
import os

class TextToSpeech:
    def __init__(self):
        self.api_key = os.getenv("XI_API_KEY")
        self.base_url = "https://api.elevenlabs.io/v1/text-to-speech"
        self.voice_id = "ErXwobaYiN019PkySvjV"

    def text_to_audio(self, text, output_file):
        url = f"{self.base_url}/{self.voice_id}"
        headers = {"xi-api-key": self.api_key}
        data = {"text": text}
        response = requests.post(url, json=data, headers=headers)

        if response.status_code == 200:
            with open(output_file, "wb") as audio_file:
                audio_file.write(response.content)
            return True
        else:
            print("Error generating audio:", response.text)
            return False
