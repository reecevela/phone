from transcription import Transcriber

tr = Transcriber()

test_audio_file = "./audio/testaudio.wav"
transcribed_text = tr.transcribe_audio(test_audio_file)

print("Transcribed text:")
print(transcribed_text)
