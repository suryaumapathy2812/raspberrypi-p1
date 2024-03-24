import wave

# Audio signal parameters
# - number of channels 
# - sample width
# - (framerate/sample_rate)  E.g. 44100 Hz,  This is the standard sampling rate for CD quality of the audio signal
# - number of frames
# - value of a frames

audio = wave.open("sample_recording2.wav", "rb")   # src, mode = read binary

print("Number of channels: ", audio.getnchannels())
print("Sample width: ", audio.getsampwidth())
print("Frame rate: ", audio.getframerate())
print("Number of frames: ", audio.getnframes())
print("Parameters: ", audio.getparams())

t_audio = audio.getnframes() / audio.getframerate()
print("Duration: ", t_audio)

frames = audio.readframes(-1)
# print(type(frames), type(frames[0]))
print(len(frames)/audio.getsampwidth())  #  460800 / 2 => 230400.0