# Use a small Python base
FROM python:3.10-slim

# Set /app as our working directory
WORKDIR /app

# First copy just requirements and install them
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Now copy the rest of the code
COPY app/ ./app
COPY templates/ ./templates
COPY static/ ./static

# Expose port 5000 (Flask default)
EXPOSE 5000

# Run the Flask app
CMD ["python", "app/app.py"]
