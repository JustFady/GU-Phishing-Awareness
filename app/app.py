from flask import Flask, render_template, request, redirect
import os
import json
import datetime

app = Flask(__name__)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/submit', methods=['POST'])
def submit():
    # Grab the email from the form
    email = request.form.get('email')

    # Build an entry with timestamp and IP
    entry = {
        "time": datetime.datetime.utcnow().isoformat(),
        "email": email,
        "ip": request.remote_addr
    }

    # Ensure logs folder and file exist
    os.makedirs('logs', exist_ok=True)
    log_file = 'logs/visits.json'
    if os.path.exists(log_file):
        with open(log_file, 'r') as f:
            data = json.load(f)
    else:
        data = []

    # Append and save
    data.append(entry)
    with open(log_file, 'w') as f:
        json.dump(data, f, indent=2)

    return redirect('/success')

@app.route('/success')
def success():
    return render_template('success.html')

if __name__ == '__main__':
    # Default host=127.0.0.1, port=5000
    app.run(debug=True)
