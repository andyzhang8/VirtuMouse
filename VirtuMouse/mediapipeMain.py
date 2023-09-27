import mediapipe as mp
import cv2
from win32api import GetSystemMetrics
import pydirectinput as inp

mp_drawing = mp.solutions.drawing_utils
mp_hands = mp.solutions.hands


def getAvailableCameraDevices():
    # checks the first 10 indexes.
    index = 0
    arr = []
    i = 10
    while i > 0:
        cap = cv2.VideoCapture(index)
        if cap.read()[0]:
            arr.append(index)
            cap.release()
        index += 1
        i -= 1
    return arr

def getMidpoint(hand, image, h, w):
    mx = ((hand.landmark[mp_hands.HandLandmark.INDEX_FINGER_MCP].x * w) + (hand.landmark[mp_hands.HandLandmark.WRIST].x * w) + (hand.landmark[mp_hands.HandLandmark.PINKY_MCP].x * w)) / 3
    my = ((hand.landmark[mp_hands.HandLandmark.INDEX_FINGER_MCP].y * h) + (hand.landmark[mp_hands.HandLandmark.WRIST].y * h) + (hand.landmark[mp_hands.HandLandmark.PINKY_MCP].y * h)) / 3
    
    # cv2.circle(image, (int(mx), int(my)), 5, (0, 0, 255), -1)

    return mx, my

def drawLandmarks(hand, image, h, w):
    
    cv2.line(image, 
                (int(hand.landmark[mp_hands.HandLandmark.INDEX_FINGER_MCP].x * w), int(hand.landmark[mp_hands.HandLandmark.INDEX_FINGER_MCP].y * h)),
                (int(hand.landmark[mp_hands.HandLandmark.PINKY_MCP].x * w), int(hand.landmark[mp_hands.HandLandmark.PINKY_MCP].y * h)),
                (255,0,0),2)
    cv2.line(image, 
                (int(hand.landmark[mp_hands.HandLandmark.INDEX_FINGER_MCP].x * w), int(hand.landmark[mp_hands.HandLandmark.INDEX_FINGER_MCP].y * h)),
                (int(hand.landmark[mp_hands.HandLandmark.WRIST].x * w), int(hand.landmark[mp_hands.HandLandmark.WRIST].y * h)),
                (255,0,0),2)
    
    cv2.line(image, 
                (int(hand.landmark[mp_hands.HandLandmark.WRIST].x * w), int(hand.landmark[mp_hands.HandLandmark.WRIST].y * h)),
                (int(hand.landmark[mp_hands.HandLandmark.PINKY_MCP].x * w), int(hand.landmark[mp_hands.HandLandmark.PINKY_MCP].y * h)),
                (255,0,0),2)
    
        
def main():

    
    devices = getAvailableCameraDevices()
    camera = 0

    if len(devices) == 1:
        print("[INFO] One input device found")
    else:
        camera = input(f'[INFO] Multuple input devices detected: {devices}\nSelect one ')


    cap = cv2.VideoCapture(camera)

    with mp_hands.Hands(min_detection_confidence=0.8, min_tracking_confidence=0.5) as hands: 
        while cap.isOpened():
            ret, frame = cap.read()
            h, w, c = frame.shape
            mx = GetSystemMetrics(0) / w
            my = GetSystemMetrics(1) / h
            
            # BGR 2 RGB
            image = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
            
            # Flip on horizontal
            image = cv2.flip(image, 1)
            
            # Set flag
            image.flags.writeable = False
            
            # Detections
            results = hands.process(image)
            
            # Set flag to true
            image.flags.writeable = True
            
            # RGB 2 BGR
            image = cv2.cvtColor(image, cv2.COLOR_RGB2BGR)
            
            
            # Rendering results
            if results.multi_hand_landmarks:
                for hand in results.multi_hand_landmarks:
                    # drawLandmarks(hand, image, h, w)
                    x, y = getMidpoint(hand, image, h, w)
                    inp.moveTo(int(x * mx), int(y * my))


            if cv2.waitKey(10) & 0xFF == ord('q'):
                break

    cap.release()


if __name__ == '__main__':
    main()