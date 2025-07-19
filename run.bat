@echo off
REM MLWBD Movie Scraper - Windows Run Script

echo 🎬 Starting MLWBD Movie Scraper...

REM Check if Python is installed
python --version >nul 2>&1
if %errorlevel% neq 0 (
    echo ❌ Python is not installed. Please install Python 3.7 or higher.
    pause
    exit /b 1
)

REM Check if virtual environment exists
if not exist "venv" (
    echo 📦 Creating virtual environment...
    python -m venv venv
)

REM Activate virtual environment
echo 🔧 Activating virtual environment...
call venv\Scripts\activate.bat

REM Install dependencies
echo 📥 Installing dependencies...
pip install -r requirements.txt

REM Run the application
echo 🚀 Starting Flask application...
echo 📱 Open your browser and go to: http://localhost:5000
echo ⏹️  Press Ctrl+C to stop the server

python app.py
