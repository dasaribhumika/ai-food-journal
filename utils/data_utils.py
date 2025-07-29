import json
import os
from datetime import datetime, date
from typing import List, Dict, Any

# File paths
FOOD_JOURNAL_FILE = "food_journal.json"
INSIGHTS_FILE = "insights.json"

def save_food_entry(entry: Dict[str, Any]) -> None:
    """Save a food journal entry to JSON file."""
    # Add timestamp if not present
    if 'timestamp' not in entry:
        entry['timestamp'] = datetime.now().isoformat()
    
    # Load existing entries
    entries = load_food_entries()
    
    # Add new entry
    entries.append(entry)
    
    # Save back to file
    with open(FOOD_JOURNAL_FILE, 'w') as f:
        json.dump(entries, f, indent=2)

def load_food_entries() -> List[Dict[str, Any]]:
    """Load all food journal entries from JSON file."""
    if not os.path.exists(FOOD_JOURNAL_FILE):
        return []
    
    try:
        with open(FOOD_JOURNAL_FILE, 'r') as f:
            return json.load(f)
    except (json.JSONDecodeError, FileNotFoundError):
        return []

def get_todays_entries() -> List[Dict[str, Any]]:
    """Get all entries for today."""
    entries = load_food_entries()
    today = date.today().isoformat()
    
    todays_entries = []
    for entry in entries:
        entry_date = datetime.fromisoformat(entry['timestamp']).date().isoformat()
        if entry_date == today:
            todays_entries.append(entry)
    
    return todays_entries

def get_entries_by_date_range(start_date: str, end_date: str) -> List[Dict[str, Any]]:
    """Get entries within a date range."""
    entries = load_food_entries()
    filtered_entries = []
    
    for entry in entries:
        entry_date = datetime.fromisoformat(entry['timestamp']).date().isoformat()
        if start_date <= entry_date <= end_date:
            filtered_entries.append(entry)
    
    return filtered_entries

def format_entry_for_display(entry: Dict[str, Any]) -> str:
    """Format an entry for display."""
    timestamp = datetime.fromisoformat(entry['timestamp'])
    time_str = timestamp.strftime("%I:%M %p")
    
    display_parts = [f"🕐 {time_str}"]
    
    if 'meal_type' in entry:
        display_parts.append(f"🍽️ {entry['meal_type']}")
    
    if 'food_items' in entry:
        food_str = ", ".join(entry['food_items'])
        display_parts.append(f"🍎 {food_str}")
    
    if 'supplements' in entry and entry['supplements']:
        supp_str = ", ".join(entry['supplements'])
        display_parts.append(f"💊 {supp_str}")
    
    if 'symptoms' in entry and entry['symptoms']:
        symptoms_str = ", ".join(entry['symptoms'])
        display_parts.append(f"⚠️ {symptoms_str}")
    
    return " | ".join(display_parts)
