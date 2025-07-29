#!/bin/bash

echo "🍎 Setting up AI Food Journal..."

# Check if Python 3 is installed
if ! command -v python3 &> /dev/null; then
    echo "❌ Python 3 is not installed. Please install Python 3 first."
    exit 1
fi

# Create virtual environment if it doesn't exist
if [ ! -d "venv" ]; then
    echo "📦 Creating virtual environment..."
    python3 -m venv venv
fi

# Activate virtual environment
echo "🔧 Activating virtual environment..."
source venv/bin/activate

# Install dependencies
echo "📥 Installing dependencies..."
pip install -r requirements.txt

# Create .env file if it doesn't exist
if [ ! -f ".env" ]; then
    echo "🔑 Creating .env file..."
    cat > .env << EOF
# GROQ API Key (get from https://console.groq.com/)
GROQ_API_KEY=your-groq-api-key-here

# Optional: Add your GROQ API key here for AI features
# GROQ_API_KEY=your-actual-groq-api-key
EOF
    echo "✅ .env file created! Please edit it to add your GROQ API key."
fi

echo "🚀 Starting the application..."
echo "📱 The app will open in your browser at http://localhost:8501"
echo "🔑 Don't forget to add your GROQ API key to the .env file for AI features!"
echo ""

# Start Streamlit
streamlit run app.py 