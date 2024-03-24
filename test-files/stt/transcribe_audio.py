
import os
from dotenv import load_dotenv
import logging
from faster_whisper import WhisperModel

load_dotenv(dotenv_path="./../.env")

logging.basicConfig()
logging.getLogger("faster_whisper").setLevel(logging.DEBUG)

model_size = os.getenv("WHISPER_MODEL") or "large-v2"
model_device = os.getenv("WHISPER_DEVICE") or "cpu"

def main():
  logging.info("starting")
  model = WhisperModel(model_size, device="cpu", compute_type="int8")
  ## Uncomment the following line to use beam search
  _segments, _info = model.transcribe("sample_recording2.wav", language="en", beam_size=5 )
  
  ## Uncomment the following line to use VAD
  # _segments, _info = model.transcribe("sample_recording.mp3",language="en", vad_filter=True, vad_parameters=dict(min_silence_duration_ms=500))
  print("Detected language '%s' with probability %f" % (_info.language, _info.language_probability))
  segments = list(_segments) 
  
  for segment in segments:
    print("[%.2fs -> %.2fs] %s" % (segment.start, segment.end, segment.text))


if __name__ == "__main__":
  main()
