import pyaudio
import numpy as np 
import sys
import webrtcvad

# Parameters
channels = 1
mapping = [c - 1 for c in [channels]]
sample_rate = 16000
interval_size = 10000  # 10 seconds interval for silence
downsample = 1

block_size = sample_rate * 30 / 1000

# Create PyAudio instance
p = pyaudio.PyAudio()

vad = webrtcvad.Vad()

def voice_activity_detection(audio_data):
    return vad.is_speech(audio_data, sample_rate)


# Callback function for audio stream
def audio_callback(in_data, frames, time, status):
    print(f"underlying audio stack warning:{status}", file=sys.stderr)
    if status:
        print(f"underlying audio stack warning:{status}", file=sys.stderr)
    
    assert frames == block_size
    audio_data = in_data[::downsample, mapping]  # possibly downsample, in a naive way
    audio_data = map(
        lambda x: (x + 1) / 2, audio_data
    )  # normalize from [-1,+1] to [0,1], you might not need it with different microphones/drivers
    audio_data = np.fromiter(audio_data, np.float16) 
    
    audio_data = audio_data.tobytes()
    detection = voice_activity_detection(audio_data)
    
    # Process the audio data here
    return (in_data, pyaudio.paContinue)

# Create PyAudio stream
stream = p.open(format=pyaudio.paInt16,
                channels=channels,
                rate=sample_rate,
                input=True,
                frames_per_buffer=int(sample_rate * interval_size / 1000),
                stream_callback=audio_callback)

# Start recording
stream.start_stream()

print(stream.is_active())

# Wait for the stream to finish (in your case, it will run indefinitely)
while stream.is_active():
    pass

# Stop and close the stream
stream.stop_stream()

print(stream.is_active())
stream.close()

# Terminate PyAudio
p.terminate()
