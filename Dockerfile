# Use an official Python 3.9.6 image from the Alpine Linux distribution as the base image
FROM python:3.9.6-alpine

# Set the working directory inside the container to /usr/src/app
WORKDIR /usr/src/app

# Set environment variables to ensure Python does not write bytecode files (.pyc) and runs in unbuffered mode
ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

# Upgrade pip to the latest version
RUN pip install --upgrade pip

# Copy the requirements.txt file from the host to the working directory inside the container
COPY ./requirements.txt .

# Install Python dependencies listed in requirements.txt
RUN pip install -r requirements.txt

# Copy the entire project directory (including source code) from the host to the working directory inside the container
COPY . .
