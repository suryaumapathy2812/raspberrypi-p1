import wave
import matplotlib.pyplot as plt
import numpy as np


audio = wave.open("sample_recording2.wav", "rb")   # src, mode = read binary

sample_freq = audio.getframerate()
n_sample = audio.getnframes()
signal_wave = audio.readframes(-1)

audio.close()

t_audio = n_sample / sample_freq
print("Duration: ", t_audio)

signal_array = np.frombuffer(signal_wave, dtype=np.int16)
times= np.linspace(0, t_audio, num=n_sample)

plt.figure(figsize=(10,5))
plt.plot(times, signal_array)
plt.title("Audio Signal")
plt.xlabel("Time (s)")
plt.ylabel("Amplitude")
plt.xlim(0, t_audio)
plt.show()