# 🍎 AI Food Journal

A comprehensive Streamlit application for logging food, meal times, supplements, and symptoms with AI-powered insights using GPT-4.

## Features

### 📝 Food Journal
- **Meal Logging**: Log breakfast, lunch, dinner, snacks, and other meals
- **Food Items**: Track individual food items (one per line)
- **Supplements**: Record supplements taken with meals
- **Symptoms**: Log any symptoms experienced (bloating, fatigue, etc.)
- **Notes**: Add additional observations and notes
- **Meal Time**: Record exact meal timing

### 🤖 AI Insights
- **Pattern Detection**: GPT-4 analyzes your food journal data
- **Trigger Identification**: Detect potential food triggers for symptoms
- **Recommendations**: Get personalized dietary recommendations
- **Trend Analysis**: Identify meal timing patterns and their effects
- **Supplement Analysis**: Track supplement effectiveness

### 📊 OURA Sleep & Activity Analysis
- **CSV Upload**: Upload YOURA ring data exports
- **Sleep Analysis**: Track sleep hours, efficiency, and quality scores
- **Activity Tracking**: Monitor readiness, activity levels, and heart rate
- **Food Correlation**: Compare sleep patterns with food journal entries
- **AI Insights**: Generate insights like "sleep affected by late meals"
- **Visual Charts**: Interactive charts for sleep and activity trends

### 📋 Task Manager
- **Task Creation**: Add tasks with categories (Work, Health, Personal)
- **Priority Management**: Set High, Medium, Low priorities
- **Due Date Tracking**: Set and track due dates
- **Task Completion**: Mark tasks as complete with timestamps
- **Smart Organization**: Today's tasks, upcoming tasks, overdue tasks
- **AI Insights**: Generate productivity insights using GROQ
- **Statistics**: Track completion rates and productivity patterns

### 🎯 Goal Tracker
- **Goal Creation**: Add goals with Daily, Weekly, Monthly timeframes
- **Priority Setting**: Set High, Medium, Low priority levels
- **Deadline Tracking**: Set specific deadlines for each goal
- **Progress Visualization**: Progress bars for completion rates
- **Smart Organization**: Today's goals, weekly goals, monthly goals, overdue goals
- **AI Insights**: Generate motivational insights and detect missing goals using GROQ
- **Statistics**: Track completion rates by timeframe

### 🍽️ Meal Planning
- **Weekly Meal Plans**: Plan breakfast, lunch, and dinner for each day
- **Recipe Book**: Create and manage recipes with ingredients and steps
- **Grocery List Generation**: Automatically generate shopping lists from meal plans
- **AI Recommendations**: Get personalized meal suggestions based on food journal data
- **Search Functionality**: Search recipes by title or ingredients
- **Meal Statistics**: Track total plans, meals, and recipes used

### 🧘‍♀️ Self-Care Scheduler
- **Recurring Tasks**: Schedule daily, weekly, or monthly self-care routines
- **Category Organization**: Grooming, cleaning, health, wellness, laundry, hygiene
- **Time Scheduling**: Set specific times for each self-care activity
- **Completion Tracking**: Mark tasks as done with timestamps
- **Overdue Detection**: Identify missed routines and overdue tasks
- **AI Insights**: Analyze patterns and suggest routine improvements using GROQ
- **Statistics**: Track completion rates and routine consistency

### 📊 Analytics
- **Date Range Analysis**: View entries within custom date ranges
- **Summary Statistics**: Track total entries, unique foods, symptoms, and supplements
- **Trend Visualization**: Identify patterns in your eating habits

## 🚀 Quick Start

### Option 1: Easy Startup Scripts

**For Mac/Linux:**
```bash
./start.sh
```

**For Windows:**
```bash
start.bat
```

### Option 2: Manual Setup

1. **Install Dependencies:**
   ```bash
   pip install -r requirements.txt
   ```

