import json
import os
from datetime import datetime, date, timedelta
from typing import List, Dict, Any, Optional
import openai
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

# File paths
SELFCARE_FILE = "selfcare_tasks.json"

def save_selfcare_task(task: Dict[str, Any]) -> None:
    """Save a self-care task to JSON file."""
    # Add timestamp if not present
    if 'created_at' not in task:
        task['created_at'] = datetime.now().isoformat()
    
    # Load existing tasks
    tasks = load_selfcare_tasks()
    
    # Add new task
    tasks.append(task)
    
    # Save back to file
    with open(SELFCARE_FILE, 'w') as f:
        json.dump(tasks, f, indent=2)

def load_selfcare_tasks() -> List[Dict[str, Any]]:
    """Load all self-care tasks from JSON file."""
    if not os.path.exists(SELFCARE_FILE):
        return []
    
    try:
        with open(SELFCARE_FILE, 'r') as f:
            return json.load(f)
    except (json.JSONDecodeError, FileNotFoundError):
        return []

def get_todays_selfcare_tasks() -> List[Dict[str, Any]]:
    """Get all tasks scheduled for today."""
    tasks = load_selfcare_tasks()
    today = date.today()
    
    todays_tasks = []
    for task in tasks:
        if task.get('frequency') == 'Daily':
            todays_tasks.append(task)
        elif task.get('frequency') == 'Weekly':
            # Check if today is the scheduled day
            if task.get('scheduled_day'):
                try:
                    scheduled_day = datetime.fromisoformat(task['scheduled_day']).date()
                    if scheduled_day == today:
                        todays_tasks.append(task)
                except (ValueError, TypeError):
                    continue
        elif task.get('frequency') == 'Monthly':
            # Check if today is the scheduled day of the month
            if task.get('scheduled_day_of_month'):
                if today.day == task['scheduled_day_of_month']:
                    todays_tasks.append(task)
    
    return todays_tasks

def get_upcoming_selfcare_tasks(days: int = 7) -> List[Dict[str, Any]]:
    """Get tasks scheduled in the next N days."""
    tasks = load_selfcare_tasks()
    today = date.today()
    end_date = today + timedelta(days=days)
    
    upcoming_tasks = []
    for task in tasks:
        next_occurrence = get_next_occurrence(task)
        if next_occurrence and today <= next_occurrence <= end_date:
            task_copy = task.copy()
            task_copy['next_occurrence'] = next_occurrence.isoformat()
            upcoming_tasks.append(task_copy)
    
    return upcoming_tasks

def get_next_occurrence(task: Dict[str, Any]) -> Optional[date]:
    """Get the next occurrence date for a task."""
    today = date.today()
    
    if task.get('frequency') == 'Daily':
        return today
    
    elif task.get('frequency') == 'Weekly':
        if task.get('scheduled_day'):
            try:
                scheduled_day = datetime.fromisoformat(task['scheduled_day']).date()
                # Find next occurrence
                days_until = (scheduled_day - today).days
                if days_until < 0:
                    days_until += 7
                return today + timedelta(days=days_until)
            except (ValueError, TypeError):
                return None
    
    elif task.get('frequency') == 'Monthly':
        if task.get('scheduled_day_of_month'):
            day_of_month = task['scheduled_day_of_month']
            # Find next occurrence this month or next month
            if today.day <= day_of_month:
                # This month
                return today.replace(day=day_of_month)
            else:
                # Next month
                next_month = today.replace(day=1) + timedelta(days=32)
                next_month = next_month.replace(day=1)
                return next_month.replace(day=day_of_month)
    
    return None

def get_overdue_selfcare_tasks() -> List[Dict[str, Any]]:
    """Get tasks that are overdue."""
    tasks = load_selfcare_tasks()
    today = date.today()
    
    overdue_tasks = []
    for task in tasks:
        last_completion = get_last_completion(task)
        if last_completion:
            next_due = get_next_due_date(task, last_completion)
            if next_due and next_due < today:
                overdue_tasks.append(task)
    
    return overdue_tasks

def get_last_completion(task: Dict[str, Any]) -> Optional[date]:
    """Get the last completion date for a task."""
    completions = task.get('completions', [])
    if completions:
        try:
            # Get the most recent completion
            latest_completion = max(completions, key=lambda x: datetime.fromisoformat(x['timestamp']).date())
            return datetime.fromisoformat(latest_completion['timestamp']).date()
        except (ValueError, TypeError):
            return None
    return None

