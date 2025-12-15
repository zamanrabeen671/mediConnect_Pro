@echo off
REM MediConnectPro Startup Script for Windows

REM Create virtual environment if it doesn't exist
if not exist "venv" (
    echo Creating virtual environment...
    python -m venv venv
)

REM Activate virtual environment
call venv\Scripts\activate

REM Install requirements
echo Installing dependencies...
pip install -r requirements.txt

REM Create .env if it doesn't exist
if not exist ".env" (
    echo Creating .env from .env.example...
    copy .env.example .env
    echo Please edit .env with your database credentials
)

REM Start the server
echo Starting MediConnectPro API...
uvicorn app.main:app --reload --host 0.0.0.0 --port 8000
