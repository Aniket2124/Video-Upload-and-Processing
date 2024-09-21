# Video Processing App

This project is a video processing application that allows users to upload, process, and view videos, with integrated subtitle search functionality.

## Prerequisites

- Python 3.9+
- Docker
- PostgreSQL
- Redis
- Virtualenv
- PGAdmin (for PostgreSQL database management)

## Setup Guide
### 1. Clone the Repository

- git clone <repository-url>
- cd <repository-folder>

### 2. Create and Activate Virtual Environment

It's recommended to use a virtual environment to manage your project's dependencies.

```bash
# Install virtualenv if you don't have it
pip install virtualenv

# Create a virtual environment
virtualenv venv
#OR
python3 -m venv venv

# Activate the virtual environment
# On Linux/macOS:
source venv/bin/activate

# On Windows:
venv\Scripts\activate

### Note:-
### If You Have Docker Installed

1. **Start Docker**: Ensure Docker is running on your system.

2. **Build and Start Services**: Use the following command to build and start your Docker services as defined in the `docker-compose.yml` file:

   ```bash
   docker-compose up --build

### Django development server is starting and showing Starting development server at http://0.0.0.0:8000/, but you cannot access the application from http://localhost:8000 or http://127.0.0.1:8000

### If you don`t have docker setup on your system
## Update Database Credentials in Django Settings
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql',
        'NAME': '<your-database-name>',
        'USER': '<your-database-user>',
        'PASSWORD': '<your-database-password>',
        'HOST': 'localhost',
        'PORT': '5432',
    }
}

## Install Requirements
pip install -r requirements.txt

## Run Migrations
python manage.py makemigrations
python manage.py migrate

## Create a Superuser
python manage.py createsuperuser

## Run redis server
celery -A video_processing worker -l info

## Run the Django Server
python manage.py runserver
