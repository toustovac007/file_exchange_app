# File Exchange

A simple web application for uploading and downloading files built with Flask.

## Features

- Upload files
- Download files
- List available files

## Setup

1. Clone or download the project.
2. Install dependencies:
   ```
   pip install -r requirements.txt
   ```
3. Run the application:
   ```
   python app.py
   ```
4. Open your browser and go to `http://127.0.0.1:5000/`

## Environment Variables

Copy `.env.example` to `.env` and set your secret key.

## Project Structure

- `app.py`: Main Flask application
- `templates/`: HTML templates
- `static/`: CSS and other static files
- `uploads/`: Directory for uploaded files