def get_next_due_date(task: Dict[str, Any], last_completion: date) -> Optional[date]:
    """Get the next due date based on frequency and last completion."""
    if task.get('frequency') == 'Daily':
        return last_completion + timedelta(days=1)
    
    elif task.get('frequency') == 'Weekly':
        return last_completion + timedelta(days=7)
    
    elif task.get('frequency') == 'Monthly':
        # Add one month to last completion
        next_month = last_completion.replace(day=1) + timedelta(days=32)
        return next_month.replace(day=last_completion.day)
    
    return None

def mark_selfcare_task_complete(task_id: str) -> bool:
    """Mark a self-care task as complete."""
    tasks = load_selfcare_tasks()
    
    for task in tasks:
        if task.get('id') == task_id:
            # Initialize completions if not present
            if 'completions' not in task:
                task['completions'] = []
            
            # Add completion record
            completion = {
                'timestamp': datetime.now().isoformat(),
                'date': date.today().isoformat()
            }
            task['completions'].append(completion)
            
            # Save updated tasks
            with open(SELFCARE_FILE, 'w') as f:
                json.dump(tasks, f, indent=2)
            
            return True
    
    return False

def delete_selfcare_task(task_id: str) -> bool:
    """Delete a self-care task."""
    tasks = load_selfcare_tasks()
    
    for i, task in enumerate(tasks):
        if task.get('id') == task_id:
            del tasks[i]
            
            # Save updated tasks
            with open(SELFCARE_FILE, 'w') as f:
                json.dump(tasks, f, indent=2)
            
            return True
    
    return False

def get_selfcare_statistics() -> Dict[str, Any]:
    """Get self-care task statistics."""
    tasks = load_selfcare_tasks()
    
    if not tasks:
        return {
            'total_tasks': 0,
            'completed_tasks': 0,
            'pending_tasks': 0,
            'overdue_tasks': 0,
            'completion_rate': 0.0,
            'daily_tasks': 0,
            'weekly_tasks': 0,
            'monthly_tasks': 0
        }
    
    total_tasks = len(tasks)
    completed_tasks = 0
    pending_tasks = 0
    overdue_tasks = len(get_overdue_tasks())
    
    # Count by frequency
    daily_tasks = len([t for t in tasks if t.get('frequency') == 'Daily'])
    weekly_tasks = len([t for t in tasks if t.get('frequency') == 'Weekly'])
    monthly_tasks = len([t for t in tasks if t.get('frequency') == 'Monthly'])
    
    # Calculate completion rate
    total_completions = sum(len(t.get('completions', [])) for t in tasks)
    completion_rate = (total_completions / total_tasks) * 100 if total_tasks > 0 else 0
    
    return {
        'total_tasks': total_tasks,
        'completed_tasks': completed_tasks,
        'pending_tasks': pending_tasks,
        'overdue_tasks': overdue_tasks,
        'completion_rate': completion_rate,
        'daily_tasks': daily_tasks,
        'weekly_tasks': weekly_tasks,
        'monthly_tasks': monthly_tasks,
        'total_completions': total_completions
    }

def generate_selfcare_insights(tasks: List[Dict[str, Any]]) -> str:
    """Generate AI insights for self-care routines using GROQ."""
    if not tasks:
        return "No self-care tasks found to analyze."
    
    # Set up GROQ client
    api_key = os.getenv('GROQ_API_KEY')
    if not api_key:
        return "GROQ API key not found. Please set GROQ_API_KEY environment variable."
    
    client = openai.OpenAI(
        api_key=api_key,
        base_url="https://api.groq.com/openai/v1"
    )
    
    # Prepare task data for analysis
    task_analysis = []
    for task in tasks:
        task_entry = {
            'title': task.get('title', 'Unknown'),
            'category': task.get('category', 'Unknown'),
            'frequency': task.get('frequency', 'Unknown'),
            'scheduled_time': task.get('scheduled_time', 'No time set'),
            'completions_count': len(task.get('completions', [])),
            'last_completion': get_last_completion(task),
            'next_occurrence': get_next_occurrence(task)
        }
        task_analysis.append(task_entry)
    
    # Create prompt for GROQ
    prompt = f"""
    Analyze the following self-care routine data and provide insights and recommendations:

    SELF-CARE TASKS DATA:
    {json.dumps(task_analysis, indent=2)}

    Please provide insights on:
    1. **Routine Patterns**: Analysis of completion patterns and consistency
    2. **Frequency Optimization**: Whether daily, weekly, or monthly frequencies are working well
    3. **Time Management**: Analysis of scheduled times and completion timing
    4. **Category Balance**: Distribution across grooming, cleaning, health, and wellness
    5. **Missed Routines**: Identification of potentially missed or inconsistent routines
    6. **Recommendations**: Suggestions for improving self-care routine consistency
    7. **Wellness Insights**: How the routine contributes to overall wellness
    8. **Motivational Tips**: Encouragement for maintaining self-care habits

    Focus on:
    - Identifying patterns in completion rates
    - Suggesting optimal frequencies for different activities
    - Detecting potential gaps in self-care routines
    - Providing actionable recommendations for improvement
    - Encouraging consistent self-care habits

    Format your response in a clear, structured way with specific recommendations.
    Include motivational content and practical tips for maintaining routines.
    """
    
    try:
        response = client.chat.completions.create(
            model="llama3-70b-8192",  # Using GROQ's Llama model
            messages=[
                {"role": "system", "content": "You are a wellness coach and self-care expert analyzing routine data to provide insights and recommendations for maintaining consistent self-care habits."},
                {"role": "user", "content": prompt}
            ],
            max_tokens=1200,
            temperature=0.8
        )
        
        return response.choices[0].message.content
    
    except Exception as e:
        return f"Error generating insights: {str(e)}"

