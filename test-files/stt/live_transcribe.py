import os
import logging
from random import sample
from dotenv import load_dotenv
import wave
import pyaudio
from faster_whisper import WhisperModel
from vad import EnergyVAD
import numpy as np
import numpy as np  # required to avoid crashing in assigning the callback input which is a numpy object
import webrtcvad


load_dotenv(dotenv_path="./../.env")

logging.basicConfig()
logging.getLogger("faster_whisper").setLevel(logging.DEBUG)

model_size = os.getenv("WHISPER_MODEL") or "large-v3"
model_device = os.getenv("WHISPER_DEVICE") or "cpu"

FRAMES_PER_BUFFER = 480
FORMAT = pyaudio.paInt16
CHANNELS = 1
RATE = 16000
CHUNK = 1024
INTERVAL_SIZE = 10000

# vad = EnergyVAD(
#     sample_rate=RATE,
#     energy_threshold=0.05,  # threshold for energy above which frames are considered as speech
#     frame_length=0.02,  # frame length in seconds # type: ignore
#     frame_shift=0.01,  # frame shift in seconds #type: ignore
#     pre_emphasis=0.95,  # pre-emphasis factor
# )

vad = webrtcvad.Vad()
vad.set_mode(3)

# def print_input_devices():
#     p = pyaudio.PyAudio()
#     num_devices = p.get_device_count()
#     logging.info("Available audio input devices:")
#     for i in range(num_devices):
#         device_info = p.get_device_info_by_index(i)
#         device_name = device_info['name']
#         logging.info(f"Device {i}: {device_name}")


def check_vad(data):
    silence_threshold = 0.05
    silent_count = 0
    rms = np.sqrt(np.mean(np.square(data)))
    logging.debug("RMS: %f", rms)
    if rms < silence_threshold:
        silent_count += 1
    else:
        silent_count = 0

    return silent_count

def check_vad3(data):
    
    sample_rate = RATE
    # frame_duration = 30  # ms

    is_speech = vad.is_speech(data, sample_rate)
    return is_speech
    

def record_audio():
    p = pyaudio.PyAudio()

    # Get device info
    device_info = p.get_device_info_by_index(2)
    device_name = device_info["name"]
    print(f"Recording from: {device_name}")

    stream = p.open(
        format=FORMAT,
        frames_per_buffer=int(RATE * INTERVAL_SIZE / 1000),
        channels=CHANNELS,
        rate=RATE,
        input=True,
        # stream_callback=
    )

    logging.info("Recording started")
    frames = []

    # seconds = 5
    # for i in range(0, int(RATE / FRAMES_PER_BUFFER * seconds)):  # Record for 5 seconds
    while True:
        logging.info("Recording started")
        data = stream.read(FRAMES_PER_BUFFER)

        # try:
        #     data = stream.read(FRAMES_PER_BUFFER)
        # except OSError as e:
        #     if e.errno == -9981:
        #         logging.warning(
        #             "Input overflowed. Adjusting buffer size or processing speed may help."
        #         )
        #         continue  # Continue recording
        #     else:
        #         raise e  # Reraise other OSError

        frames.append(data)
        i = len(frames)
        logging.debug("Recording frame %d", i)

        
        

        # Convert audio data to numpy array for processing
        audio_data = np.fromiter(data, np.float16) 
        audio_data = audio_data.tobytes()

        silent_count = check_vad3(audio_data)
        # silent_count = check_vad2(audio_data)
        logging.debug("Silent count: ", silent_count)

        # If silent for more than a certain duration, stop recording
        if silent_count > RATE / CHUNK * 2:  # TODO Adjust the duration as needed
            break

    stream.stop_stream()
    stream.close()
    p.terminate()
    print("Recording stopped")

    new_recording = wave.open("stt/live_transcribe_audio.wav", "wb")
    new_recording.setnchannels(CHANNELS)
    new_recording.setsampwidth(p.get_sample_size(FORMAT))
    new_recording.setframerate(RATE)
    new_recording.writeframes(b"".join(frames))
    new_recording.close()

    return b"".join(frames)


def transcribe_audio_whisper(recording):
    model = WhisperModel(
        model_size_or_path="large-v3",
        device="cpu",
        compute_type="int8",
    )
    audio = np.frombuffer(recording, dtype=np.int16)
    _segments, _info = model.transcribe(audio=audio, language="en", beam_size=5)
    # _segments, _info = model.transcribe("sample_recording2.wav", language="en", beam_size=5)
    print(
        "Detected language '%s' with probability %f"
        % (_info.language, _info.language_probability)
    )
    segments = list(_segments)

    for segment in segments:
        print("[%.2fs -> %.2fs] %s" % (segment.start, segment.end, segment.text))


def main():
    # print_input_devices()
    logging.info("Starting the conversation")
    recording = record_audio()
    # logging.info(recording)
    logging.info("Transcribing the audio")
    transcribe_audio_whisper(recording)
    logging.info("Conversation ended")


if __name__ == "__main__":
    main()
