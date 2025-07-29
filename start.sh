#!/bin/bash

# AI Food Journal Startup Script
echo "🚀 Starting AI Food Journal Application..."

# Check if virtual environment exists
if [ ! -d "venv" ]; then
    echo "📦 Creating virtual environment..."
    python3 -m venv venv
fi

# Activate virtual environment
echo "🔧 Activating virtual environment..."
source venv/bin/activate

# Install dependencies
echo "📚 Installing dependencies..."
pip install -r requirements.txt

# Check if .env file exists
if [ ! -f ".env" ]; then
    echo "⚠️  No .env file found. Creating template..."
    cat > .env << EOF
# API Keys (optional but recommended for full functionality)
OPENAI_API_KEY=your-openai-api-key-here
GROQ_API_KEY=your-groq-api-key-here
EOF
    echo "📝 Please edit .env file with your API keys"
fi

# Start the application
echo "🌟 Launching application..."
echo "📱 Application will be available at: http://localhost:8501"
echo "🌐 To access from other devices, use: http://$(hostname -I | awk '{print $1}'):8501"
echo ""
echo "Press Ctrl+C to stop the application"
echo ""

streamlit run app.py --server.address=0.0.0.0 --server.port=8501 