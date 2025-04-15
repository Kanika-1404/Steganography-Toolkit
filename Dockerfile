# Use official Python image
FROM python:3.11-slim

# System dependencies
RUN apt-get update && \
    apt-get install -y ffmpeg && \
    apt-get clean && \
    rm -rf /var/lib/apt/lists/*

# Set working directory
WORKDIR /app

# Copy requirements and install
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy the rest of your code
COPY . .

# Expose port (adjust if not using 5000)
EXPOSE 5000

# Set entrypoint (assuming Flask app)
CMD ["gunicorn", "--bind", "0.0.0.0:5000", "app:app"]
