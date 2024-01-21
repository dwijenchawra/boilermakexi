from flask import Flask
from flask_cors import CORS, cross_origin
app = Flask(__name__)
cors = CORS(app)
app.config['CORS_HEADERS'] = 'Content-Type'

app = Flask(__name__)

@app.route("/")
def hello_world():
    print("hello world endpoint is running")
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
@cross_origin()
def start_wave():
    print("we have begun recording")
    # is_running = True
    # thread = _detect_wave()
    # success = start thread
    # return success 
    return "it worked"
    
def _running_wave():
    # run media_pipe.py
    # while is_running:
    # match debounced output to user gesture sequences
    # if matc    
    # run mapped action
    return

@app.route("/stop_wave")
def stop_wave():
    # is_running = False
    # thread.join()
    # return success
    return

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
        return



if __name__ == '__main__':
    app.run(debug=True)
