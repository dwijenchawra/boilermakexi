from audio_recorder import AudioRecorder
from transcription_service import TranscriptionService
from interpreter_interface import InterpreterInterface
from text_to_speech import TextToSpeech
from application_controller import ApplicationController
from interpreter import interpreter

def main():
    # Initialize the components
    audio_recorder = AudioRecorder()
    transcription_service = TranscriptionService()
    interpreter_interface = InterpreterInterface(interpreter)
    text_to_speech = TextToSpeech()

    app_controller = ApplicationController(audio_recorder, transcription_service, interpreter_interface, text_to_speech)

    try:
        while True:  # Run indefinitely until interrupted
            # Record and process user input
            response = app_controller.record_and_process_user_input()
            if response:
                # Read back the response
                app_controller.read_back_response(response)
            else:
                print("No response or an error occurred.")
    except KeyboardInterrupt:
        print("\nExiting application...")
    finally:
        # Cleanup resources
        audio_recorder.close()

if __name__ == "__main__":
    main()
