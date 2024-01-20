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
        response = self.interpreter_interface.send_message(transcription)

        return response

    def read_back_response(self, response):
        # Combine the text content from the response
        combined_response = ' '.join([msg['content'] for msg in response if msg['role'] == 'assistant' and 'content' in msg])

        # Step 4: Convert response to speech and play it
        if combined_response:
            print(f"Interpreter Response: {combined_response}")
            self.text_to_speech.synthesize_speech(combined_response)
        else:
            print("No response received.")