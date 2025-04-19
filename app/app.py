from flask import Flask, render_template, request, redirect
import os
import json
import datetime

app = Flask(__name__)

LOG_FILE = 'logs/visits.json'


@app.route('/')
def index():
    return render_template('index.html')


@app.route('/submit', methods=['POST'])
def submit():
    email = request.form.get('email')
    visitor_info = {
        "timestamp": datetime.datetime.utcnow().isoformat(),
        "email": email,
        "ip": request.remote_addr,
        "user_agent": request.headers.get('User-Agent')
    }

    os.makedirs('logs', exist_ok=True)

    if os.path.exists(LOG_FILE):
        with open(LOG_FILE, 'r+') as f:
            try:
                data = json.load(f)
            except json.JSONDecodeError:
                data = []
            data.append(visitor_info)
            f.seek(0)
            json.dump(data, f, indent=2)
    else:
        with open(LOG_FILE, 'w') as f:
            json.dump([visitor_info], f, indent=2)

    return redirect('/success')


@app.route('/success')
def success():
    return render_template('success.html')


if __name__ == '__main__':
    app.run(debug=True)
