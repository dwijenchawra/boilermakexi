from threading import Thread, Event
from flask import Flask, Response, request
import cv2
import mediapipe as mp
from Hand_Tracking.Pose_storage.Pose_DB import *
from google.protobuf.json_format import MessageToDict
from Hand_Tracking.Pose_Detection_Model.inference import *
from Hand_Tracking.Pose_Detection_Model.train import *
from Hand_Tracking.Gesture_Detection.Detector import *
from Hand_Tracking.Debouncer.debounce import debounce
from flask_cors import CORS, cross_origin
import subprocess
import os
from audio_recorder import AudioRecorder
import time
from transcription_service import TranscriptionService
import re
from interpreter import interpreter

app = Flask(__name__)
cors = CORS(app)
app.config['CORS_HEADERS'] = 'Content-Type'
#video processing
latest_frame = None
#webcam
cap = cv2.VideoCapture(0)
#thread control
stop_wave_event = Event()
stop_alright_wave_event = Event()
training_event = Event()

command_text= ""
alright_wave_string = ""
from threading import Thread, Event
from flask import Flask, Response, request
import cv2
import mediapipe as mp
from Hand_Tracking.Pose_storage.Pose_DB import *
from google.protobuf.json_format import MessageToDict
from Hand_Tracking.Pose_Detection_Model.inference import *
from Hand_Tracking.Pose_Detection_Model.train import *
from Hand_Tracking.Gesture_Detection.Detector import *
from Hand_Tracking.Debouncer.debounce import debounce
from flask_cors import CORS, cross_origin
import subprocess
import os
from audio_recorder import AudioRecorder
import time
from transcription_service import TranscriptionService
import re
from interpreter import interpreter

app = Flask(__name__)
cors = CORS(app)
app.config['CORS_HEADERS'] = 'Content-Type'
#video processing
latest_frame = None
#webcam
cap = cv2.VideoCapture(0)
#thread control
stop_wave_event = Event()
stop_alright_wave_event = Event()
training_event = Event()

command_text= ""
alright_wave_string = ""

app = Flask(__name__)

@app.route("/")
def hello_world():
    print("hello world endpoint is running")
    print("hello world endpoint is running")
    return "<p>Hello, World!</p>"

#load gesture-action pair from cloud or local
#load gesture-action pair from cloud or local
@app.route("/load_pairs")
def load_pairs(pairs):

    #pairs json

    return pairs

#upload gesture-action pair to cloud and local
#upload gesture-action pair to cloud and local
@app.route("/save_pairs")
def save_pairs(pairs):

    #pairs json

    return pairs

#script execution
'''
Example usage
result = execute_script('/path/to/your/script.py')
print(result)
'''

def execute_script(script_path):
    try:
        # Check if the file exists
        if not os.path.exists(script_path):
            return "Script file does not exist"

        # Determine the type of script based on its extension
        _, file_extension = os.path.splitext(script_path)

        if file_extension == '.py':
            # Execute a Python script
            subprocess.run(['python', script_path], check=True)
        elif file_extension == '.scpt':
            # Execute an AppleScript file
            subprocess.run(['osascript', script_path], check=True)
        else:
            return "Unsupported script type"

        return "Execution successful"
    except subprocess.CalledProcessError as e:
        return f"An error occurred during script execution: {e}"
    except Exception as e:
        return f"An error occurred: {e}"

