import os
import json
from datetime import datetime
from flask import Flask, render_template, request, redirect

app = Flask(__name__)


@app.route('/')
def index():
    # Show the password change form
    return render_template('index.html')


@app.route('/submit', methods=['POST'])
def submit():
    # Get the email from the form
    email = request.form.get('email')

    # Build log entry
    entry = {
        "time": datetime.utcnow().isoformat(),
        "email": email,
        "ip": request.remote_addr
    }

    # Ensure logs folder exists
    os.makedirs('logs', exist_ok=True)
    log_file = 'logs/visits.json'

    # Load existing entries or start new list
    try:
        with open(log_file) as f:
            data = json.load(f)
    except Exception:
        data = []

    # Save the new entry
    data.append(entry)
    with open(log_file, 'w') as f:
        json.dump(data, f, indent=2)

    # Redirect to success page
    return redirect('/success')


@app.route('/success')
def success():
    # Show confirmation
    return render_template('success.html')


if __name__ == '__main__':
    # Run the app locally
    app.run(debug=True)
