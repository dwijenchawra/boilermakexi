from flask import Flask, Response
import cv2
import mediapipe as mp


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
    return
    
def _running_wave():
    # run media_pipe.py
    # while is_running:
        # match debounced output to user gesture sequences
        # if match
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

#webcam
camera = cv2.VideoCapture(0)

def gen_frames():  
    while True:
        success, frame = camera.read()  # read the camera frame
        if not success:
            break
        else:
            frame = cv2.flip(frame, 1)
            ret, buffer = cv2.imencode('.jpg', frame)
            frame = buffer.tobytes()
            yield (b'--frame\r\n'
                   b'Content-Type: image/jpeg\r\n\r\n' + frame + b'\r\n')  # concat frame one by one and show result
                

@app.route('/video_feed')
def video_feed():
    return Response(gen_frames(), mimetype='multipart/x-mixed-replace; boundary=frame')


class Wave:
    def __init__(self):
        # self.is_running = False
        # self.thread = None (maybe use subprocess instead)
        return



if __name__ == '__main__':
    app.run(debug=True)
