import cv2
import os
import csv
from datetime import datetime, timedelta

# Load face detection model
face_cascade = cv2.CascadeClassifier(cv2.data.haarcascades + 'haarcascade_frontalface_default.xml')
if face_cascade.empty():
    raise IOError("Failed to load Haar cascade!")

# Paths
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
SNAPSHOT_DIR = os.path.join(BASE_DIR, '../snapshots')
LOG_PATH = os.path.join(BASE_DIR, '../data/intrusion_log.csv')

# Ensure folders exist
os.makedirs(SNAPSHOT_DIR, exist_ok=True)
os.makedirs(os.path.dirname(LOG_PATH), exist_ok=True)

# Init log file if not exist
if not os.path.isfile(LOG_PATH):
    with open(LOG_PATH, 'w', newline='') as f:
        writer = csv.writer(f)
        writer.writerow(['timestamp', 'image'])

# Global cooldown
last_detection_time = None
cooldown = timedelta(seconds=10)

def detect_and_log(frame):
    global last_detection_time
    detected = False

    # Convert and resize
    frame = cv2.resize(frame, (640, 480))
    gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)

    faces = face_cascade.detectMultiScale(gray, 1.1, 4)
    for (x, y, w, h) in faces:
        cv2.rectangle(frame, (x, y), (x+w, y+h), (0, 255, 0), 2)
        detected = True

    # Save only if cooldown passed
    if detected:
        now = datetime.now()
        if not last_detection_time or (now - last_detection_time) > cooldown:
            last_detection_time = now
            timestamp = now.strftime('%Y-%m-%d_%H-%M-%S')
            filename = f'snapshot_{timestamp}.jpg'
            filepath = os.path.join(SNAPSHOT_DIR, filename)
            cv2.imwrite(filepath, frame)
            with open(LOG_PATH, 'a', newline='') as file:
                writer = csv.writer(file)
                writer.writerow([timestamp.replace('_', ' '), filename])

    return frame, detected
