import json
import os
from datetime import datetime, date, timedelta
from typing import List, Dict, Any, Optional
import openai
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

# File paths
GOALS_FILE = "goals.json"

def save_goal(goal: Dict[str, Any]) -> None:
    """Save a goal to JSON file."""
    # Add timestamp if not present
    if 'created_at' not in goal:
        goal['created_at'] = datetime.now().isoformat()
    
    # Load existing goals
    goals = load_goals()
    
    # Add new goal
    goals.append(goal)
    
    # Save back to file
    with open(GOALS_FILE, 'w') as f:
        json.dump(goals, f, indent=2)

def load_goals() -> List[Dict[str, Any]]:
    """Load all goals from JSON file."""
    if not os.path.exists(GOALS_FILE):
        return []
    
    try:
        with open(GOALS_FILE, 'r') as f:
            return json.load(f)
    except (json.JSONDecodeError, FileNotFoundError):
        return []

def get_todays_goals() -> List[Dict[str, Any]]:
    """Get all goals due today."""
    goals = load_goals()
    today = date.today()
    
    todays_goals = []
    for goal in goals:
        if goal.get('deadline'):
            try:
                deadline = datetime.fromisoformat(goal['deadline']).date()
                if deadline == today:
                    todays_goals.append(goal)
            except (ValueError, TypeError):
                continue
    
    return todays_goals

def get_weekly_goals() -> List[Dict[str, Any]]:
    """Get all goals due this week."""
    goals = load_goals()
    today = date.today()
    week_end = today + timedelta(days=7)
    
    weekly_goals = []
    for goal in goals:
        if goal.get('deadline'):
            try:
                deadline = datetime.fromisoformat(goal['deadline']).date()
                if today <= deadline <= week_end:
                    weekly_goals.append(goal)
            except (ValueError, TypeError):
                continue
    
    return weekly_goals

def get_monthly_goals() -> List[Dict[str, Any]]:
    """Get all goals due this month."""
    goals = load_goals()
    today = date.today()
    month_end = today.replace(day=28) + timedelta(days=4)
    month_end = month_end.replace(day=1) - timedelta(days=1)
    
    monthly_goals = []
    for goal in goals:
        if goal.get('deadline'):
            try:
                deadline = datetime.fromisoformat(goal['deadline']).date()
                if today <= deadline <= month_end:
                    monthly_goals.append(goal)
            except (ValueError, TypeError):
                continue
    
    return monthly_goals

def get_overdue_goals() -> List[Dict[str, Any]]:
    """Get overdue goals."""
    goals = load_goals()
    today = date.today()
    
    overdue_goals = []
    for goal in goals:
        if goal.get('deadline') and not goal.get('completed', False):
            try:
                deadline = datetime.fromisoformat(goal['deadline']).date()
                if deadline < today:
                    overdue_goals.append(goal)
            except (ValueError, TypeError):
                continue
    
    return overdue_goals

def mark_goal_complete(goal_id: str) -> bool:
    """Mark a goal as complete."""
    goals = load_goals()
    
    for goal in goals:
        if goal.get('id') == goal_id:
            goal['completed'] = True
            goal['completed_at'] = datetime.now().isoformat()
            
            # Save updated goals
            with open(GOALS_FILE, 'w') as f:
                json.dump(goals, f, indent=2)
            
            return True
    
    return False

def delete_goal(goal_id: str) -> bool:
    """Delete a goal."""
    goals = load_goals()
    
    for i, goal in enumerate(goals):
        if goal.get('id') == goal_id:
            del goals[i]
            
            # Save updated goals
            with open(GOALS_FILE, 'w') as f:
                json.dump(goals, f, indent=2)
            
            return True
    
    return False

def get_goal_statistics() -> Dict[str, Any]:
    """Get goal completion statistics."""
    goals = load_goals()
    
    if not goals:
        return {
            'total_goals': 0,
            'completed_goals': 0,
            'pending_goals': 0,
            'overdue_goals': 0,
            'completion_rate': 0.0,
            'daily_goals': 0,
            'weekly_goals': 0,
            'monthly_goals': 0
        }
    
    total_goals = len(goals)
    completed_goals = len([g for g in goals if g.get('completed', False)])
    pending_goals = total_goals - completed_goals
    overdue_goals = len(get_overdue_goals())
    
    completion_rate = (completed_goals / total_goals) * 100 if total_goals > 0 else 0
    
    # Count by timeframe
    daily_goals = len([g for g in goals if g.get('timeframe') == 'Daily'])
    weekly_goals = len([g for g in goals if g.get('timeframe') == 'Weekly'])
    monthly_goals = len([g for g in goals if g.get('timeframe') == 'Monthly'])
    
    return {
        'total_goals': total_goals,
        'completed_goals': completed_goals,
        'pending_goals': pending_goals,
        'overdue_goals': overdue_goals,
        'completion_rate': completion_rate,
        'daily_goals': daily_goals,
        'weekly_goals': weekly_goals,
        'monthly_goals': monthly_goals
    }

