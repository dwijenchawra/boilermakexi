from gtts import gTTS
import os
import playsound

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