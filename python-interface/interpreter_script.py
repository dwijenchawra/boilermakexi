from interpreter import interpreter

# Initialize the interpreter
my_interpreter = interpreter.Interpreter()

# Listen for messages and respond
while True:
    message = input()  # Listen for input from the GUI process
    response = my_interpreter.process_message(message)
    print(response)  # Send the response back to the GUI process
