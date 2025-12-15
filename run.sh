#!/bin/bash
# MediConnectPro Startup Script

# Create virtual environment if it doesn't exist
if [ ! -d "venv" ]; then
    echo "Creating virtual environment..."
    python -m venv venv
fi

# Activate virtual environment
source venv/bin/activate

# Install requirements
echo "Installing dependencies..."
pip install -r requirements.txt

# Create .env if it doesn't exist
if [ ! -f ".env" ]; then
    echo "Creating .env from .env.example..."
    cp .env.example .env
    echo "Please edit .env with your database credentials"
fi

# Run migrations if available
# alembic upgrade head

# Start the server
echo "Starting MediConnectPro API..."
uvicorn app.main:app --reload --host 0.0.0.0 --port 8000
