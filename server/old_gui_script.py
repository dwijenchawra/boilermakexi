from interpreter import interpreter
import pyaudio
import threading
import wave
import subprocess
import re
from gtts import gTTS
import os
import playsound


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
        self.frames = []
        self.stream = self.audio.open(format=self.format, channels=self.channels,
                                      rate=self.rate, input=True,
                                      frames_per_buffer=self.chunk)
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
    
class TranscriptionService:
    def __init__(self, whisper_cpp_path="./whisper.cpp/main", model_path="whisper.cpp/models/ggml-base.en.bin"):
        self.whisper_cpp_path = whisper_cpp_path
        self.model_path = model_path

    def transcribe_audio(self, file_path):
        try:
            command = [self.whisper_cpp_path, "-m", self.model_path, "-f", file_path]
            result = subprocess.run(command, capture_output=True, text=True, check=True)
            transcription = result.stdout.strip()

            # Clean the transcription
            cleaned_transcription = self._clean_transcription(transcription)
            return cleaned_transcription
        except subprocess.CalledProcessError as e:
            print(f"An error occurred while transcribing: {e}")
            return None

    def _clean_transcription(self, transcription):
        # Remove timestamps and blank audio tags
        cleaned = re.sub(r'\[\d{2}:\d{2}:\d{2}\.\d{3} --> \d{2}:\d{2}:\d{2}\.\d{3}\]', '', transcription)
        cleaned = re.sub(r'\[BLANK_AUDIO\]', '', cleaned)
        
        # Remove extra whitespaces
        cleaned = ' '.join(cleaned.split())

        return cleaned
    
class InterpreterInterface:
    def __init__(self, interpreter, max_budget=0.01):
        self.interpreter = interpreter
        self.max_budget = max_budget
        self.conversation_history = []

    def send_message(self, message):
        # Send the message to open-interpreter
        # Assuming `interpreter.chat()` is the method to send messages
        self.interpreter.chat(message)
        self._update_conversation_history(role="user", message=message)

    def receive_response(self):
        # Receive the response from open-interpreter
        # This could be a direct return from `interpreter.chat()` or another method
        # Assuming `interpreter.get_response()` gets the latest response
        response = self.interpreter.get_response()
        self._update_conversation_history(role="assistant", message=response)
        return response

    def _update_conversation_history(self, role, message):
        # Update the conversation history
        self.conversation_history.append({"role": role, "message": message})

    def get_conversation_history(self):
        return self.conversation_history


class TextToSpeech:
    def __init__(self, language='en'):
        self.language = language

    def synthesize_speech(self, text, output_file='output.mp3'):
        # Convert the text to speech
        tts = gTTS(text=text, lang=self.language)
        tts.save(output_file)

        # Play the converted audio
        playsound.playsound(output_file)

        # Optionally, remove the audio file after playing
        os.remove(output_file)

class ApplicationController:
    def __init__(self, audio_recorder, transcription_service, interpreter_interface, text_to_speech):
        self.audio_recorder = audio_recorder
        self.transcription_service = transcription_service
        self.interpreter_interface = interpreter_interface
        self.text_to_speech = text_to_speech

    def record_and_process_user_input(self):
        # Step 1: Record audio
        self.audio_recorder.start_recording()
        print("Recording... (Press Enter to stop)")
        input()  # Wait for user to press Enter to stop recording
        self.audio_recorder.stop_recording()

        # Step 2: Transcribe audio
        transcription = self.transcription_service.transcribe_audio(self.audio_recorder.filename)
        if transcription is None:
            print("Error in transcription.")
            return

        print(f"Transcribed Text: {transcription}")

        # Step 3: Send to interpreter and get response
        self.interpreter_interface.send_message(transcription)
        response = self.interpreter_interface.receive_response()

        return response

    def read_back_response(self, response):
        # Step 4: Convert response to speech and play it
        if response:
            print(f"Interpreter Response: {response}")
            self.text_to_speech.synthesize_speech(response)
        else:
            print("No response received.")
