import cv2
import mediapipe as mp

import gestures.simple_gestures_lib as sgest


class MyVideoCapture:

    def __init__(self):
        # Open the video source
        self.vid = cv2.VideoCapture(0)
        self.vid.set(3, 300)
        self.vid.set(4, 150)
        self.mp_drawing = mp.solutions.drawing_utils
        self.mp_hands = mp.solutions.hands
        self.hands = self.mp_hands.Hands(
            min_detection_confidence=0.7, min_tracking_confidence=0.7)
        if not self.vid.isOpened():
            raise ValueError("Unable to open video source", 0)
        # Get video source width and height
        self.width = self.vid.get(cv2.CAP_PROP_FRAME_WIDTH)
        self.height = self.vid.get(cv2.CAP_PROP_FRAME_HEIGHT)

    def get_frame(self):
        if self.vid.isOpened():
            success, image = self.vid.read()
            image = cv2.cvtColor(cv2.flip(image, 1), cv2.COLOR_BGR2RGB)
            image.flags.writeable = False
            results = self.hands.process(image)

            image.flags.writeable = True
            image = cv2.cvtColor(image, cv2.COLOR_RGB2BGR)
            if results.multi_hand_landmarks:
                for hand_landmarks in results.multi_hand_landmarks:
                    self.mp_drawing.draw_landmarks(
                        image, hand_landmarks, self.mp_hands.HAND_CONNECTIONS)
            # if cv2.waitKey(33) == ord('s'):
            # fingers = {'index': (), 'middle': (), 'ring': (), 'pinky': ()}
            fingers = {}
            if results.multi_hand_landmarks:
                for hand_landmarks in results.multi_hand_landmarks:
                    fingers['index'] = sgest.check_index_finger(hand_landmarks)
                    fingers['start_stop'] = sgest.get_start_stop(hand_landmarks)
                    fingers['ninja'] = sgest.search_for_ninja_turtle(hand_landmarks)
                    fingers['middle'] = sgest.check_middle_finger(hand_landmarks)
                    # fingers['ring'] = sgest.check_ring_finger(hand_landmarks)
                    # fingers['pinky'] = sgest.check_pinky_finger(hand_landmarks)
            else:
                fingers = None
            return fingers, image, success

    # Release the video source when the object is destroyed
    def release(self):
        print('My video capture delete')
        if self.vid.isOpened():
            self.vid.release()
        self.hands.close()
