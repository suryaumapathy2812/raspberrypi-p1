from vosk import Model, KaldiRecognizer
import os
import pyaudio


if not os.path.exists("vosk_model"):
    print(
        "Please download the model from https://github.com/alphacep/kaldi-android-demo/releases and unpack as 'model' in the current folder."
    )
    exit(1)

# Define the path to the Vosk model you downloaded
model_path = "vosk_model"
wake_word = "hello"  # Define your wake word here

# Load the Vosk model
model = Model(model_path)

# Initialize PyAudio and open the microphone stream
p = pyaudio.PyAudio()
stream = p.open(
    format=pyaudio.paInt16, channels=1, rate=16000, input=True, frames_per_buffer=8192
)
stream.start_stream()

# Initialize the recognizer
recognizer = KaldiRecognizer(model, 16000)

print("Listening for the wake word...")

while True:
    data = stream.read(4096)
    if recognizer.AcceptWaveform(data):
        result = recognizer.Result()
        # Check for the wake word in the recognition result
        if wake_word in result:
            print("Wake word detected!")
            # Perform action upon detecting the wake word...
