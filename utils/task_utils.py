import json
import os
from datetime import datetime, date, timedelta
from typing import List, Dict, Any, Optional
import openai
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

# File paths
TASKS_FILE = "tasks.json"

def save_task(task: Dict[str, Any]) -> None:
    """Save a task to JSON file."""
    # Add timestamp if not present
    if 'created_at' not in task:
        task['created_at'] = datetime.now().isoformat()
    
    # Load existing tasks
    tasks = load_tasks()
    
    # Add new task
    tasks.append(task)
    
    # Save back to file
    with open(TASKS_FILE, 'w') as f:
        json.dump(tasks, f, indent=2)

def load_tasks() -> List[Dict[str, Any]]:
    """Load all tasks from JSON file."""
    if not os.path.exists(TASKS_FILE):
        return []
    
    try:
        with open(TASKS_FILE, 'r') as f:
            return json.load(f)
    except (json.JSONDecodeError, FileNotFoundError):
        return []

def get_todays_tasks() -> List[Dict[str, Any]]:
    """Get all tasks due today."""
    tasks = load_tasks()
    today = date.today()
    
    todays_tasks = []
    for task in tasks:
        if task.get('due_date'):
            try:
                due_date = datetime.fromisoformat(task['due_date']).date()
                if due_date == today:
                    todays_tasks.append(task)
            except (ValueError, TypeError):
                continue
    
    return todays_tasks

def get_upcoming_tasks(days: int = 7) -> List[Dict[str, Any]]:
    """Get tasks due in the next N days."""
    tasks = load_tasks()
    today = date.today()
    end_date = today + timedelta(days=days)
    
    upcoming_tasks = []
    for task in tasks:
        if task.get('due_date'):
            try:
                due_date = datetime.fromisoformat(task['due_date']).date()
                if today <= due_date <= end_date:
                    upcoming_tasks.append(task)
            except (ValueError, TypeError):
                continue
    
    return upcoming_tasks

def get_overdue_tasks() -> List[Dict[str, Any]]:
    """Get overdue tasks."""
    tasks = load_tasks()
    today = date.today()
    
    overdue_tasks = []
    for task in tasks:
        if task.get('due_date') and not task.get('completed', False):
            try:
                due_date = datetime.fromisoformat(task['due_date']).date()
                if due_date < today:
                    overdue_tasks.append(task)
            except (ValueError, TypeError):
                continue
    
    return overdue_tasks

def mark_task_complete(task_id: str) -> bool:
    """Mark a task as complete."""
    tasks = load_tasks()
    
    for task in tasks:
        if task.get('id') == task_id:
            task['completed'] = True
            task['completed_at'] = datetime.now().isoformat()
            
            # Save updated tasks
            with open(TASKS_FILE, 'w') as f:
                json.dump(tasks, f, indent=2)
            
            return True
    
    return False

def delete_task(task_id: str) -> bool:
    """Delete a task."""
    tasks = load_tasks()
    
    for i, task in enumerate(tasks):
        if task.get('id') == task_id:
            del tasks[i]
            
            # Save updated tasks
            with open(TASKS_FILE, 'w') as f:
                json.dump(tasks, f, indent=2)
            
            return True
    
    return False

def get_task_statistics() -> Dict[str, Any]:
    """Get task completion statistics."""
    tasks = load_tasks()
    
    if not tasks:
        return {
            'total_tasks': 0,
            'completed_tasks': 0,
            'pending_tasks': 0,
            'overdue_tasks': 0,
            'completion_rate': 0.0
        }
    
    total_tasks = len(tasks)
    completed_tasks = len([t for t in tasks if t.get('completed', False)])
    pending_tasks = total_tasks - completed_tasks
    overdue_tasks = len(get_overdue_tasks())
    
    completion_rate = (completed_tasks / total_tasks) * 100 if total_tasks > 0 else 0
    
    return {
        'total_tasks': total_tasks,
        'completed_tasks': completed_tasks,
        'pending_tasks': pending_tasks,
        'overdue_tasks': overdue_tasks,
        'completion_rate': completion_rate
    }

