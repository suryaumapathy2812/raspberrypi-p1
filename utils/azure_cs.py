import os
from dotenv import load_dotenv

import azure.cognitiveservices.speech as speechsdk

class AzureSpeechToText:
    def __init__(self, subscription_key, service_region):
        self.subscription_key = subscription_key
        self.service_region = service_region
        self.speech_config = speechsdk.SpeechConfig(subscription=subscription_key, region=service_region,speech_recognition_language="en-IN")
        self.audio_config = speechsdk.audio.AudioConfig(use_default_microphone=True)
        self.speech_recognizer = speechsdk.SpeechRecognizer(speech_config=self.speech_config, audio_config=self.audio_config)
        
    def recognize_from_microphone(self):
        print("Say something...")
        result = self.speech_recognizer.recognize_once()
        if result.reason == speechsdk.ResultReason.RecognizedSpeech:
            print("Recognized: {}".format(result.text))
            return result.text
        elif result.reason == speechsdk.ResultReason.NoMatch:
            print("No speech could be recognized")
        elif result.reason == speechsdk.ResultReason.Canceled:
            cancellation_details = result.cancellation_details
            print("Speech Recognition canceled: {}".format(cancellation_details.reason))
            if cancellation_details.reason == speechsdk.CancellationReason.Error:
                print("Error details: {}".format(cancellation_details.error_details))
        return None