#hand_tracking stuff
def video_processing():
    global stop_wave_event
    global latest_frame
    global training_event

    config = load_config()
    inference = MLP_Inference(threads=config["threads"])
    # double load because might reset output
    config = load_config()

    mp_drawing = mp.solutions.drawing_utils
    mp_drawing_styles = mp.solutions.drawing_styles
    mp_hands = mp.solutions.hands

    pose_db = Pose_DB(config["db_path"])
    detector = Detector(time_delta=config["time_delta"])

    def get_keypoints_from_hand(hand):
        keypoint_pos = []
        for i in hand["landmark"]:
            # Acquire x, y but don't forget to convert to integer.
            keypoint_pos.append({"x": i["x"], "y": i["y"], "z": i["z"]})
        return keypoint_pos

    tmp_dataset = []

    def show_hand(hand, image):
        mp_drawing.draw_landmarks(
            image,
            hand,
            mp_hands.HAND_CONNECTIONS,
            mp_drawing_styles.get_default_hand_landmarks_style(),
            mp_drawing_styles.get_default_hand_connections_style())

    # For webcam input:

    with mp_hands.Hands(
            model_complexity=0,
            min_detection_confidence=0.5,
            min_tracking_confidence=0.5) as hands:
        while cap.isOpened() and not stop_wave_event.is_set():

            success, image = cap.read()
            if not success:
                print("Ignoring empty camera frame.")
                # If loading a video, use 'break' instead of 'continue'.
                continue

            # To improve performance, optionally mark the image as not writeable to
            # pass by reference.
            image.flags.writeable = False
            image = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)
            results = hands.process(image)
            # Draw the hand annotations on the image.
            image.flags.writeable = True
            image = cv2.cvtColor(image, cv2.COLOR_RGB2BGR)

            # key logic for adding an action
            point = None
            text = "no hands detected!"
            if results.multi_hand_landmarks:
                hand = MessageToDict(results.multi_hand_landmarks[-1])

                classification = MessageToDict(results.multi_handedness[-1])["classification"][-1]
                points = get_keypoints_from_hand(hand)
                inference_pts = [[pt["x"], pt["y"]] for pt in points]
                landmark_list = calc_landmark_list(image, results.multi_hand_landmarks[-1])
                point = calc_pointer(image, hand["landmark"][8])

                pre_processed_landmark_list = pre_process_landmark(landmark_list)
                pose = init_pose_from_values(endpoints=points,
                                            score=classification["score"],
                                            label=classification["label"],
                                            parsed_endpoints=pre_processed_landmark_list,
                                            id="n/a",
                                            )

                id = pose_db.match(pose)

                inference_id = inference(pre_processed_landmark_list)
                #print("inference_id  -----------   ", inference_id)
                # print(id, inference_id)
                text = f"{id}, {inference_id}"

                if training_event.is_set():
                    if id == 'n/a':
                        # succeed in being different enough
                        # need to appent datapoints to a tmp dataset
                        row = [len(pose_db.poses)]
                        row.extend(pre_processed_landmark_list)
                        tmp_dataset.append(row)
                else:
                    if len(tmp_dataset) != 0 and len(tmp_dataset) < config["sample_count"]:
                        print("error, not enough dataset has been generated, please regenerat a new one")
                        tmp_dataset = []

                # check if enough of dataset is created:
                if len(tmp_dataset) > config["sample_count"]:
                    # can extend the csv file and retain the model
                    pose_db.add_static_pose(pose)
                    add_to_csv(tmp_dataset, config["dataset_path"])
                    tmp_dataset = []
                    # now need to train
                    config["output_classes"] += 1
                    update_config(config)
                    train()

                    inference = MLP_Inference(threads=config["inference_threads"])
                    training_event.clear()
                    #query frontend that training has ended

                image_width, image_height = image.shape[1], image.shape[0]
                detector.update_state(point, image_width, image_height)
                temp = detector.get_state()

                # temp is a tuple
                three, four = temp

                # id, inference_id, three four
                # format this string with width 10, just ljust it
                width = 10

                text = f"{str(id).ljust(width)} {str(inference_id).ljust(width)} {str(three).ljust(width)} {str(four).ljust(width)}"

                for hand_landmarks in results.multi_hand_landmarks:
                    mp_drawing.draw_landmarks(
                        image,
                        hand_landmarks,
                        mp_hands.HAND_CONNECTIONS,
                        mp_drawing_styles.get_default_hand_landmarks_style(),
                        mp_drawing_styles.get_default_hand_connections_style())
            # Flip the image horizontally for a selfie-view display.
            image = cv2.flip(image, 1)
            image = cv2.putText(image, text, [50, 50], cv2.FONT_HERSHEY_SIMPLEX,
                                1, color=(255, 0, 0), thickness=3)
            
            '''
            # Reduce the size by half
            scale_factor = 0.5

            # Calculate the new dimensions
            width = int(image.shape[1] * scale_factor)
            height = int(image.shape[0] * scale_factor)
            dim = (width, height)

            # Resize the frame
            image = cv2.resize(image, dim, interpolation=cv2.INTER_AREA)
            '''
            latest_frame = image

