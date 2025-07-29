import pandas as pd
import json
import os
from datetime import datetime, date, timedelta
from typing import List, Dict, Any, Optional
import openai
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

def parse_oura_csv(file_path: str) -> pd.DataFrame:
    """Parse OURA CSV file and return a cleaned DataFrame."""
    try:
        # Read CSV file
        df = pd.read_csv(file_path)
        
        # Standardize column names (OURA exports can have different formats)
        column_mapping = {
            'Date': 'date',
            'Sleep Score': 'sleep_score',
            'Sleep Duration': 'sleep_duration',
            'Sleep Efficiency': 'sleep_efficiency',
            'Sleep Latency': 'sleep_latency',
            'Sleep Timing': 'sleep_timing',
            'Sleep Timing Score': 'sleep_timing_score',
            'Sleep Regularity': 'sleep_regularity',
            'Sleep Regularity Score': 'sleep_regularity_score',
            'Sleep Restfulness': 'sleep_restfulness',
            'Sleep Restfulness Score': 'sleep_restfulness_score',
            'Sleep Rem Sleep': 'rem_sleep',
            'Sleep Deep Sleep': 'deep_sleep',
            'Sleep Light Sleep': 'light_sleep',
            'Sleep Awake': 'awake',
            'Sleep In Bed': 'in_bed',
            'Sleep Out Of Bed': 'out_of_bed',
            'Readiness Score': 'readiness_score',
            'Activity Score': 'activity_score',
            'Activity Calories': 'activity_calories',
            'Activity Steps': 'activity_steps',
            'Activity Rest': 'activity_rest',
            'Activity Low': 'activity_low',
            'Activity Medium': 'activity_medium',
            'Activity High': 'activity_high',
            'Activity Target': 'activity_target',
            'Activity Average Heart Rate': 'avg_heart_rate',
            'Activity Heart Rate Variability': 'hrv'
        }
        
        # Rename columns if they exist
        existing_columns = {col: column_mapping[col] for col in df.columns if col in column_mapping}
        df = df.rename(columns=existing_columns)
        
        # Convert date column to datetime
        if 'date' in df.columns:
            df['date'] = pd.to_datetime(df['date'])
        
        # Convert numeric columns
        numeric_columns = ['sleep_score', 'sleep_duration', 'sleep_efficiency', 'sleep_latency',
                          'readiness_score', 'activity_score', 'activity_calories', 'activity_steps',
                          'avg_heart_rate', 'hrv']
        
        for col in numeric_columns:
            if col in df.columns:
                df[col] = pd.to_numeric(df[col], errors='coerce')
        
        # Calculate sleep hours from duration (if in minutes)
        if 'sleep_duration' in df.columns:
            # Convert minutes to hours
            df['sleep_hours'] = df['sleep_duration'] / 60
        
        return df
    
    except Exception as e:
        raise Exception(f"Error parsing OURA CSV: {str(e)}")

def get_oura_summary_stats(df: pd.DataFrame) -> Dict[str, Any]:
    """Calculate summary statistics for OURA data."""
    stats = {}
    
    if 'sleep_score' in df.columns:
        stats['avg_sleep_score'] = df['sleep_score'].mean()
        stats['best_sleep_score'] = df['sleep_score'].max()
        stats['worst_sleep_score'] = df['sleep_score'].min()
    
    if 'sleep_hours' in df.columns:
        stats['avg_sleep_hours'] = df['sleep_hours'].mean()
        stats['total_sleep_hours'] = df['sleep_hours'].sum()
        stats['best_sleep_night'] = df.loc[df['sleep_hours'].idxmax(), 'date'] if not df.empty else None
    
    if 'readiness_score' in df.columns:
        stats['avg_readiness'] = df['readiness_score'].mean()
        stats['best_readiness'] = df['readiness_score'].max()
    
    if 'activity_score' in df.columns:
        stats['avg_activity'] = df['activity_score'].mean()
        stats['total_steps'] = df['activity_steps'].sum() if 'activity_steps' in df.columns else 0
    
    return stats

