from threading import Thread, Event
from flask import Flask, Response
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


app = Flask(__name__)
cors = CORS(app)
app.config['CORS_HEADERS'] = 'Content-Type'
#video processing
latest_frame = None
#webcam
cap = cv2.VideoCapture(0)
#thread control
stop_event = Event()

app = Flask(__name__)

@app.route("/")
def hello_world():
    print("hello world endpoint is running")
    return "<p>Hello, World!</p>"

#load gesture-action pair from cloud or local
@app.route("/load_pairs")
def load_pairs(pairs):

    #pairs json

    return pairs

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
    global stop_event
    global latest_frame
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
        while cap.isOpened() and not stop_event.is_set():

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

                key = cv2.waitKey(5) & 0xFF
                if key == ord("a"):
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
            
            # Reduce the size by half
            scale_factor = 0.5

            # Calculate the new dimensions
            width = int(image.shape[1] * scale_factor)
            height = int(image.shape[0] * scale_factor)
            dim = (width, height)

            # Resize the frame
            image = cv2.resize(image, dim, interpolation=cv2.INTER_AREA)

            latest_frame = image
    pass

@app.route("/start_wave")
@cross_origin()
def start_wave():
    global stop_event
    stop_event.clear()
    thread = Thread(target=video_processing)
    thread.start()
    return "Video processing started"

@app.route("/stop_wave")
def stop_wave():
    global stop_event
    stop_event.set()  # Signal the thread to stop
    return "Video processing stopped"

@app.route("/train_gesture")
def train_gesture(gesture):

    return "successful"

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

if __name__ == "__main__":
    app.run(port=8000, debug=True)
