# Document Generator Web System

A lightweight web application built with Python FastAPI for generating formatted documents.

## Features
- **Database Support**: Choose between SQLite (default) or MySQL
- **Template Options**: Select from three LaTeX templates
- **Web Interface**: User-friendly UI for configuration and generation

## Quick Start

1. Install dependencies:
```bash
pip install -r requirements.txt
```

2. Run the application:
```bash
python resume.app.py
```

3. Access the web interface at `http://localhost:8000`

## Configuration
- Select database type (SQLite/MySQL) via web interface
- Configure connection settings as needed

The system automatically handles database setup and document generation based on your selections.