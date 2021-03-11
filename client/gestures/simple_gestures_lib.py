from math import sqrt

INDEX_FINGER_TOP = 8
INDEX_FINGER_BOTTOM = 5
MIDDLE_FINGER_TOP = 12
MIDDLE_FINGER_BOTTOM = 9
RING_FINGER_TOP = 16
RING_FINGER_BOTTOM = 13
PINKY_FINGER_TOP = 20
PINKY_FINGER_BOTTOM = 17
THUMB_TOP = 4
THUMB_CENTER = 3
THUMB_BOTTOM = 2


def calculate_distance(ax, ay, bx, by):
    distance = sqrt(((bx - ax) ** 2 + (by - ay) ** 2))
    return distance


def get_start_stop(hand_landmarks):
    index_finger = check_index_finger(hand_landmarks)
    middle_finger = check_middle_finger(hand_landmarks)
    ring_finger = check_ring_finger(hand_landmarks)
    pinky_finger = check_pinky_finger(hand_landmarks)
    is_thumb_near_index = is_thumb_near_index_finger(hand_landmarks)

    if not index_finger['straight'] and middle_finger['straight'] and ring_finger['straight'] and pinky_finger['straight'] and is_thumb_near_index:
        return 'start'
    else:
        thumb_top_y = hand_landmarks.landmark[THUMB_TOP].y
        thumb_bottom_y = hand_landmarks.landmark[THUMB_BOTTOM].y
        is_thumb_straight = check_finger(hand_landmarks, THUMB_TOP, THUMB_BOTTOM)['straight']
        if is_thumb_straight:
            if thumb_bottom_y + 0.1 < thumb_top_y:
                return 'stop'
            else:
                return 'nothing'
        else:
            return 'nothing'

def search_for_ninja_turtle(hand_landmarks):
    index_finger = check_index_finger(hand_landmarks)
    pinky_finger = check_pinky_finger(hand_landmarks)
    middle_finger = check_middle_finger(hand_landmarks)
    ring_finger = check_ring_finger(hand_landmarks)
    if index_finger['straight'] and pinky_finger['straight'] and not middle_finger['straight'] and not ring_finger['straight']:
        #return 'ninja'
        return {'ninja': 'ninja', 'x': index_finger['x'], 'y': index_finger['y']}
    else:
        return 'nothing'

def check_index_finger(hand_landmarks):
    return check_finger(hand_landmarks, INDEX_FINGER_TOP, INDEX_FINGER_BOTTOM)


def check_middle_finger(hand_landmarks):
    return check_finger(hand_landmarks, MIDDLE_FINGER_TOP, MIDDLE_FINGER_BOTTOM)


def check_ring_finger(hand_landmarks):
    return check_finger(hand_landmarks, RING_FINGER_TOP, RING_FINGER_BOTTOM)


def check_pinky_finger(hand_landmarks):
    return check_finger(hand_landmarks, PINKY_FINGER_TOP, PINKY_FINGER_BOTTOM)


def check_finger(hand_landmarks, top_idx, bottom_idx):
    ax = hand_landmarks.landmark[top_idx].x
    ay = hand_landmarks.landmark[top_idx].y
    bx = hand_landmarks.landmark[bottom_idx].x
    by = hand_landmarks.landmark[bottom_idx].y
    distance_top_bottom = calculate_distance(ax, ay, bx, by)
    ax = hand_landmarks.landmark[bottom_idx].x
    ay = hand_landmarks.landmark[bottom_idx].y
    bx = hand_landmarks.landmark[0].x
    by = hand_landmarks.landmark[0].y
    distance_bottom_start = calculate_distance(ax, ay, bx, by)

    if distance_bottom_start < distance_top_bottom + 0.05:
        straight = True
    else:
        straight = False
    return {'straight': straight, 'x': hand_landmarks.landmark[top_idx].x, 'y': hand_landmarks.landmark[top_idx].y}


def is_thumb_near_index_finger(hand_landmarks):
    thumb_top = hand_landmarks.landmark[THUMB_TOP]
    index_finger_top = hand_landmarks.landmark[INDEX_FINGER_TOP]
    distance = calculate_distance(thumb_top.x, thumb_top.y, index_finger_top.x, index_finger_top.y)
    return distance < 0.1
