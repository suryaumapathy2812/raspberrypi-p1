import sys
import time
from openai import audio
import sounddevice as sd
import numpy as np
import webrtcvad
import threading

channels = [1]
mapping = [c - 1 for c in channels]

device_info = sd.query_devices(None, "input")
sample_rate = int(device_info["default_samplerate"])  # type: ignore

interval_size = 10000  # audio interval size in ms
downsample = 1

block_size = sample_rate * 30 / 1000

vad = webrtcvad.Vad()

print(
    "reading audio stream from default audio input device:\n"
    + str(sd.query_devices())
    + "\n"
)
print(f"audio input channels to process: {channels}")
print(f"sample_rate: {sample_rate}")
print(f"window size: {interval_size} ms")
print(f"datums per window: {block_size}")
print()

recordings = []
last_detection_time = 0
debounce_interval = 100  # seconds


def voice_activity_detection(audio_data):
    return vad.is_speech(audio_data, sample_rate)


def audio_processing():
    global recordings
    global last_detection_time
    while True:
        current_time = time.time()
        if current_time - last_detection_time < debounce_interval / 1000:
            time.sleep(0.1)
            continue

        if recordings:
            audio_data = recordings.pop(0)
            detection = voice_activity_detection(audio_data)
            print(f"{detection} \r", end="")
            if detection == 0:
                print(f"{detection} \r", end="")
                # print("calling chatgpt")
        time.sleep(0.1)  # Introduce a small delay to avoid busy waiting


def append_data(indata, frames, time, status):
    if status:
        print(f"underlying audio stack warning:{status}", file=sys.stderr)

    assert frames == block_size
    audio_data = indata[::downsample, mapping]
    audio_data = map(lambda x: (x + 1) / 2, audio_data)
    audio_data = np.fromiter(audio_data, np.float16)
    audio_data = audio_data.tobytes()
    recordings.append(audio_data)


if __name__ == "__main__":
    audio_thread = threading.Thread(target=audio_processing)
    audio_thread.start()

    with sd.InputStream(
        device=None,
        channels=max(channels),
        samplerate=sample_rate,
        blocksize=int(block_size),
        callback=append_data,
    ):
        while True:
            time.sleep(0.1)