def generate_goal_insights(goals: List[Dict[str, Any]]) -> str:
    """Generate AI insights for goal management using GROQ."""
    if not goals:
        return "No goals found to analyze."
    
    # Set up GROQ client
    api_key = os.getenv('GROQ_API_KEY')
    if not api_key:
        return "GROQ API key not found. Please set GROQ_API_KEY environment variable."
    
    client = openai.OpenAI(
        api_key=api_key,
        base_url="https://api.groq.com/openai/v1"
    )
    
    # Prepare goal data for analysis
    goal_analysis = []
    for goal in goals:
        goal_entry = {
            'title': goal.get('title', 'Unknown'),
            'description': goal.get('description', ''),
            'timeframe': goal.get('timeframe', 'Unknown'),
            'deadline': goal.get('deadline', 'No deadline'),
            'completed': goal.get('completed', False),
            'created_at': goal.get('created_at', 'Unknown')
        }
        goal_analysis.append(goal_entry)
    
    # Create prompt for GROQ
    prompt = f"""
    Analyze the following goal management data and provide motivational insights and recommendations:

    GOAL DATA:
    {json.dumps(goal_analysis, indent=2)}

    Please provide insights on:
    1. Goal completion patterns and success rates
    2. Timeframe effectiveness (Daily, Weekly, Monthly goals)
    3. Motivational analysis based on goal types and completion
    4. Detection of missing or recurring goals
    5. Recommendations for better goal setting and achievement
    6. Strategies for improving goal completion rates
    7. Work-life balance insights based on goal distribution
    8. Motivational messages and encouragement

    Focus on actionable insights, motivational content, and specific recommendations.
    Format your response in a clear, structured way with bullet points for key findings.
    Include encouraging and motivational language.
    """
    
    try:
        response = client.chat.completions.create(
            model="llama3-70b-8192",  # Using GROQ's Llama model
            messages=[
                {"role": "system", "content": "You are a motivational coach and goal-setting expert analyzing goal data to provide encouraging insights and actionable advice for better goal achievement."},
                {"role": "user", "content": prompt}
            ],
            max_tokens=1200,
            temperature=0.8
        )
        
        return response.choices[0].message.content
    
    except Exception as e:
        return f"Error generating insights: {str(e)}"

def save_goal_insight(insight_content: str, goals_analyzed: int) -> None:
    """Save goal insight to JSON file."""
    insight = {
        'content': insight_content,
        'source': 'goal_tracking',
        'timestamp': datetime.now().isoformat(),
        'goals_analyzed': goals_analyzed,
        'analysis_type': 'Goal Management & Motivation'
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

def get_goal_insights() -> List[Dict[str, Any]]:
    """Get all goal-related insights."""
    insights_file = "insights.json"
    
    if not os.path.exists(insights_file):
        return []
    
    try:
        with open(insights_file, 'r') as f:
            all_insights = json.load(f)
        
        # Filter for goal insights
        goal_insights = [insight for insight in all_insights if insight.get('source') == 'goal_tracking']
        return goal_insights
    except (json.JSONDecodeError, FileNotFoundError):
        return []

def format_goal_for_display(goal: Dict[str, Any]) -> str:
    """Format a goal for display."""
    title = goal.get('title', 'No title')
    timeframe = goal.get('timeframe', 'Unknown')
    deadline = goal.get('deadline', 'No deadline')
    
    # Format deadline
    if deadline != 'No deadline':
        try:
            deadline_obj = datetime.fromisoformat(deadline)
            deadline = deadline_obj.strftime("%b %d, %Y")
        except (ValueError, TypeError):
            pass
    
    # Timeframe emoji
    timeframe_emoji = {
        'Daily': '📅',
        'Weekly': '📆',
        'Monthly': '🗓️'
    }.get(timeframe, '🎯')
    
    # Completion status
    status = "✅" if goal.get('completed', False) else "⏳"
    
    return f"{status} {timeframe_emoji} {title} (Due: {deadline})"

def calculate_goal_progress(goals: List[Dict[str, Any]]) -> float:
    """Calculate overall goal progress percentage."""
    if not goals:
        return 0.0
    
    completed = len([g for g in goals if g.get('completed', False)])
    return (completed / len(goals)) * 100

def detect_missing_goals(goals: List[Dict[str, Any]]) -> List[str]:
    """Detect potential missing or recurring goals."""
    suggestions = []
    
    # Analyze goal patterns
    daily_goals = [g for g in goals if g.get('timeframe') == 'Daily']
    weekly_goals = [g for g in goals if g.get('timeframe') == 'Weekly']
    monthly_goals = [g for g in goals if g.get('timeframe') == 'Monthly']
    
    # Check for missing timeframes
    if not daily_goals:
        suggestions.append("Consider adding daily goals for consistent progress")
    
    if not weekly_goals:
        suggestions.append("Weekly goals help with medium-term planning")
    
    if not monthly_goals:
        suggestions.append("Monthly goals provide long-term direction")
    
    # Check completion patterns
    completed_goals = [g for g in goals if g.get('completed', False)]
    if len(completed_goals) < len(goals) * 0.5:
        suggestions.append("Focus on completing existing goals before adding new ones")
    
    return suggestions 