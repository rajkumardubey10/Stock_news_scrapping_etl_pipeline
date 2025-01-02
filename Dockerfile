# Use an official Python base image
FROM python:3.9-slim

# Set the working directory in the container
WORKDIR /app

# Install PostgreSQL development libraries
RUN apt-get update && apt-get install -y libpq-dev

# Create a directory for logs inside the container
RUN mkdir -p /app/logs/investing_logs /app/logs/moneycontrol_logs

# Copy all the files to the container
COPY . .

# Copy the .env file separately to ensure it's available for the app
COPY .env /app/.env

# Install dependencies from requirements.txt
RUN pip install --no-cache-dir -r requirements.txt

# Declare a volume for logs
VOLUME ["/app/logs"]

# Run the Python script when the container starts
CMD ["python", "main.py"]
