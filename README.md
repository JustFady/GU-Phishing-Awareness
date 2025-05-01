# GU-Phishing-Awareness

A phishing awareness demo for Gonzaga University that simulates a password change form to collect user submissions.

## File Structure

```
app/
├── assets/               # Static assets (images, favicon)
├── app.py                # Main Flask application
└── __init__.py           # Python package initialization
```

## Running the Application

### Using Docker Compose
```bash
docker-compose up --build
```

This will:
1. Build the Docker image
2. Start the container
3. Mount a persistent volume for data storage
4. Make the app available at http://localhost:5000

### Manual Setup
1. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```

2. Run the application:
   ```bash
   python app/app.py
   ```

## Features
- Password change form that captures credentials
- Successful form submission redirects to a confirmation page
- All captured data is stored in a persistent volume
- View all submissions at http://localhost:5000/view-logs
- Download submissions in JSON, CSV, or TXT format
