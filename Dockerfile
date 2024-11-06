# First stage: Build stage
FROM python:3.11-slim AS builder

# Set environment variables for the build stage
ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1

# Set the working directory
WORKDIR /app

# Install system dependencies for Python build
RUN apt-get update && apt-get install -y \
    build-essential \
    libpq-dev \
    && rm -rf /var/lib/apt/lists/*

# Copy only the requirements file to leverage Docker cache
COPY requirements.txt .

# Install Python dependencies
RUN pip install --upgrade pip && pip install --prefix=/install -r requirements.txt




# Second stage: Final runtime stage
FROM python:3.11-slim AS runtime

# Set environment variables for the runtime stage
ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1

# Set the working directory
WORKDIR /app

# Copy installed packages from the builder stage
COPY --from=builder /install /usr/local

# Copy the project code into the container
COPY . /app/

# Command to run your application (modify as needed)
CMD ["python", "app.py"]
