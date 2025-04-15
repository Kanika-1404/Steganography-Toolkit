# Use an official Python image
FROM python:3.11-slim

# Install FFmpeg
RUN apt-get update && apt-get install -y ffmpeg

# Set work directory
WORKDIR /app

# Copy project files
COPY . .

# Install dependencies
RUN pip install --no-cache-dir -r requirements.txt

# Expose port (for Flask default)
EXPOSE 5000

# Command to run the app
CMD ["gunicorn", "app:app", "--bind", "0.0.0.0:5000"]
