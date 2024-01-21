from interpreter import interpreter

# Listen for messages and respond
while True:
    message = input()  # Listen for input from the GUI process
    response = interpreter.send_message(message)
    print(response)  # Send the response back to the GUI process
