import cv2
import os
import csv
from datetime import datetime, timedelta

# Load Haar cascade for face detection
face_cascade = cv2.CascadeClassifier(cv2.data.haarcascades + 'haarcascade_frontalface_default.xml')

# Directory setup
SNAPSHOT_DIR = 'snapshots'
LOG_PATH = 'data/intrusion_log.csv'
os.makedirs(SNAPSHOT_DIR, exist_ok=True)
os.makedirs(os.path.dirname(LOG_PATH), exist_ok=True)

# Create CSV if not exists
if not os.path.isfile(LOG_PATH):
    with open(LOG_PATH, 'w', newline='') as file:
        writer = csv.writer(file)
        writer.writerow(['timestamp', 'image'])

# Detection cooldown setup
last_detection_time = None
cooldown = timedelta(seconds=10)

def detect_and_log(frame):
    global last_detection_time
    gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
    faces = face_cascade.detectMultiScale(gray, scaleFactor=1.1, minNeighbors=4, minSize=(60, 60))
    detected = False
    for (x, y, w, h) in faces:
        cv2.rectangle(frame, (x, y), (x+w, y+h), (255, 0, 0), 2)
        detected = True
    if detected:
        now = datetime.now()
        if not last_detection_time or (now - last_detection_time) > cooldown:
            last_detection_time = now
            timestamp = now.strftime('%Y-%m-%d_%H-%M-%S')
            filename = f'snapshot_{timestamp}.jpg'
            filepath = os.path.join(SNAPSHOT_DIR, filename)
            small_frame = cv2.resize(frame, (320, 240))
            cv2.imwrite(filepath, small_frame)
            with open(LOG_PATH, 'a', newline='') as file:
                writer = csv.writer(file)
                writer.writerow([timestamp.replace('_', ' '), filename])
    return frame, detected
