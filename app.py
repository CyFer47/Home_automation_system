from flask import Flask, render_template, request, redirect, session, url_for, Response
from utils.controller import toggle_light, toggle_fan, get_status
from utils.auth import check_credentials
from utils.detector import detect_and_log
import cv2
import os

app = Flask(__name__)
app.secret_key = 'your_secret_key'

CAMERA_INDEX = 1  # Change as needed

# ============ LOGIN SYSTEM ============

@app.route('/')
def dashboard():
    if 'username' not in session:
        return redirect('/login')
    status = get_status()
    return render_template('index.html', status=status, role=session['role'])

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        role = check_credentials(username, password)
        if role:
            session['username'] = username
            session['role'] = role
            return redirect('/')
        else:
            return render_template('login.html', error="Invalid credentials")
    return render_template('login.html')

@app.route('/logout')
def logout():
    session.clear()
    return redirect('/login')


# ============ DEVICE CONTROL ============

@app.route('/toggle_light', methods=['POST'])
def light():
    if session.get('role') != 'admin':
        return {'error': 'Unauthorized'}, 403
    toggle_light()
    return get_status()

@app.route('/toggle_fan', methods=['POST'])
def fan():
    if session.get('role') != 'admin':
        return {'error': 'Unauthorized'}, 403
    toggle_fan()
    return get_status()


# ============ CAMERA VIEW ONLY ============
@app.route('/camera_feed')
def camera_feed():
    if 'username' not in session:
        return redirect('/login')

    def gen():
        cap = cv2.VideoCapture(CAMERA_INDEX)
        while True:
            success, frame = cap.read()
            if not success:
                break

            # Run detection and get annotated frame
            processed_frame, detected = detect_and_log(frame)

            # Add text overlay
            if detected:
                cv2.putText(processed_frame, "🟢 FACE DETECTED", (10, 30),
                            cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 255, 0), 3)
            else:
                cv2.putText(processed_frame, "No face detected", (10, 30),
                            cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 0, 255), 2)

            ret, buffer = cv2.imencode('.jpg', processed_frame)
            frame_bytes = buffer.tobytes()

            yield (b'--frame\r\n'
                   b'Content-Type: image/jpeg\r\n\r\n' + frame_bytes + b'\r\n')

        cap.release()

    return Response(gen(), mimetype='multipart/x-mixed-replace; boundary=frame')


# ============ RUN FLASK APP ============

if __name__ == '__main__':
    os.makedirs('snapshots', exist_ok=True)
    os.makedirs('data', exist_ok=True)
    app.run(debug=True)
