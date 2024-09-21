# python docker image
# # Use the official Python image from the Docker Hub
FROM python:3.9-bookworm

# Use an official Ubuntu image as the base
# FROM ubuntu:20.04

# Set environment variables to prevent Python from writing pyc files to disk 
# and to buffer output (useful for Docker logs)
# ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1

# Set environment to prevent timezone prompts
ENV DEBIAN_FRONTEND=noninteractive

RUN apt-get update && apt-get install -y ffmpeg

# Install dependencies
RUN apt-get update && \
    apt-get install -y \
    --no-install-recommends \
    # ffmpeg \
    python3 \
    python3-pip \
    redis-server \
    postgresql-client && \
    rm -rf /var/lib/apt/lists/*

# # Set the working directory inside the container
WORKDIR /app

# Upgrade pip
RUN pip install --upgrade pip


# Copy the requirements file into the container
COPY requirements.txt .

# Install the dependencies
RUN pip install -r requirements.txt

# Copy the rest of the application code into the container
COPY . .

# Create a shell script to start services
RUN echo '#!/bin/bash\n\
service redis-server start\n\
exec python3 manage.py runserver 0.0.0.0:8000' > /start.sh && \
    chmod +x /start.sh

# Expose the port the app runs on
EXPOSE 8000

# Use CMD to run the shell script
CMD ["/bin/bash", "/start.sh"]
