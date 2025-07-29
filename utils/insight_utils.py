import json
import os
from datetime import datetime
from typing import List, Dict, Any
import openai
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

# File paths
INSIGHTS_FILE = "insights.json"

def save_insight(insight: Dict[str, Any]) -> None:
    """Save an insight to JSON file."""
    # Add timestamp if not present
    if 'timestamp' not in insight:
        insight['timestamp'] = datetime.now().isoformat()
    
    # Load existing insights
    insights = load_insights()
    
    # Add new insight
    insights.append(insight)
    
    # Save back to file
    with open(INSIGHTS_FILE, 'w') as f:
        json.dump(insights, f, indent=2)

def load_insights() -> List[Dict[str, Any]]:
    """Load all insights from JSON file."""
    if not os.path.exists(INSIGHTS_FILE):
        return []
    
    try:
        with open(INSIGHTS_FILE, 'r') as f:
            return json.load(f)
    except (json.JSONDecodeError, FileNotFoundError):
        return []

def generate_ai_insights(entries: List[Dict[str, Any]]) -> str:
    """Generate AI insights using GROQ based on food journal entries."""
    if not entries:
        return "No entries found to analyze."
    
    # Set up GROQ client
    api_key = os.getenv('GROQ_API_KEY')
    if not api_key:
        return "GROQ API key not found. Please set GROQ_API_KEY environment variable."

    client = openai.OpenAI(
        api_key=api_key,
        base_url="https://api.groq.com/openai/v1"
    )
    
    # Prepare the data for analysis
    analysis_data = []
    for entry in entries:
        # Use meal_time if available, otherwise fall back to timestamp
        if 'meal_time' in entry and entry['meal_time']:
            meal_time = entry['meal_time']
        else:
            meal_time = datetime.fromisoformat(entry['timestamp']).strftime('%H:%M')
        
        analysis_entry = {
            'date': datetime.fromisoformat(entry['timestamp']).strftime('%Y-%m-%d'),
            'time': meal_time,
            'meal_type': entry.get('meal_type', 'Unknown'),
            'food_items': entry.get('food_items', []),
            'supplements': entry.get('supplements', []),
            'symptoms': entry.get('symptoms', [])
        }
        analysis_data.append(analysis_entry)
    
    # Create prompt for GROQ
    prompt = f"""
    Analyze the following food journal entries and provide insights about potential patterns, triggers, and recommendations:

    {json.dumps(analysis_data, indent=2)}

    Note: The 'time' field represents when the meal was actually consumed (not when it was logged).

    Please provide insights on:
    1. Potential food triggers for symptoms (especially bloating, digestive issues)
    2. Meal timing patterns and their effects (analyze if meal times are realistic and well-spaced)
    3. Supplement effectiveness
    4. Dietary patterns and recommendations
    5. Any correlations between food choices and symptoms
    6. Meal timing recommendations (optimal spacing between meals)

    Format your response in a clear, actionable way with specific recommendations.
    """
    
    try:
        response = client.chat.completions.create(
            model="llama3-70b-8192",
            messages=[
                {"role": "system", "content": "You are a nutrition and health expert analyzing food journal data to identify patterns and provide actionable insights."},
                {"role": "user", "content": prompt}
            ],
            max_tokens=1000,
            temperature=0.7
        )
        
        return response.choices[0].message.content
    
    except Exception as e:
        return f"Error generating insights: {str(e)}"

def format_insight_for_display(insight: Dict[str, Any]) -> str:
    """Format an insight for display."""
    timestamp = datetime.fromisoformat(insight['timestamp'])
    date_str = timestamp.strftime("%B %d, %Y at %I:%M %p")
    
    return f"📊 {date_str}\n{insight.get('content', 'No content')}"

def get_recent_insights(limit: int = 5) -> List[Dict[str, Any]]:
    """Get the most recent insights."""
    insights = load_insights()
    # Sort by timestamp (newest first) and return limited results
    sorted_insights = sorted(insights, key=lambda x: x.get('timestamp', ''), reverse=True)
    return sorted_insights[:limit]
