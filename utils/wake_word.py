import os
from vosk import Model, KaldiRecognizer
import logging

class WakeWordManager:
    def __init__(self, wake_word="hello", model_path="model"):
        self.wake_word = wake_word
        self.check_model_files()
        self.model_path = model_path
        self.wake_word = wake_word
        self.model = Model(model_path)
        self.recognizer = KaldiRecognizer(self.model, 16000)

    def check_model_files(self):
        if not os.path.exists("vosk_model"):
            print(
                "Please download the model from https://github.com/alphacep/kaldi-android-demo/releases and unpack as 'model' in the current folder."
            )
            exit(1)

    def detect_wake_word(self, data):
        if self.recognizer.AcceptWaveform(data):
            result = self.recognizer.Result()
            logging.debug(result)
            return self.wake_word in result
        return False
