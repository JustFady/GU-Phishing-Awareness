FROM python:3.10-slim

WORKDIR /app

# Copy requirements and install dependencies
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy application code
COPY app/ ./

# Print directory structure for debugging
RUN find . -type d | sort

# Create data directory with proper permissions
RUN mkdir -p /data && chmod 777 /data

# Use a volume for persistent data storage
VOLUME /data

# Set environment variables
ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1
ENV DATA_DIR=/data
ENV FLASK_DEBUG=1

# Expose the application port
EXPOSE 5000

# Run the application with unbuffered output
CMD ["python", "-u", "app.py"]