def start_wave_internal():
    global stop_wave_event
    stop_wave_event.clear()
    thread = Thread(target=video_processing)
    thread.start()
    return "Video processing started"

@app.route("/start_wave")
@cross_origin()
@cross_origin()
def start_wave():
    with app.app_context():
        return start_wave_internal()

def stop_wave_internal():
    global stop_wave_event
    stop_wave_event.set()  # Signal the thread to stop
    return "Video processing stopped"
    with app.app_context():
        return start_wave_internal()

def stop_wave_internal():
    global stop_wave_event
    stop_wave_event.set()  # Signal the thread to stop
    return "Video processing stopped"

@app.route("/stop_wave")
@cross_origin()
@cross_origin()
def stop_wave():
    with app.app_context():
        return stop_wave_internal()


def check_for_phrase(string, *args):
    global alright_wave_string
    # Get the phrase to check for  
    # Read the file content
    cleaned_text = re.sub(r'[^\w\s]', '', string).lower()
    # Check if the phrase appears in the text
    for (i, phrase) in enumerate(args):
        if phrase in cleaned_text:
            alright_wave_string = ""
            return True

def alright_wave():
    ar = AudioRecorder()
    ts = TranscriptionService()
    global command_text
    global stop_alright_wave_event
    global alright_wave_string
    while not stop_alright_wave_event.is_set():
        # Record and transcribe
        ar.start_recording()
        time.sleep(2.5)
        ar.stop_recording()
        ar._save_recording()
        text = ts.transcribe_audio("recording.wav")
        alright_wave_string = f"{alright_wave_string} {text}"
        # Check for wake phrase
        if check_for_phrase(alright_wave_string, 'alright wave', 'all right wave', 'all rightwave', 'alrightwave'):
            print("Wake phrase detected. Listening for command...")

            # Record a command after wake phrase is detected
            ar.start_recording()
            #super jank way to do this (only 5 second commands at most allowed)
            time.sleep(4)
            ar.stop_recording()
            ar._save_recording()
            command_text = ts.transcribe_audio("recording.wav")

            # Process the command
            process_command()

def process_command():
    if check_for_phrase(command_text, 'start wave'):
        print("start wave")
        with app.app_context():
            start_wave_internal()
    elif check_for_phrase(command_text, 'stop wave'):
        print("stop wave")
        with app.app_context():
            stop_wave_internal()
    elif check_for_phrase(command_text, 'train gesture'):
        print("train gesture")
        with app.app_context():
            train_gesture()    

@app.route("/start_alright_wave")
def start_alright_wave():
    global stop_alright_wave_event
    stop_alright_wave_event.clear()
    thread = Thread(target=alright_wave)
    thread.start()
    return "Alright Wave started"

@app.route("/stop_alright_wave")
def stop_alright_wave():
    global stop_alright_wave_event
    stop_alright_wave_event.set()
    return "Alright Wave stopped"
    with app.app_context():
        return stop_wave_internal()

@app.route("/train_gesture")
def train_gesture():
    time.sleep(3)
    global training_event
    training_event.set()
    return "Gesture training started"

@app.route("/create_action")
def create_action():
    instructions = request.form['instructions']
    interpreter.auto_run = True
    response = interpreter.chat(instructions)
    return response


'''
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
'''

#get frames from video processing 
def gen_frames():  
    global latest_frame
    while True:
        if latest_frame is not None:
            ret, buffer = cv2.imencode('.jpg', latest_frame)
            if ret:
                frame_bytes = buffer.tobytes()
                yield (b'--frame\r\n'
                       b'Content-Type: image/jpeg\r\n\r\n' + frame_bytes + b'\r\n')

@app.route('/video_feed')
def video_feed():
    return Response(gen_frames(), mimetype='multipart/x-mixed-replace; boundary=frame')


if __name__ == '__main__':
    app.run(port = 8000, debug=True)
