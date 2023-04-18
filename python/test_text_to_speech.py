from pydub import AudioSegment
from pydub.playback import play
from text_to_speech import TextToSpeech

tts = TextToSpeech()

phrase = "Hello world."
output_file = "test.mp3"

print(f"Saying {phrase}")

if tts.text_to_audio(phrase, output_file=output_file):
    audio = AudioSegment.from_mp3(output_file)
    play(audio)
    pass

