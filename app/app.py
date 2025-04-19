@app.route('/submit', methods=['POST'])
def submit():
email = request.form.get('email')

    visitor_info = {
        "timestamp": datetime.datetime.utcnow().isoformat(),
        "email": email,
        "ip": request.remote_addr,
        "user_agent": request.headers.get('User-Agent')
    }

    if os.path.exists(log_path):
        with open(log_path, 'r+') as f:
            try:
                data = json.load(f)
            except json.JSONDecodeError:
                data = []
            data.append(visitor_info)
            f.seek(0)
            json.dump(data, f, indent=2)
    else:
        with open(log_path, 'w') as f:
            json.dump([visitor_info], f, indent=2)

    return redirect('/success')
