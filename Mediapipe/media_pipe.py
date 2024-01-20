import cv2
import mediapipe as mp
from Gesture_storage.Static_gesture import *
from Gesture_storage.Gesture_DB import *
from google.protobuf.json_format import MessageToDict
from Gesture_storage.utils import *

config = load_config()

mp_drawing = mp.solutions.drawing_utils
mp_drawing_styles = mp.solutions.drawing_styles
mp_hands = mp.solutions.hands

gesture_db = Gesture_DB(config["db_path"])


def get_keypoints_from_hand(hand):
    keypoint_pos = []
    for i in hand["landmark"]:
        # Acquire x, y but don't forget to convert to integer.
        keypoint_pos.append({"x": i["x"], "y": i["y"], "z": i["z"]})
    return keypoint_pos


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

        text = "no hands detected!"
        if results.multi_hand_landmarks:
            hand = MessageToDict(results.multi_hand_landmarks[-1])

            classification = MessageToDict(results.multi_handedness[-1])["classification"][-1]
            points = get_keypoints_from_hand(hand)
            gesture = init_gesture_from_values(endpoints=points,
                                               score=classification["score"],
                                               label=classification["label"],
                                               id="n/a",
                                               )
            id = gesture_db.match(gesture)
            print(id)
            text = id

            key = cv2.waitKey(5) & 0xFF
            if key == ord("a"):
                gesture_db.add_static_gesture(gesture)

            for hand_landmarks in results.multi_hand_landmarks:
                mp_drawing.draw_landmarks(
                    image,
                    hand_landmarks,
                    mp_hands.HAND_CONNECTIONS,
                    mp_drawing_styles.get_default_hand_landmarks_style(),
                    mp_drawing_styles.get_default_hand_connections_style())
        # Flip the image horizontally for a selfie-view display.
        image = cv2.putText(image, text, [50, 50], cv2.FONT_HERSHEY_SIMPLEX,
                            1, color=(255, 0, 0))
        image = cv2.flip(image, 1)
        cv2.imshow('MediaPipe Hands', image)
        if cv2.waitKey(5) & 0xFF == 27:
            break
cap.release()