def save_selfcare_insight(insight_content: str, tasks_analyzed: int) -> None:
    """Save self-care insight to JSON file."""
    insight = {
        'content': insight_content,
        'source': 'selfcare_routines',
        'timestamp': datetime.now().isoformat(),
        'tasks_analyzed': tasks_analyzed,
        'analysis_type': 'Self-Care Routine Analysis'
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

def get_selfcare_insights() -> List[Dict[str, Any]]:
    """Get all self-care insights."""
    insights_file = "insights.json"
    
    if not os.path.exists(insights_file):
        return []
    
    try:
        with open(insights_file, 'r') as f:
            all_insights = json.load(f)
        
        # Filter for self-care insights
        selfcare_insights = [insight for insight in all_insights if insight.get('source') == 'selfcare_routines']
        return selfcare_insights
    except (json.JSONDecodeError, FileNotFoundError):
        return []

def format_selfcare_task_for_display(task: Dict[str, Any]) -> str:
    """Format a self-care task for display."""
    title = task.get('title', 'No title')
    category = task.get('category', 'Unknown')
    frequency = task.get('frequency', 'Unknown')
    scheduled_time = task.get('scheduled_time', 'No time set')
    
    # Category emoji
    category_emoji = {
        'Grooming': '💇‍♀️',
        'Cleaning': '🧹',
        'Health': '🏥',
        'Wellness': '🧘‍♀️',
        'Laundry': '👕',
        'Hygiene': '🛁'
    }.get(category, '📋')
    
    # Frequency emoji
    frequency_emoji = {
        'Daily': '📅',
        'Weekly': '📆',
        'Monthly': '🗓️'
    }.get(frequency, '⏰')
    
    return f"{category_emoji} {title} ({frequency_emoji} {frequency}, ⏰ {scheduled_time})"

def get_selfcare_task_completion_status(task: Dict[str, Any]) -> str:
    """Get the completion status of a task."""
    completions = task.get('completions', [])
    if not completions:
        return "Not started"
    
    # Get the most recent completion
    try:
        latest_completion = max(completions, key=lambda x: datetime.fromisoformat(x['timestamp']).date())
        completion_date = datetime.fromisoformat(latest_completion['timestamp']).date()
        today = date.today()
        
        if completion_date == today:
            return "Completed today"
        elif completion_date == today - timedelta(days=1):
            return "Completed yesterday"
        else:
            days_ago = (today - completion_date).days
            return f"Completed {days_ago} days ago"
    except (ValueError, TypeError):
        return "Unknown status"

def detect_missed_routines(tasks: List[Dict[str, Any]]) -> List[Dict[str, Any]]:
    """Detect potentially missed routines."""
    missed_routines = []
    today = date.today()
    
    for task in tasks:
        last_completion = get_last_completion(task)
        if last_completion:
            next_due = get_next_due_date(task, last_completion)
            if next_due and next_due < today:
                days_overdue = (today - next_due).days
                missed_routines.append({
                    'task': task,
                    'days_overdue': days_overdue,
                    'next_due': next_due
                })
    
    # Sort by days overdue (most overdue first)
    missed_routines.sort(key=lambda x: x['days_overdue'], reverse=True)
    return missed_routines 