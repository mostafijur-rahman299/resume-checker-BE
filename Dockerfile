# Use a specific Python runtime version as a parent image
FROM python:3.11-slim

# Set environment variables
# To remove .pyc file cause it's not necessary for containers which will reduce the size of container
ENV PYTHONDONTWRITEBYTECODE=1
# This disables output buffering in Python, which makes sure that logs are immediately visible in the Docker logs
ENV PYTHONUNBUFFERED=1

# Set the working directory
WORKDIR /app

# Install system dependencies for Python build
RUN apt-get update && apt-get install -y \
    build-essential \
    libpq-dev \
    && rm -rf /var/lib/apt/lists/*

# Install Python dependencies
COPY requirements.txt /app/
RUN pip install --upgrade pip && pip install -r requirements.txt

# Copy the project code into the container
COPY . /app/
