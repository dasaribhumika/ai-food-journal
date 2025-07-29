# 🚀 Quick Start Guide

## Get Started in 3 Steps

### 1. Activate Virtual Environment
```bash
source venv/bin/activate
```

### 2. Set Up OpenAI API Key (Optional)
Create a `.env` file in the project root:
```
OPENAI_API_KEY=your_openai_api_key_here
```

**Note**: The basic food journal works without the API key, but AI insights require it.

### 3. Run the Application
```bash
streamlit run app.py
```

The application will open in your browser at `http://localhost:8501`

## What You Can Do

### 📝 Log Your Meals
- Select meal type (Breakfast, Lunch, Dinner, Snack)
- Enter food items (one per line)
- Add supplements and symptoms
- Set meal time
- Add notes

### 🤖 Generate AI Insights
- Log several meals over time
- Click "Generate AI Insights" button
- Get personalized recommendations
- View pattern analysis

### 📊 OURA Sleep Analysis
- Upload YOURA ring data CSV exports
- View sleep hours, readiness, and activity scores
- Generate insights comparing sleep with food patterns
- Track correlations like "sleep affected by late meals"

### 📋 Task Management
- Add tasks with categories (Work, Health, Personal)
- Set priorities (High, Medium, Low)
- Track due dates and completion status
- View today's tasks, upcoming tasks, and overdue tasks
- Generate AI insights for productivity optimization

### 🎯 Goal Tracking
- Add goals with timeframes (Daily, Weekly, Monthly)
- Set priorities and specific deadlines
- Track progress with visual progress bars
- View today's goals, weekly goals, monthly goals, and overdue goals
- Generate motivational insights and detect missing goals

### 🍽️ Meal Planning
- Plan weekly meals (breakfast, lunch, dinner)
- Create and manage recipes with ingredients and steps
- Generate grocery lists automatically from meal plans
- Get AI-powered meal recommendations based on food journal data
- Search recipes by title or ingredients

### 🧘‍♀️ Self-Care Scheduling
- Schedule recurring self-care routines (daily, weekly, monthly)
- Organize tasks by category (grooming, cleaning, health, wellness)
- Set specific times for each self-care activity
- Track completion and monitor overdue tasks
- Get AI insights for routine improvement

### 📊 View Analytics
- Select date ranges
- View summary statistics
- Track eating patterns

## Data Storage
- All data is stored locally in JSON files
- No cloud storage or external services (except OpenAI for insights)
- Your data stays private on your machine

## Troubleshooting
- **API Key Issues**: Make sure your `.env` file is in the project root
- **Import Errors**: Ensure you're in the virtual environment
- **Port Issues**: The app runs on port 8501 by default

---

**Ready to start?** Run `streamlit run app.py` and begin logging your meals! 🍎 