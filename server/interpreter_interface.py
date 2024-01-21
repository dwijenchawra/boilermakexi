class InterpreterInterface:
    def __init__(self, interpreter, max_budget=0.01):
        self.interpreter = interpreter
        self.max_budget = max_budget
        self.interpreter.auto_run = True
        self.conversation_history = []

    def send_message(self, message):
        # Send the message and receive the response
        response = self.interpreter.chat(message)
        self._update_conversation_history(role="user", message=message)
        self._update_conversation_history(role="assistant", message=response)
        return response

    def _update_conversation_history(self, role, message):
        # Update the conversation history
        self.conversation_history.append({"role": role, "message": message})

    def get_conversation_history(self):
        return self.conversation_history
