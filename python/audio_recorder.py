import pyaudio
import numpy as np
import soundfile as sf
import time
import datetime

class AudioRecorder:
    def __init__(self):
        self.FORMAT = pyaudio.paInt16
        self.CHANNELS = 1
        self.RATE = 16000
        self.CHUNK = 1024

        self.audio = pyaudio.PyAudio()
        self.stream = self.audio.open(
            format=self.FORMAT,
            channels=self.CHANNELS,
            rate=self.RATE,
            input=True,
            frames_per_buffer=self.CHUNK,
            stream_callback=self.callback
        )

        self.audio_buffer = []

    def callback(self, in_data, frame_count, time_info, status):
        audio_data = np.frombuffer(in_data, dtype=np.int16)
        self.audio_buffer.extend(audio_data)
        return (in_data, pyaudio.paContinue)

    def save_audio(self, file_name):
        sf.write(file_name, np.array(self.audio_buffer), self.RATE)

    def record_audio(self, duration=None):
        start_time = time.time()
        file_name = f"audio/audio_{start_time}_{datetime.datetime.now().strftime('%Y-%m-%d')}.wav"
        
        try:
            self.stream.start_stream()
            print("Recording... Press Ctrl+C to stop.")
            while self.stream.is_active():
                time.sleep(0.1)
                if duration and (time.time() - start_time) >= duration:
                    break
        except KeyboardInterrupt:
            print("Stopping recording...")

        self.stream.stop_stream()
        self.stream.close()
        self.audio.terminate()

        self.save_audio(file_name)
        self.audio_buffer.clear()

        return file_name

