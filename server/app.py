from flask import Flask

app = Flask(__name__)

@app.route("/")
def hello_world():
    return "<p>Hello, World!</p>"

@app.route("/load_pairs")
def load_pairs(pairs):

    #pairs json

    return pairs

@app.route("/save_pairs")
def save_pairs(pairs):

    #pairs json

    return pairs

@app.route("/start_wave")
def start_wave():
    # is_running = True
    # thread = _detect_wave()
    # success = start thread
    # return success 
    
def _running_wave():

    # run media_pipe.py
    # while is_running:
        # match debounced output to user gesture sequences
        # if match
            # run mapped action

@app.route("/stop_wave")
def stop_wave():
    # is_running = False
    # thread.join()
    # return success

@app.route("/train_gesture")
def train_gesture(gesture):

    return "successful"

@app.route("/delete_gesture")
def delete_gesture(gesture):

    return "successful"

@app.route("/rename_gesture")
def rename_gesture_gesture(gesture):

    #new_name =
    return new_name

@app.route("/message_interpreter")
def message_interpreter(message):
    response = interpreter.chat(message)
    return response

class Wave:
    def __init__(self):
        # self.is_running = False
        # self.thread = None



if __name__ == '__main__':
    app.run(debug=True)
