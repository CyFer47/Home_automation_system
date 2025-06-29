from flask import Flask, render_template, request, redirect, session, url_for
from utils.controller import toggle_light, toggle_fan, get_status
from utils.auth import check_credentials

app = Flask(__name__)
app.secret_key = 'your_secret_key'  # Use a secure key in real app

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

if __name__ == '__main__':
    app.run(debug=True)
