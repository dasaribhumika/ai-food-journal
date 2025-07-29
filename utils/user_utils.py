import json
import os
import hashlib
from datetime import datetime
from typing import Dict, List, Optional

USERS_FILE = "users.json"
USER_DATA_DIR = "user_data"

def ensure_user_data_dir():
    """Ensure user data directory exists"""
    if not os.path.exists(USER_DATA_DIR):
        os.makedirs(USER_DATA_DIR)

def hash_password(password: str) -> str:
    """Hash password for security"""
    return hashlib.sha256(password.encode()).hexdigest()

def save_user(username: str, password: str) -> bool:
    """Save new user to users.json"""
    ensure_user_data_dir()
    
    # Load existing users
    users = load_users()
    
    # Check if username already exists
    if username in users:
        return False
    
    # Hash password and save user
    users[username] = {
        "password_hash": hash_password(password),
        "created_at": datetime.now().isoformat(),
        "last_login": datetime.now().isoformat()
    }
    
    # Save to file
    with open(USERS_FILE, 'w') as f:
        json.dump(users, f, indent=2)
    
    # Create user-specific data files
    create_user_data_files(username)
    
    return True

def load_users() -> Dict:
    """Load users from users.json"""
    if not os.path.exists(USERS_FILE):
        return {}
    
    try:
        with open(USERS_FILE, 'r') as f:
            return json.load(f)
    except:
        return {}

def authenticate_user(username: str, password: str) -> bool:
    """Authenticate user login"""
    users = load_users()
    
    if username not in users:
        return False
    
    stored_hash = users[username]["password_hash"]
    input_hash = hash_password(password)
    
    if stored_hash == input_hash:
        # Update last login
        users[username]["last_login"] = datetime.now().isoformat()
        with open(USERS_FILE, 'w') as f:
            json.dump(users, f, indent=2)
        return True
    
    return False

def create_user_data_files(username: str):
    """Create empty data files for new user"""
    ensure_user_data_dir()
    
    user_files = [
        "food_journal.json",
        "insights.json", 
        "tasks.json",
        "goals.json",
        "meal_plans.json",
        "recipes.json",
        "selfcare_tasks.json"
    ]
    
    for filename in user_files:
        user_file_path = os.path.join(USER_DATA_DIR, f"{username}_{filename}")
        if not os.path.exists(user_file_path):
            with open(user_file_path, 'w') as f:
                json.dump([], f)

def get_user_file_path(username: str, file_type: str) -> str:
    """Get the file path for a user's specific data file"""
    ensure_user_data_dir()
    return os.path.join(USER_DATA_DIR, f"{username}_{file_type}.json")

def save_user_data(username: str, file_type: str, data: List) -> None:
    """Save data to user-specific file"""
    file_path = get_user_file_path(username, file_type)
    with open(file_path, 'w') as f:
        json.dump(data, f, indent=2)

def load_user_data(username: str, file_type: str) -> List:
    """Load data from user-specific file"""
    file_path = get_user_file_path(username, file_type)
    
    if not os.path.exists(file_path):
        create_user_data_files(username)
        return []
    
    try:
        with open(file_path, 'r') as f:
            return json.load(f)
    except:
        return []

def user_exists(username: str) -> bool:
    """Check if user exists"""
    users = load_users()
    return username in users

def get_user_stats(username: str) -> Dict:
    """Get statistics for a user"""
    stats = {}
    
    # Count entries in each data type
    data_types = ["food_journal", "tasks", "goals", "meal_plans", "recipes", "selfcare_tasks"]
    
    for data_type in data_types:
        data = load_user_data(username, f"{data_type}.json")
        stats[f"{data_type}_count"] = len(data)
    
    # Get user info
    users = load_users()
    if username in users:
        stats["created_at"] = users[username]["created_at"]
        stats["last_login"] = users[username]["last_login"]
    
    return stats

def delete_user_data(username: str) -> bool:
    """Delete all data for a user"""
    try:
        # Remove user from users.json
        users = load_users()
        if username in users:
            del users[username]
            with open(USERS_FILE, 'w') as f:
                json.dump(users, f, indent=2)
        
        # Remove user data files
        user_files = [
            "food_journal.json",
            "insights.json", 
            "tasks.json",
            "goals.json",
            "meal_plans.json",
            "recipes.json",
            "selfcare_tasks.json"
        ]
        
        for filename in user_files:
            file_path = os.path.join(USER_DATA_DIR, f"{username}_{filename}")
            if os.path.exists(file_path):
                os.remove(file_path)
        
        return True
    except:
        return False 