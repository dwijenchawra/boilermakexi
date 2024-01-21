import pyaudio
import threading
import wave

class AudioRecorder:
    def __init__(self, filename="recording.wav", format=pyaudio.paInt16, channels=1, rate=16000, chunk=1024):
        self.filename = filename
        self.format = format
        self.channels = channels
        self.rate = rate
        self.chunk = chunk
        self.frames = []
        self.is_recording = False
        self.audio = pyaudio.PyAudio()
        self.stream = None
        self.thread = None

    def start_recording(self):
        if self.is_recording:
            return  # Already recording
        self.is_recording = True

        p = pyaudio.PyAudio()
        info = p.get_host_api_info_by_index(0)
        numdevices = info.get('deviceCount')

        # set device_id to the mic with "MacBook Pro Microphone" in its name
        device_id = None
        for i in range(0, numdevices):
            if (p.get_device_info_by_host_api_device_index(0, i).get('maxInputChannels')) > 0:
                if ("MacBook Pro Microphone" in p.get_device_info_by_host_api_device_index(0, i).get('name')):
                    device_id = i
                    break


        self.frames = []
        self.stream = self.audio.open(format=self.format, channels=self.channels,
                                      rate=self.rate, input=True,
                                      frames_per_buffer=self.chunk, input_device_index=device_id)
        self.thread = threading.Thread(target=self._record)
        self.thread.start()

    def _record(self):
        while self.is_recording:
            data = self.stream.read(self.chunk)
            self.frames.append(data)

    def stop_recording(self):
        if not self.is_recording:
            return  # Not recording
        self.is_recording = False
        self.thread.join()
        self.stream.stop_stream()
        self.stream.close()
        self.stream = None
        self._save_recording()

    def _save_recording(self):
        with wave.open(self.filename, 'wb') as wf:
            wf.setnchannels(self.channels)
            wf.setsampwidth(self.audio.get_sample_size(self.format))
            wf.setframerate(self.rate)
            wf.writeframes(b''.join(self.frames))

    def close(self):
        self.audio.terminate()