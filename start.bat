@echo off
echo 🍎 Setting up AI Food Journal...

REM Check if Python is installed
python --version >nul 2>&1
if errorlevel 1 (
    echo ❌ Python is not installed. Please install Python first.
    pause
    exit /b 1
)

REM Create virtual environment if it doesn't exist
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

REM Create .env file if it doesn't exist
if not exist ".env" (
    echo 🔑 Creating .env file...
    (
        echo # GROQ API Key ^(get from https://console.groq.com/^)
        echo GROQ_API_KEY=your-groq-api-key-here
        echo.
        echo # Optional: Add your GROQ API key here for AI features
        echo # GROQ_API_KEY=your-actual-groq-api-key
    ) > .env
    echo ✅ .env file created! Please edit it to add your GROQ API key.
)

echo 🚀 Starting the application...
echo 📱 The app will open in your browser at http://localhost:8501
echo 🔑 Don't forget to add your GROQ API key to the .env file for AI features!
echo.

REM Start Streamlit
streamlit run app.py 