import subprocess
import time

import cv2
import mediapipe as mp
from Hand_Tracking.Pose_storage.Pose_DB import *
from google.protobuf.json_format import MessageToDict
from Hand_Tracking.Pose_Detection_Model.inference import *
from Hand_Tracking.Pose_Detection_Model.train import *
from Hand_Tracking.Gesture_Detection.Detector import *
from Hand_Tracking.Debouncer.debounce import debounce

config = load_config()
inference = MLP_Inference(threads=config["threads"])
# double load because might reset output
config = load_config()

mp_drawing = mp.solutions.drawing_utils
mp_drawing_styles = mp.solutions.drawing_styles
mp_hands = mp.solutions.hands

pose_db = Pose_DB(config["db_path"])
detector = Detector(time_delta=config["time_delta"])

# LOAD PATH TO GESTURE SEQUENCES FILE
gest_seq_path = config["gest_seq_path"]

# execute applescript given file path
def execute_applescript(file_path):
    # join path with actions subdirectory
    file_path = os.path.join(config["actions_directory"], file_path)
    subprocess.run(["osascript", file_path], check=True)



class Sequence:
    def __init__(self, name, action, seq):
        self.name = name
        self.action = action

        self.matchers = []

        # seq is a list dict of poses and directions
        # need to convert to list of strings
        self.seq = seq

        # convert to list of strings
        self.seq_strs = []

        for i in self.seq:
            # check if item is a pose or direction
            if "p_class" in i:
                # pose
                self.seq_strs.append(i["p_class"][-1]) # get id of pose
            else:
                # direction
                self.seq_strs.append(i["d_class"])

    def clear_matchers(self):
        # clear all matchers when a sequence is matched
        self.matchers = []

    def check_match(self, curr_pose, curr_direction):
        # check if any of the matchers match
        # if they do, return the action
        # if they don't, return None

        for matcher in self.matchers:
            state = matcher.update(curr_pose, curr_direction)
            if state == Matcher.state_dict["MATCHED"]:
                # matched
                self.clear_matchers()
                return self.action
            elif state == Matcher.state_dict["DELETE"]:
                self.matchers.remove(matcher)
                del matcher

        if curr_pose == self.seq_strs[0]:
            # pose matches first item in sequence, create new matcher
            self.matchers.append(Matcher(self, miss_limit=7))

        return None

    def print_matchers(self):
        out = ""
        for matcher in self.matchers:
            out += f"Matcher: {matcher.seq_index}/{len(self.seq_strs)}\t"
        print(out)



class Matcher:

    state_dict = {
        "MATCHING": 0,
        "MATCHED": 1,
        "DELETE": 2
    }

    '''
    This class is used to keep track of a stream match
    We are getting gesture and pose from video, and want to see if it matches
    a gesture sequence
    '''

    def __init__(self, sequence: Sequence, miss_limit=5):
        self.seq = sequence
        self.seq_index = 1 # start at 1 because we already checked first item
        self.matched = False
        self.miss_count = 0
        self.miss_limit = miss_limit

    def update(self, curr_pose, curr_direction):
        # check if next item in sequence matches
        # if it does, increment seq_index
        # if it doesn't, increment miss_count
        # if miss_count exceeds miss_limit, delete Matcher

        if curr_pose == self.seq.seq_strs[self.seq_index]:
            # pose matches
            self.seq_index += 1
        elif curr_direction == self.seq.seq_strs[self.seq_index]:
            # direction matches
            self.seq_index += 1
        else:
            # miss
            self.miss_count += 1
            self.seq_index = 0
            if self.miss_count > self.miss_limit:
                return self.state_dict["DELETE"]

        if self.seq_index == len(self.seq.seq_strs):
            # matched
            return self.state_dict["MATCHED"]

        return self.state_dict["MATCHING"]


def pre_process_gest_seq(gest_seq_path):
    gest_seqs = []

    '''
    The gesture sequence file is a json file
    
    Here is a brief overview of the fields:

    compatible_model: Specifies the compatible model file, in this case, "model001.pkl".
    
    pose_classes: Defines different pose classes, each with a unique identifier (p_class) and a name (p_name).
    
    direction_classes: Describes different direction classes, each with a type (d_type) and a class identifier (d_class). The directions include LEFT, RIGHT, UP, DOWN, INTO_SCREEN, OUT_OF_SCREEN, CCW (Counter Clockwise), and CW (Clockwise).
    
    gesture_sequences: Specifies sequences of gestures, each with a sequence name (seq_name), a sequence of poses and directions (seq), and an associated action (action). In the example provided, there is a "swipe" sequence with specific poses and directions triggering the action "switch_tabs".
    '''
    with open(gest_seq_path, "r") as f:
        raw_gest_seq_file = json.load(f)

    print(raw_gest_seq_file)

    for seq in raw_gest_seq_file["gesture_sequences"]:
        print("seq: ", seq)
        name = seq["seq_name"]
        action = seq["action"]
        seq = seq["seq"]
        gest_seqs.append(Sequence(name, action, seq))

    return gest_seqs, raw_gest_seq_file


# preprocess the gesture sequences
gest_seqs, raw_gest_seq_file = pre_process_gest_seq(gest_seq_path)


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
cap = cv2.VideoCapture(0)
with mp_hands.Hands(
        model_complexity=0,
        min_detection_confidence=0.5,
        min_tracking_confidence=0.5) as hands:
    while cap.isOpened():
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
            direction_val, in_out_screen = temp

            # id, inference_id, three four
            # format this string with width 10, just ljust it
            width = 10

            text = f"{str(id).ljust(width)} {str(inference_id).ljust(width)} {str(direction_val).ljust(width)} {str(in_out_screen).ljust(width)}"
            print(text)

            # check if any of the sequences match
            for seq in gest_seqs:
                # seq.print_matchers()
                action = seq.check_match(str(inference_id), direction_val)
                if action is not None:
                    print(f"Action: {action} RAAAAAAHHHHH!!!!")
                    execute_applescript(action)

                    # do something with action

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
        cv2.imshow('MediaPipe Hands', image)
        if cv2.waitKey(5) & 0xFF == 27:
            break
cap.release()
