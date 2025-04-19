from flask import Flask, render_template, request, redirect
import os
import json
import datetime

@app.route('/submit', methods=['POST'])
def submit():
    # Get the email from the submitted form
    email = request.form.get('email')

    # Gather info about the visitor
    visitor_info = {
        "timestamp": datetime.datetime.utcnow().isoformat(),
        "email": email,
        "ip": request.remote_addr,
        "user_agent": request.headers.get('User-Agent')
    }

    # Make sure the logs folder exists
    os.makedirs('app/logs', exist_ok=True)

    # Load existing data or start a new list
    log_file = 'app/logs/visits.json'
    if os.path.exists(log_file):
        with open(log_file, 'r') as f:
            try:
                data = json.load(f)
            except json.JSONDecodeError:
                data = []
    else:
        data = []

    # Add new visitor info and save it
    data.append(visitor_info)
    with open(log_file, 'w') as f:
        json.dump(data, f, indent=2)

    # Redirect to success page after submission
    return redirect('/success')
