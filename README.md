## How to Run the App Locally

### Option 1 – Docker (recommended)

    docker-compose up --build

Builds the image, starts the container, mounts a volume for logs, and serves the site at  
http://localhost:5000

### Option 2 – Manual (no Docker)

    pip install -r requirements.txt   # install dependencies
    python app/app.py                 # start Flask app

## Temporary Live Demo (expires May 14 2025)

https://gu-phishing-awareness.onrender.com/  
https://gu-phishing-awareness.onrender.com/success  
https://gu-phishing-awareness.onrender.com/view-logs  

## What It Does

* Fake password‑reset form
* Captures every submission and stores it locally (JSON file or Docker volume)
* Redirects to a bogus success page after submit
* `/view-logs` shows everything and lets you download data as JSON, CSV, or TXT

For demo and educational use only.