def generate_oura_insights(oura_data: pd.DataFrame, food_entries: List[Dict[str, Any]] = None) -> str:
    """Generate AI insights using GROQ based on OURA data and optionally food journal entries."""
    if oura_data.empty:
        return "No OURA data found to analyze."
    
    # Set up GROQ client
    api_key = os.getenv('GROQ_API_KEY')
    if not api_key:
        return "GROQ API key not found. Please set GROQ_API_KEY environment variable."

    client = openai.OpenAI(
        api_key=api_key,
        base_url="https://api.groq.com/openai/v1"
    )
    
    # Prepare OURA data for analysis
    oura_summary = get_oura_summary_stats(oura_data)
    
    # Create analysis prompt
    prompt = f"""
    Analyze the following OURA sleep and activity data and provide insights about sleep quality, activity patterns, and health recommendations:

    OURA Data Summary:
    {json.dumps(oura_summary, indent=2)}

    Key Metrics:
    - Average Sleep Duration: {oura_summary.get('avg_sleep_duration', 'N/A')} hours
    - Average Sleep Efficiency: {oura_summary.get('avg_sleep_efficiency', 'N/A')}%
    - Average Readiness Score: {oura_summary.get('avg_readiness', 'N/A')}
    - Average Activity Level: {oura_summary.get('avg_activity', 'N/A')}
    - Average Steps: {oura_summary.get('avg_steps', 'N/A')}

    Please provide insights on:
    1. Sleep quality patterns and potential improvements
    2. Activity level recommendations
    3. Readiness score interpretation
    4. Sleep hygiene suggestions
    5. Overall health optimization tips

    Format your response in a clear, actionable way with specific recommendations.
    """
    
    # Add food journal correlation if available
    if food_entries:
        prompt += f"""

    Additionally, analyze correlations with food journal entries:
    {json.dumps(food_entries[:10], indent=2)}  # Show last 10 entries

    Please also consider:
    6. How meal timing might affect sleep quality
    7. Food choices that could impact sleep
    8. Recommendations for better sleep through diet
    """
    
    try:
        response = client.chat.completions.create(
            model="llama3-70b-8192",
            messages=[
                {"role": "system", "content": "You are a sleep and health expert analyzing OURA ring data to provide actionable insights for better sleep and overall health."},
                {"role": "user", "content": prompt}
            ],
            max_tokens=1000,
            temperature=0.7
        )
        
        return response.choices[0].message.content
    
    except Exception as e:
        return f"Error generating OURA insights: {str(e)}"

def save_oura_insight(insight_content: str, oura_data_points: int, food_entries_count: int) -> None:
    """Save OURA insight to JSON file."""
    insight = {
        'content': insight_content,
        'source': 'oura_sleep',
        'timestamp': datetime.now().isoformat(),
        'oura_data_points': oura_data_points,
        'food_entries_analyzed': food_entries_count,
        'analysis_type': 'OURA Sleep & Food Correlation'
    }
    
    # Load existing insights
    insights_file = "insights.json"
    insights = []
    
    if os.path.exists(insights_file):
        try:
            with open(insights_file, 'r') as f:
                insights = json.load(f)
        except (json.JSONDecodeError, FileNotFoundError):
            insights = []
    
    # Add new insight
    insights.append(insight)
    
    # Save back to file
    with open(insights_file, 'w') as f:
        json.dump(insights, f, indent=2)

def get_oura_insights() -> List[Dict[str, Any]]:
    """Get all OURA-related insights."""
    insights_file = "insights.json"
    
    if not os.path.exists(insights_file):
        return []
    
    try:
        with open(insights_file, 'r') as f:
            all_insights = json.load(f)
        
        # Filter for OURA insights
        oura_insights = [insight for insight in all_insights if insight.get('source') == 'oura_sleep']
        return oura_insights
    except (json.JSONDecodeError, FileNotFoundError):
        return []

def format_oura_insight_for_display(insight: Dict[str, Any]) -> str:
    """Format an OURA insight for display."""
    timestamp = datetime.fromisoformat(insight['timestamp'])
    date_str = timestamp.strftime("%B %d, %Y at %I:%M %p")
    
    return f"📊 OURA Analysis - {date_str}\n{insight.get('content', 'No content')}"

def create_sleep_food_correlation_data(oura_data: pd.DataFrame, food_entries: List[Dict[str, Any]]) -> pd.DataFrame:
    """Create a DataFrame for correlation analysis between sleep and food data."""
    correlation_data = []
    
    for _, oura_row in oura_data.iterrows():
        oura_date = oura_row['date'].date() if pd.notna(oura_row['date']) else None
        
        if oura_date:
            # Find food entries for the same date
            day_food_entries = []
            for food_entry in food_entries:
                food_date = datetime.fromisoformat(food_entry['timestamp']).date()
                if food_date == oura_date:
                    day_food_entries.append(food_entry)
            
            # Create correlation entry
            correlation_entry = {
                'date': oura_date,
                'sleep_score': oura_row.get('sleep_score'),
                'sleep_hours': oura_row.get('sleep_hours'),
                'readiness_score': oura_row.get('readiness_score'),
                'activity_score': oura_row.get('activity_score'),
                'meals_count': len(day_food_entries),
                'late_meals': len([e for e in day_food_entries if e.get('meal_time', '') > '20:00']),
                'symptoms_reported': any(e.get('symptoms') for e in day_food_entries),
                'supplements_taken': any(e.get('supplements') for e in day_food_entries)
            }
            
            correlation_data.append(correlation_entry)
    
    return pd.DataFrame(correlation_data) 