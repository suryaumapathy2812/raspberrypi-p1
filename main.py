import os
import logging
from dotenv import load_dotenv
import pyaudio
from playsound import playsound

from utils.audio import PyAudioManager
from utils.azure_cs import AzureSpeechToText
from utils.wake_word import WakeWordManager
from utils.assistant import Assistant

load_dotenv(".env")

logging.basicConfig(level=logging.INFO)

FRAMES_PER_BUFFER = 480
FORMAT = pyaudio.paInt16
CHANNELS = 1
RATE = 16000
CHUNK = 1024
INTERVAL_SIZE = 10000


def present_message(response):
    content_block = response.content[0]
    if content_block.type == "text":
        print("Assistant: ", content_block.text.value)
    # elif content_block.type == "image":
    #   print("Assistant: Image received")
    else:
        print("Assistant: Unknown content type")


def main():
    am = PyAudioManager()
    devices = am.get_all_device_info()
    for i, device in enumerate(devices):
        print(f"Device {i}: {device['name']}")

    am.open_stream_default()
    wakeword = WakeWordManager(model_path="vosk_model", wake_word="alexa")
    azure_cs = AzureSpeechToText(
        subscription_key="03a1cd3c605d412492b47eff1abb2bdc", service_region="eastus"
    )
    assistant = Assistant()

    while True:
        stream = am.streams[0]
        text = None
        try:
            data = stream.read(4096, exception_on_overflow=False)
            # print(data)
            is_detected = wakeword.detect_wake_word(data)
            logging.debug(is_detected)
            if is_detected:
                playsound("./assets/ping.mp3")
                text = azure_cs.recognize_from_microphone()
                logging.debug(text)

            if (text is None) or (text.strip() == ""):
                text = None
                continue

            if text.lower().replace(".", " ").strip() == "stop":
                break

            if text is not None:
                print(f"User: {text}")
                reply = assistant.send_message(text)
                present_message(reply)
                if reply.content[0].type == "text":
                    azure_cs.generate_speech(reply.content[0].text.value)

        except OSError as e:
            print(f"Overflow error: {e}")
        except KeyboardInterrupt:
            print("\nStopping...")
            break

    am.close_all_streams()
    am.terminate()


if __name__ == "__main__":
    main()
