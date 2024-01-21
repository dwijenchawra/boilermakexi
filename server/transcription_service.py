import subprocess
import re

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
            print(cleaned_transcription)
            return f'{cleaned_transcription}. Keep your response brief'
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