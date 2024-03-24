# Raspberry Pi 4 - Simple Assistant

## Description

This python script is a simple assistant that can be run on a Raspberry Pi 4. It uses the `vosk` for Voice Activity Detection to listen for the `wakeword` (alexa, can be modified), then uses Azure Cognitive Speech services to listen to the user's command and sends the command to the OpenAI Assistant API to process.

## Installation

```bash
sudo apt-get update
sudo apt-get upgrade

sudo apt-get install libportaudio2 libportaudiocpp0
sudo apt install portaudio19-dev
```

```bash
python3 -m venv venv
source venv/bin/activate

pip install -r requirements.txt

wget https://alphacephei.com/vosk/models/vosk-model-small-en-us-0.15.zip
unzip vosk-model-small-en-us-0.15.zip
mv vosk-model-small-en-us-0.15/* vosk_model/

# Clean up
# rm -rf vosk-model-small-en-us-0.15.zip vosk-model-small-en-us-0.15

python3 main.py
```

## Configuration

- Rename the `.env.example` to `.env`
- Create an account on [Azure Cognitive Services](https://azure.microsoft.com/en-us/services/cognitive-services/speech-to-text/)
- Create an account on [OpenAI](https://beta.openai.com/signup/)
- Create an assistant on OpenAI
- Add the following variables to the `.env` file

```bash
# Azure Cognitive Services
AZURE_SPEECH_KEY=<YOUR_AZURE_SPEECH_KEY>
AZURE_SPEECH_REGION=<YOUR_AZURE_SPEECH_REGION>

# OpenAI API
OPENAI_API=<YOUR_OPENAI_API>
ASSISTANT_ID=<YOUR_ASSISTANT_ID>
```

### Personal References

- https://www.youtube.com/watch?v=n2FKsPt83_A&t=940s
- https://www.youtube.com/watch?v=SAIsk0i7KgU
- [audio detection](https://stackoverflow.com/questions/59698199/how-to-detect-input-audio-existence-and-do-action-whenever-it-exists)
- [TTS](https://www.nickersonj.com/posts/whisper-and-tortoise/#using-tortoise-text-to-speech)
- https://colab.research.google.com/drive/1IHum-j2AOjVOs_ZoqJ5yBUjf1kI4SLmt?usp=sharing
- https://colab.research.google.com/drive/1GTfQWyysAO3Lvhk5JMew1ipnXflILujz?usp=sharing
- https://www.nickersonj.com/posts/whisper-and-tortoise/#using-tortoise-text-to-speech
