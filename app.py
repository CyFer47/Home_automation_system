from flask import Flask, render_template, request, redirect, session, Response, jsonify, send_from_directory, url_for
from utils.controller import toggle_light, toggle_fan, get_status, set_brightness, get_light_status, get_fan_status, get_water_status, toggle_valve, get_valve_status
from utils.auth import check_credentials
from utils.detector import detect_and_log
from utils.water_logger import log_water_flow, get_water_history, check_abnormal_consumption, get_hourly_consumption
from utils.ventilation import get_env_status, control_ventilation, toggle_ventilation
import cv2
import os
import csv
from flask_mail import Mail, Message
from apscheduler.schedulers.background import BackgroundScheduler

app = Flask(__name__)
app.secret_key = 'your_very_secret_key'
CAMERA_INDEX = 0

# Email config
app.config['MAIL_SERVER'] = 'smtp.example.com'
app.config['MAIL_PORT'] = 587
app.config['MAIL_USERNAME'] = 'your_email@example.com'
app.config['MAIL_PASSWORD'] = 'your_password'
app.config['MAIL_USE_TLS'] = True
mail = Mail(app)

ADMIN_EMAIL_PATH = 'data/admin_email.txt'

def get_admin_email():
    if os.path.exists(ADMIN_EMAIL_PATH):
        with open(ADMIN_EMAIL_PATH, 'r') as f:
            return f.read().strip()
    return "admin@example.com"

def set_admin_email(email):
    with open(ADMIN_EMAIL_PATH, 'w') as f:
        f.write(email)

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
        return render_template('login.html', error="Invalid credentials")
    return render_template('login.html')

@app.route('/logout')
def logout():
    session.clear()
    return redirect('/login')

@app.route('/')
def dashboard():
    if 'username' not in session:
        return redirect('/login')
    snapshot_dir = 'snapshots'
    if not os.path.exists(snapshot_dir):
        os.makedirs(snapshot_dir)
    image_files = sorted(
        [f for f in os.listdir(snapshot_dir) if f.endswith('.jpg')],
        reverse=True
    )[:3]
    return render_template(
        'index.html',
        status=get_status(),
        role=session.get('role'),
        snapshots=image_files,
        water_flow=get_water_status(),
        admin_email=get_admin_email()
    )

@app.route('/snapshots/<filename>')
def snapshot(filename):
    return send_from_directory('snapshots', filename)

@app.route('/update_admin_email', methods=['POST'])
def update_admin_email():
    if session.get('role') == 'admin':
        email = request.form.get('admin_email')
        if email:
            set_admin_email(email)
    return redirect('/')

@app.route('/toggle_light', methods=['POST'])
def toggle_light_route():
    if session.get('role') != 'admin': return jsonify({'error': 'Unauthorized'}), 403
    toggle_light()
    return jsonify({'light_status': get_light_status()})

@app.route('/toggle_fan', methods=['POST'])
def toggle_fan_route():
    if session.get('role') != 'admin': return jsonify({'error': 'Unauthorized'}), 403
    toggle_fan()
    return jsonify({'fan_status': get_fan_status()})

@app.route('/toggle_valve', methods=['POST'])
def toggle_valve_route():
    if session.get('role') != 'admin': return jsonify({'error': 'Unauthorized'}), 403
    toggle_valve()
    return jsonify({'valve_status': get_valve_status()})

@app.route('/set_brightness', methods=['POST'])
def set_brightness_route():
    if session.get('role') != 'admin': return jsonify({'error': 'Unauthorized'}), 403
    value = int(request.form.get('brightness', 100))
    set_brightness(value)
    return jsonify({'status': 'success', 'brightness': value})

@app.route('/get_status')
def status_api():
    if 'username' not in session:
        return jsonify({'error': 'Unauthorized'}), 403
    status = get_status()  # Light/Fan/Valve status
    env = get_env_status()  # Temperature/Humidity/Ventilation
    status.update({
        'temperature': env.get('temperature'),
        'humidity': env.get('humidity'),
        'ventilation': env.get('ventilation')
    })
    return jsonify(status)

@app.route('/light-control')
def light_control():
    if 'username' not in session: return redirect('/login')
    return render_template('light_control.html', status=get_status(), role=session.get('role'))

@app.route('/water-flow')
def water_flow():
    if 'username' not in session: return redirect('/login')
    return render_template('water_flow.html', water_flow=get_water_status(), history=get_water_history(), abnormal=check_abnormal_consumption())

@app.route('/video-feed')
def video_feed():
    if 'username' not in session: return redirect('/login')
    return render_template('video_feed.html')

@app.route('/ventilation', methods=['GET', 'POST'])
def ventilation():
    if 'username' not in session:
        return redirect('/login')
    if request.method == 'POST' and session.get('role') == 'admin':
        toggle_ventilation()
    return render_template('ventilation.html', env=get_env_status(), role=session.get('role'))

@app.route('/access-areas')
def access_areas():
    if 'username' not in session: return redirect('/login')
    return render_template('access_areas.html')

@app.route('/report')
def report():
    if 'username' not in session: return redirect('/login')
    return render_template('report.html')

@app.route('/send_quick_report', methods=['POST'])
def send_quick_report():
    if 'username' not in session: return jsonify({'error': 'Unauthorized'}), 403
    return jsonify({'message': 'Report Sent (Simulated)!'})

def generate_frames():
    cap = cv2.VideoCapture(CAMERA_INDEX)
    cap.set(cv2.CAP_PROP_FRAME_WIDTH, 640)
    cap.set(cv2.CAP_PROP_FRAME_HEIGHT, 480)
    if not cap.isOpened():
        print("Error: Could not open video stream.")
        return
    while True:
        success, frame = cap.read()
        if not success:
            break
        frame, detected = detect_and_log(frame)
        if detected:
            cv2.putText(frame, "FACE DETECTED", (10, 30), cv2.FONT_HERSHEY_SIMPLEX, 0.7, (0, 0, 255), 2)
        ret, buffer = cv2.imencode('.jpg', frame)
        if not ret:
            continue
        frame_bytes = buffer.tobytes()
        yield (b'--frame\r\n'
               b'Content-Type: image/jpeg\r\n\r\n' + frame_bytes + b'\r\n')
    cap.release()

@app.route('/camera_feed')
def camera_feed():
    if 'username' not in session: return redirect('/login')
    return Response(generate_frames(), mimetype='multipart/x-mixed-replace; boundary=frame')

if __name__ == '__main__':
    if not os.path.exists('data'): os.makedirs('data')
    if not os.path.exists('snapshots'): os.makedirs('snapshots')
    scheduler = BackgroundScheduler()
    scheduler.add_job(log_water_flow, 'interval', hours=1)
    scheduler.start()
    app.run(host='0.0.0.0', port=5000, debug=True)


#comment