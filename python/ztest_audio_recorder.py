from audio_recorder import AudioRecorder

audio_recorder = AudioRecorder()
file_path = audio_recorder.record_audio(duration=10)  # Record for 10 seconds
print(f"Audio saved to {file_path}")
