# app.py

import cv2
import os
from flask import (
    Flask, render_template, request, redirect,
    session, Response, jsonify, send_from_directory
)

# Corrected import block
from utils.controller import (
    toggle_light, toggle_fan, toggle_valve, set_brightness,
    get_status, get_light_status, get_fan_status,
    get_valve_status, get_water_status
)
from utils.auth import check_credentials
from utils.detector import detect_and_log

app = Flask(__name__)
app.secret_key = 'your_very_secret_key_that_is_long_and_secure'
CAMERA_INDEX = 1  # Use 0 for the default camera, or change if you have multiple

# ================== LOGIN & LOGOUT ===================
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

# ================== DASHBOARD ===================
@app.route('/')
def dashboard():
    if 'username' not in session:
        return redirect('/login')

    # Get system status
    status = get_status()
    water_flow = get_water_status()

    # Load latest 3 intrusion images
    snapshot_dir = 'snapshots'
    image_files = sorted(
        [f for f in os.listdir(snapshot_dir) if f.endswith('.jpg')],
        reverse=True
    )[:3]

    return render_template(
        'index.html',
        status=status,
        role=session.get('role'),
        snapshots=image_files,
        water_flow=water_flow
    )

# ================== STATIC FILES & SNAPSHOTS ===================
@app.route('/snapshots/<string:filename>')
def snapshot(filename):
    return send_from_directory('snapshots', filename)

# ================== API & CONTROL ROUTES ===================
@app.route('/toggle_light', methods=['POST'])
def toggle_light_route():
    if session.get('role') != 'admin':
        return jsonify({'error': 'Unauthorized'}), 403
    toggle_light()
    return jsonify({'light_status': get_light_status()})

@app.route('/toggle_fan', methods=['POST'])
def toggle_fan_route():
    if session.get('role') != 'admin':
        return jsonify({'error': 'Unauthorized'}), 403
    toggle_fan()
    return jsonify({'fan_status': get_fan_status()})

@app.route('/toggle_valve', methods=['POST'])
def toggle_valve_route():
    if session.get('role') != 'admin':
        return jsonify({'error': 'Unauthorized'}), 403
    toggle_valve()
    return jsonify({'valve_status': get_valve_status()})

@app.route('/set_brightness', methods=['POST'])
def set_brightness_route():
    if session.get('role') != 'admin':
        return jsonify({'error': 'Unauthorized'}), 403
    value = int(request.form.get('brightness', 100))
    set_brightness(value)
    return jsonify({'brightness': value, 'status': 'success'})

@app.route('/get_status')
def status_api():
    if 'username' not in session:
        return jsonify({'error': 'Unauthorized'}), 403
    return jsonify(get_status())

@app.route('/water_status')
def water_status_api():
    if 'username' not in session:
        return jsonify({'error': 'Unauthorized'}), 403
    return jsonify(get_water_status())

# ================== CAMERA FEED ===================
def generate_frames():
    cap = cv2.VideoCapture(CAMERA_INDEX)
    if not cap.isOpened():
        print("Error: Could not open video stream.")
        return

    while True:
        success, frame = cap.read()
        if not success:
            break
        
        # Face detection and logging
        frame, detected = detect_and_log(frame)
        if detected:
            cv2.putText(frame, "🟢 FACE DETECTED", (10, 30),
                        cv2.FONT_HERSHEY_SIMPLEX, 0.7, (0, 255, 0), 2)
        
        ret, buffer = cv2.imencode('.jpg', frame)
        if not ret:
            continue
            
        frame_bytes = buffer.tobytes()
        yield (b'--frame\r\n'
               b'Content-Type: image/jpeg\r\n\r\n' + frame_bytes + b'\r\n')
    
    cap.release()

@app.route('/camera_feed')
def camera_feed():
    if 'username' not in session:
        return redirect('/login')
    return Response(generate_frames(), mimetype='multipart/x-mixed-replace; boundary=frame')

# ================== START SERVER ===================
if __name__ == '__main__':
    os.makedirs('snapshots', exist_ok=True)
    os.makedirs('data', exist_ok=True)
    app.run(host='0.0.0.0', port=5000, debug=True)