2. **Set Up API Keys (Optional but Recommended):**
   Create a `.env` file in the project root:
   ```bash
   OPENAI_API_KEY=your_openai_api_key_here
   GROQ_API_KEY=your_groq_api_key_here
   ```

   You can get API keys from:
   - [OpenAI's platform](https://platform.openai.com/api-keys) for food and OURA insights
   - [GROQ's platform](https://console.groq.com/keys) for task management insights

3. **Run the Application:**
   ```bash
   streamlit run app.py
   ```

   The application will open in your browser at `http://localhost:8501`.

### 🌐 Deployment

For hosting the application, see [DEPLOYMENT.md](DEPLOYMENT.md) for detailed instructions on deploying to:
- Streamlit Cloud (Recommended)
- Heroku
- Railway
- Local Network Sharing

## Usage Guide

### Logging Food Entries

1. **Navigate to Food Journal**: Use the sidebar to select "Food Journal"
2. **Fill in Meal Information**:
   - Select meal type (Breakfast, Lunch, Dinner, Snack, Other)
   - Enter food items (one per line)
   - Add supplements if taken
3. **Add Health Information**:
   - Log any symptoms experienced
   - Add additional notes
   - Set meal time
4. **Save Entry**: Click "💾 Save Entry" to save your entry

### Generating AI Insights

1. **Add Entries**: Log several meals over time to build data
2. **Generate Insights**: Click "🔍 Generate AI Insights" button
3. **Review Analysis**: The AI will analyze your patterns and provide recommendations
4. **View Past Insights**: Scroll down to see previously generated insights

### OURA Sleep Analysis

1. **Export Data**: Export your OURA ring data as CSV from the OURA app
2. **Upload File**: Go to "OURA Analysis" page and upload your CSV file
3. **View Statistics**: See summary statistics and interactive charts
4. **Generate Insights**: Click "Generate OURA + Food Insights" for correlation analysis
5. **Compare Data**: View how your sleep patterns correlate with food choices

### Task Management

1. **Add Tasks**: Go to "Task Manager" page and create new tasks
2. **Set Categories**: Choose Work, Health, or Personal categories
3. **Set Priorities**: Assign High, Medium, or Low priority levels
4. **Track Progress**: View today's tasks, upcoming tasks, and overdue tasks
5. **Generate Insights**: Click "Generate Task Insights" for AI-powered productivity analysis

### Goal Tracking

1. **Add Goals**: Go to "Goal Tracker" page and create new goals
2. **Set Timeframes**: Choose Daily, Weekly, or Monthly timeframes
3. **Set Deadlines**: Assign specific deadlines for each goal
4. **Track Progress**: View today's goals, weekly goals, monthly goals, and overdue goals
5. **Generate Insights**: Click "Generate Goal Insights" for motivational analysis and missing goal detection

### Meal Planning

1. **Create Meal Plans**: Go to "Meal Planning" page and plan weekly meals
2. **Add Recipes**: Create recipes with ingredients and cooking steps
3. **Generate Grocery Lists**: Automatically create shopping lists from meal plans
4. **Get AI Recommendations**: Generate personalized meal suggestions based on food journal data
5. **Search Recipes**: Find recipes by title or ingredients

### Self-Care Scheduling

1. **Add Self-Care Tasks**: Go to "Self-Care" page and create recurring routines
2. **Set Frequencies**: Choose daily, weekly, or monthly schedules
3. **Schedule Times**: Set specific times for each self-care activity
4. **Track Completion**: Mark tasks as done and monitor progress
5. **Get AI Insights**: Generate routine analysis and improvement suggestions

### Analytics

1. **Navigate to Analytics**: Use the sidebar to select "Analytics"
2. **Select Date Range**: Choose start and end dates for analysis
3. **Review Statistics**: View summary metrics and detailed entries

## Data Storage

- **Food Journal Data**: Stored in `food_journal.json`
- **AI Insights**: Stored in `insights.json`
- **Local Storage**: All data is stored locally on your machine

## File Structure

```
ai-food-journal/
├── app.py                 # Main Streamlit application
├── requirements.txt       # Python dependencies
├── README.md             # This file
├── .env                  # Environment variables (create this)
├── food_journal.json     # Food journal data (auto-created)
├── insights.json         # AI insights data (auto-created)
├── goals.json           # Goal tracking data (auto-created)
├── tasks.json           # Task management data (auto-created)
├── meal_plans.json     # Meal planning data (auto-created)
├── recipes.json        # Recipe book data (auto-created)
├── selfcare_tasks.json # Self-care scheduling data (auto-created)
├── sample_oura_data.csv  # Sample OURA data for testing
└── utils/
    ├── data_utils.py     # Data management utilities
    ├── insight_utils.py  # AI insight generation utilities
    ├── oura_utils.py     # OURA data parsing and analysis utilities
    ├── task_utils.py     # Task management utilities
    ├── goal_utils.py     # Goal tracking utilities
    ├── meal_utils.py     # Meal planning utilities
    └── selfcare_utils.py # Self-care scheduling utilities
```

## Features in Detail

### Food Journal Page
- **Two-column layout** for easy data entry
- **Real-time validation** ensures required fields are filled
- **Today's entries display** shows all entries for the current day
- **Formatted entry cards** with emojis and clear organization

### AI Insights Generation
- **GPT-4 Analysis**: Uses OpenAI's GPT-4 model for intelligent analysis
- **Pattern Recognition**: Identifies correlations between food and symptoms
- **Actionable Recommendations**: Provides specific dietary advice
- **Historical Tracking**: Saves insights for future reference

### Analytics Dashboard
- **Custom Date Ranges**: Analyze data from specific time periods
- **Summary Metrics**: Quick overview of eating patterns
- **Detailed Views**: Complete entry history with formatting

## Troubleshooting

### Common Issues

1. **OpenAI API Key Error**
   - Ensure your `.env` file contains the correct API key
   - Verify the API key is valid and has sufficient credits

2. **Missing Dependencies**
   - Run `pip install -r requirements.txt` to install all required packages

3. **Data Not Saving**
   - Check file permissions in the project directory
   - Ensure the application has write access to create JSON files

### Getting Help

- Check that all dependencies are installed correctly
- Verify your OpenAI API key is valid and has credits
- Ensure you have internet connection for AI insights generation

## Privacy & Security

- **Local Storage**: All data is stored locally on your machine
- **No Cloud Storage**: Your food journal data never leaves your computer
- **API Key Security**: Store your OpenAI API key in the `.env` file (not in code)

## Future Enhancements

- Export functionality for data backup
- More detailed analytics and visualizations
- Integration with health tracking devices
- Meal planning recommendations
- Nutritional information lookup

---

**Note**: This application requires an OpenAI API key for AI insights generation. The basic food journal functionality works without the API key, but AI insights will not be available. 