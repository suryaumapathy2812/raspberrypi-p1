import pyaudio
import logging


class PyAudioManager:
    def __init__(self):
        self.pyaudio_instance = pyaudio.PyAudio()
        self.streams = []
        self.FRAMES_PER_BUFFER = 480 
        self.FORMAT = pyaudio.paInt16
        self.CHANNELS = 1
        self.RATE = 16000
        self.CHUNK = 1024
        self.INTERVAL_SIZE = 10000

    def get_device_info(self, device_index):
        return self.pyaudio_instance.get_device_info_by_index(device_index)
      
    def get_all_device_info(self):
        num_devices = self.pyaudio_instance.get_device_count()
        return [self.get_device_info(i) for i in range(num_devices)]

    def open_stream_default(self):
        stream = self.pyaudio_instance.open(
            format=self.FORMAT,
            channels=self.CHANNELS,
            rate=self.RATE,
            input=True,
            frames_per_buffer=self.FRAMES_PER_BUFFER,
        )
        self.streams.append(stream)
        return stream

   
    def open_stream(self, **kwargs):
        stream = self.pyaudio_instance.open(**kwargs)
        self.streams.append(stream)
        return stream

    def close_all_streams(self):
        for stream in self.streams:
            stream.stop_stream()
            stream.close()
        self.streams = []

    def terminate(self):
        self.close_all_streams()
        self.pyaudio_instance.terminate()
    