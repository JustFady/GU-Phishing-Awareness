# Use a small Python base image
FROM python:3.10-slim

# Set working directory
WORKDIR /app

# Copy requirements and install
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy everything inside /app (your app source folder)
COPY app/ .

# Expose Flask's default port
EXPOSE 5000

# Run the app
CMD ["python", "app.py"]