def generate_task_insights(tasks: List[Dict[str, Any]]) -> str:
    """Generate AI insights for task management using GROQ."""
    if not tasks:
        return "No tasks found to analyze."
    
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
            'priority': task.get('priority', 'Medium'),
            'due_date': task.get('due_date', 'No due date'),
            'completed': task.get('completed', False),
            'created_at': task.get('created_at', 'Unknown')
        }
        task_analysis.append(task_entry)
    
    # Create prompt for GROQ
    prompt = f"""
    Analyze the following task management data and provide insights about productivity patterns and recommendations:

    TASK DATA:
    {json.dumps(task_analysis, indent=2)}

    Please provide insights on:
    1. Task completion patterns and productivity trends
    2. Category-wise performance analysis (Work, Health, Personal)
    3. Priority management effectiveness
    4. Time management patterns and suggestions
    5. Recommendations for improving task completion rates
    6. Suggestions for better task organization and prioritization
    7. Work-life balance insights based on task categories

    Focus on actionable insights and specific recommendations for better productivity.
    Format your response in a clear, structured way with bullet points for key findings.
    """
    
    try:
        response = client.chat.completions.create(
            model="llama3-70b-8192",  # Using GROQ's Llama model
            messages=[
                {"role": "system", "content": "You are a productivity and task management expert analyzing task data to provide actionable insights for better time management and productivity."},
                {"role": "user", "content": prompt}
            ],
            max_tokens=1000,
            temperature=0.7
        )
        
        return response.choices[0].message.content
    
    except Exception as e:
        return f"Error generating insights: {str(e)}"

def save_task_insight(insight_content: str, tasks_analyzed: int) -> None:
    """Save task insight to JSON file."""
    insight = {
        'content': insight_content,
        'source': 'task_management',
        'timestamp': datetime.now().isoformat(),
        'tasks_analyzed': tasks_analyzed,
        'analysis_type': 'Task Management & Productivity'
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

def get_task_insights() -> List[Dict[str, Any]]:
    """Get all task-related insights."""
    insights_file = "insights.json"
    
    if not os.path.exists(insights_file):
        return []
    
    try:
        with open(insights_file, 'r') as f:
            all_insights = json.load(f)
        
        # Filter for task insights
        task_insights = [insight for insight in all_insights if insight.get('source') == 'task_management']
        return task_insights
    except (json.JSONDecodeError, FileNotFoundError):
        return []

def format_task_for_display(task: Dict[str, Any]) -> str:
    """Format a task for display."""
    title = task.get('title', 'No title')
    category = task.get('category', 'Unknown')
    priority = task.get('priority', 'Medium')
    due_date = task.get('due_date', 'No due date')
    
    # Format due date
    if due_date != 'No due date':
        try:
            due_date_obj = datetime.fromisoformat(due_date)
            due_date = due_date_obj.strftime("%b %d, %Y")
        except (ValueError, TypeError):
            pass
    
    # Priority emoji
    priority_emoji = {
        'High': '🔴',
        'Medium': '🟡', 
        'Low': '🟢'
    }.get(priority, '⚪')
    
    # Category emoji
    category_emoji = {
        'Work': '💼',
        'Health': '🏥',
        'Personal': '👤'
    }.get(category, '📝')
    
    # Completion status
    status = "✅" if task.get('completed', False) else "⏳"
    
    return f"{status} {priority_emoji} {category_emoji} {title} (Due: {due_date})"

def suggest_priority_tasks(tasks: List[Dict[str, Any]]) -> List[Dict[str, Any]]:
    """Suggest priority tasks based on frequency and completion status."""
    if not tasks:
        return []
    
    # Filter incomplete tasks
    incomplete_tasks = [t for t in tasks if not t.get('completed', False)]
    
    # Sort by priority and due date
    def sort_key(task):
        priority_order = {'High': 3, 'Medium': 2, 'Low': 1}
        priority = priority_order.get(task.get('priority', 'Medium'), 2)
        
        # Check if overdue
        due_date = task.get('due_date')
        if due_date:
            try:
                due_date_obj = datetime.fromisoformat(due_date).date()
                if due_date_obj < date.today():
                    priority += 10  # Boost priority for overdue tasks
            except (ValueError, TypeError):
                pass
        
        return (-priority, task.get('due_date', ''))
    
    return sorted(incomplete_tasks, key=sort_key) 