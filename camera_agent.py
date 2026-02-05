import cv2
import time

class OpenCVCameraAgent:
    def __init__(self):
        # Load the built-in OpenCV detectors
        self.face_cascade = cv2.CascadeClassifier(cv2.data.haarcascades + 'haarcascade_frontalface_default.xml')
        self.eye_cascade = cv2.CascadeClassifier(cv2.data.haarcascades + 'haarcascade_eye.xml')
        
        self.close_start_time = None
        self.LONG_CLOSURE_LIMIT = 2.0 # Seconds

    def detect_status(self, frame):
        gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
        # 1. Find faces first (eyes are inside faces)
        faces = self.face_cascade.detectMultiScale(gray, 1.3, 5)
        
        eyes_detected = False
        for (x, y, w, h) in faces:
            roi_gray = gray[y:y+h, x:x+w]
            # 2. Search for eyes only within the face area
            eyes = self.eye_cascade.detectMultiScale(roi_gray, 1.1, 10)
            if len(eyes) >= 2:
                eyes_detected = True
                break

        # Logic for closure
        if not eyes_detected:
            if self.close_start_time is None:
                self.close_start_time = time.time()
            
            duration = time.time() - self.close_start_time
            if duration > self.LONG_CLOSURE_LIMIT:
                return "LONG CLOSURE"
            return "EYES CLOSED"
        else:
            self.close_start_time = None
            return "EYES OPEN"

# --- Simple Loop ---
import cv2
import time

class OpenCVCameraAgent:
    def __init__(self):
        # Load the built-in OpenCV detectors
        self.face_cascade = cv2.CascadeClassifier(cv2.data.haarcascades + 'haarcascade_frontalface_default.xml')
        self.eye_cascade = cv2.CascadeClassifier(cv2.data.haarcascades + 'haarcascade_eye.xml')
        
        self.close_start_time = None
        self.LONG_CLOSURE_LIMIT = 2.0 # Seconds

    def detect_status(self, frame):
        gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
        # 1. Find faces first (eyes are inside faces)
        faces = self.face_cascade.detectMultiScale(gray, 1.3, 5)
        
        eyes_detected = False
        for (x, y, w, h) in faces:
            roi_gray = gray[y:y+h, x:x+w]
            # 2. Search for eyes only within the face area
            eyes = self.eye_cascade.detectMultiScale(roi_gray, 1.1, 10)
            if len(eyes) >= 2:
                eyes_detected = True
                break

        # Logic for closure
        if not eyes_detected:
            if self.close_start_time is None:
                self.close_start_time = time.time()
            
            duration = time.time() - self.close_start_time
            if duration > self.LONG_CLOSURE_LIMIT:
                return "LONG CLOSURE"
            return "EYES CLOSED"
        else:
            self.close_start_time = None
            return "EYES OPEN"

# --- Simple Loop ---
cap = cv2.VideoCapture(0)
agent = OpenCVCameraAgent()

while True:
    ret, frame = cap.read()
    status = agent.detect_status(frame)
    cv2.putText(frame, status, (50, 50), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 0, 255), 2)
    cv2.imshow('OpenCV Only Detection', frame)
    if cv2.waitKey(1) & 0xFF == ord('q'): break

cap.release()
cv2.destroyAllWindows()