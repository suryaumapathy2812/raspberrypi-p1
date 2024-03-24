import pyaudio
import wave

FRAMES_PER_BUFFER = 3200
FORMAT = pyaudio.paInt16
CHANNELS = 1
RATE = 16000

p = pyaudio.PyAudio()

default_input = p.get_default_input_device_info()
print(f"Default input device: {default_input['name']}")


stream = p.open(
    format=FORMAT,
    frames_per_buffer=FRAMES_PER_BUFFER,
    channels=CHANNELS,
    rate=RATE,
    input=True,
)


print("Recording started")

seconds = 5
frames = []

for i in range(0, int(RATE / FRAMES_PER_BUFFER * seconds)):   # Record for 5 seconds
    data = stream.read(FRAMES_PER_BUFFER)
    frames.append(data)
    
stream.stop_stream()
stream.close()
p.terminate()


new_recording = wave.open("mic_check.wav", "wb")
new_recording.setnchannels(CHANNELS)
new_recording.setsampwidth(p.get_sample_size(FORMAT))
new_recording.setframerate(RATE)
new_recording.writeframes(b"".join(frames))
new_recording.close()