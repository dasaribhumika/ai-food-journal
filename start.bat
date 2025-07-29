@echo off
echo 🚀 Starting AI Food Journal Application...

REM Check if virtual environment exists
if not exist "venv" (
    echo 📦 Creating virtual environment...
    python -m venv venv
)

REM Activate virtual environment
echo 🔧 Activating virtual environment...
call venv\Scripts\activate.bat

REM Install dependencies
echo 📚 Installing dependencies...
pip install -r requirements.txt

REM Check if .env file exists
if not exist ".env" (
    echo ⚠️  No .env file found. Creating template...
    (
        echo # API Keys (optional but recommended for full functionality
        echo OPENAI_API_KEY=your-openai-api-key-here
        echo GROQ_API_KEY=your-groq-api-key-here
    ) > .env
    echo 📝 Please edit .env file with your API keys
)

REM Start the application
echo 🌟 Launching application...
echo 📱 Application will be available at: http://localhost:8501
echo.
echo Press Ctrl+C to stop the application
echo.

streamlit run app.py --server.address=0.0.0.0 --server.port=8501

pause 