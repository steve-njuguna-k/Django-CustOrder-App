# Use an official Python 3.9.6 image from the Alpine Linux distribution as the base image
FROM python:3.9.6-alpine

# Set the working directory inside the container to /app
WORKDIR /app

# Set environment variables to ensure Python does not write bytecode files (.pyc) and runs in unbuffered mode
ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

# Upgrade pip to the latest version
RUN pip install --upgrade pip

# Copy the requirements.txt file and install dependencies
COPY requirements.txt /app/
RUN pip install --no-cache-dir -r requirements.txt

# Copy the rest of the application code
COPY . .