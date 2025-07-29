import json
import os
from datetime import datetime, date, timedelta
from typing import List, Dict, Any, Optional
import openai
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

# File paths
MEAL_PLAN_FILE = "meal_plans.json"
RECIPES_FILE = "recipes.json"

def save_meal_plan(meal_plan: Dict[str, Any]) -> None:
    """Save a meal plan to JSON file."""
    # Add timestamp if not present
    if 'created_at' not in meal_plan:
        meal_plan['created_at'] = datetime.now().isoformat()
    
    # Load existing meal plans
    meal_plans = load_meal_plans()
    
    # Add new meal plan
    meal_plans.append(meal_plan)
    
    # Save back to file
    with open(MEAL_PLAN_FILE, 'w') as f:
        json.dump(meal_plans, f, indent=2)

def load_meal_plans() -> List[Dict[str, Any]]:
    """Load all meal plans from JSON file."""
    if not os.path.exists(MEAL_PLAN_FILE):
        return []
    
    try:
        with open(MEAL_PLAN_FILE, 'r') as f:
            return json.load(f)
    except (json.JSONDecodeError, FileNotFoundError):
        return []

def get_current_week_plan() -> Dict[str, Any]:
    """Get the current week's meal plan."""
    meal_plans = load_meal_plans()
    today = date.today()
    
    # Find the most recent meal plan for the current week
    current_week_plan = None
    for plan in meal_plans:
        if plan.get('week_start'):
            try:
                week_start = datetime.fromisoformat(plan['week_start']).date()
                week_end = week_start + timedelta(days=6)
                if week_start <= today <= week_end:
                    current_week_plan = plan
                    break
            except (ValueError, TypeError):
                continue
    
    return current_week_plan

def create_weekly_meal_plan(week_start: date, meals: Dict[str, Dict[str, Any]]) -> Dict[str, Any]:
    """Create a new weekly meal plan."""
    meal_plan = {
        'id': f"plan_{datetime.now().strftime('%Y%m%d_%H%M%S')}",
        'week_start': week_start.isoformat(),
        'week_end': (week_start + timedelta(days=6)).isoformat(),
        'meals': meals,
        'created_at': datetime.now().isoformat(),
        'updated_at': datetime.now().isoformat()
    }
    
    return meal_plan

def update_meal_plan(plan_id: str, meals: Dict[str, Dict[str, Any]]) -> bool:
    """Update an existing meal plan."""
    meal_plans = load_meal_plans()
    
    for plan in meal_plans:
        if plan.get('id') == plan_id:
            plan['meals'] = meals
            plan['updated_at'] = datetime.now().isoformat()
            
            # Save updated meal plans
            with open(MEAL_PLAN_FILE, 'w') as f:
                json.dump(meal_plans, f, indent=2)
            
            return True
    
    return False

def delete_meal_plan(plan_id: str) -> bool:
    """Delete a meal plan."""
    meal_plans = load_meal_plans()
    
    for i, plan in enumerate(meal_plans):
        if plan.get('id') == plan_id:
            del meal_plans[i]
            
            # Save updated meal plans
            with open(MEAL_PLAN_FILE, 'w') as f:
                json.dump(meal_plans, f, indent=2)
            
            return True
    
    return False

# Recipe Book Functions
def save_recipe(recipe: Dict[str, Any]) -> None:
    """Save a recipe to JSON file."""
    # Add timestamp if not present
    if 'created_at' not in recipe:
        recipe['created_at'] = datetime.now().isoformat()
    
    # Load existing recipes
    recipes = load_recipes()
    
    # Add new recipe
    recipes.append(recipe)
    
    # Save back to file
    with open(RECIPES_FILE, 'w') as f:
        json.dump(recipes, f, indent=2)

def load_recipes() -> List[Dict[str, Any]]:
    """Load all recipes from JSON file."""
    if not os.path.exists(RECIPES_FILE):
        return []
    
    try:
        with open(RECIPES_FILE, 'r') as f:
            return json.load(f)
    except (json.JSONDecodeError, FileNotFoundError):
        return []

def get_recipe_by_id(recipe_id: str) -> Optional[Dict[str, Any]]:
    """Get a recipe by its ID."""
    recipes = load_recipes()
    
    for recipe in recipes:
        if recipe.get('id') == recipe_id:
            return recipe
    
    return None

def update_recipe(recipe_id: str, updated_recipe: Dict[str, Any]) -> bool:
    """Update an existing recipe."""
    recipes = load_recipes()
    
    for recipe in recipes:
        if recipe.get('id') == recipe_id:
            recipe.update(updated_recipe)
            recipe['updated_at'] = datetime.now().isoformat()
            
            # Save updated recipes
            with open(RECIPES_FILE, 'w') as f:
                json.dump(recipes, f, indent=2)
            
            return True
    
    return False

def delete_recipe(recipe_id: str) -> bool:
    """Delete a recipe."""
    recipes = load_recipes()
    
    for i, recipe in enumerate(recipes):
        if recipe.get('id') == recipe_id:
            del recipes[i]
            
            # Save updated recipes
            with open(RECIPES_FILE, 'w') as f:
                json.dump(recipes, f, indent=2)
            
            return True
    
    return False

def search_recipes(query: str) -> List[Dict[str, Any]]:
    """Search recipes by title or ingredients."""
    recipes = load_recipes()
    query = query.lower()
    
    matching_recipes = []
    for recipe in recipes:
        title = recipe.get('title', '').lower()
        ingredients = ' '.join(recipe.get('ingredients', [])).lower()
        
        if query in title or query in ingredients:
            matching_recipes.append(recipe)
    
    return matching_recipes

def generate_grocery_list(meal_plan: Dict[str, Any], recipes: List[Dict[str, Any]]) -> List[str]:
    """Generate a grocery list from meal plan and recipes."""
    grocery_items = []
    
    # Get all meals from the meal plan
    meals = meal_plan.get('meals', {})
    
    for day, day_meals in meals.items():
        for meal_type, meal_data in day_meals.items():
            if meal_data.get('recipe_id'):
                # Get recipe ingredients
                recipe = get_recipe_by_id(meal_data['recipe_id'])
                if recipe:
                    ingredients = recipe.get('ingredients', [])
                    grocery_items.extend(ingredients)
            elif meal_data.get('ingredients'):
                # Direct ingredients
                ingredients = meal_data.get('ingredients', [])
                grocery_items.extend(ingredients)
    
    # Remove duplicates and sort
    unique_items = list(set(grocery_items))
    unique_items.sort()
    
    return unique_items

def generate_meal_recommendations(food_entries: List[Dict[str, Any]], symptoms: List[str] = None) -> str:
    """Generate AI-powered meal recommendations using GROQ."""
    if not food_entries:
        return "No food journal data available for recommendations."
    
    # Set up GROQ client
    api_key = os.getenv('GROQ_API_KEY')
    if not api_key:
        return "GROQ API key not found. Please set GROQ_API_KEY environment variable."
    
    client = openai.OpenAI(
        api_key=api_key,
        base_url="https://api.groq.com/openai/v1"
    )
    
    # Prepare food data for analysis
    food_analysis = []
    for entry in food_entries[-20:]:  # Last 20 entries
        food_entry = {
            'meal_type': entry.get('meal_type', 'Unknown'),
            'food_items': entry.get('food_items', []),
            'symptoms': entry.get('symptoms', []),
            'supplements': entry.get('supplements', []),
            'meal_time': entry.get('meal_time', 'Unknown'),
            'notes': entry.get('notes', '')
        }
        food_analysis.append(food_entry)
    
    # Create prompt for GROQ
    symptoms_context = ""
    if symptoms:
        symptoms_context = f"\nCurrent symptoms to consider: {', '.join(symptoms)}"
    
    prompt = f"""
    Analyze the following food journal data and provide personalized meal recommendations for a weekly meal plan:

    FOOD JOURNAL DATA:
    {json.dumps(food_analysis, indent=2)}
    {symptoms_context}

    Please provide:
    1. **Breakfast Recommendations** (7 days) - Consider energy levels and morning routines
    2. **Lunch Recommendations** (7 days) - Focus on balanced nutrition and productivity
    3. **Dinner Recommendations** (7 days) - Consider evening comfort and sleep quality
    4. **Snack Suggestions** - Healthy options for between meals
    5. **Recipe Ideas** - Simple recipes that align with the user's food preferences
    6. **Grocery List Suggestions** - Essential ingredients for the recommended meals
    7. **Nutritional Considerations** - Based on symptoms and food reactions
    8. **Meal Prep Tips** - How to prepare these meals efficiently

    Focus on:
    - Foods that work well for the user (based on their journal)
    - Avoiding foods that cause symptoms
    - Balanced nutrition and variety
    - Practical, easy-to-prepare meals
    - Seasonal and accessible ingredients

    Format your response in a clear, structured way with specific meal suggestions for each day.
    Include recipe ideas and grocery shopping recommendations.
    """
    
    try:
        response = client.chat.completions.create(
            model="llama3-70b-8192",  # Using GROQ's Llama model
            messages=[
                {"role": "system", "content": "You are a nutritionist and meal planning expert analyzing food journal data to provide personalized meal recommendations that consider the user's food preferences, symptoms, and nutritional needs."},
                {"role": "user", "content": prompt}
            ],
            max_tokens=1500,
            temperature=0.8
        )
        
        return response.choices[0].message.content
    
    except Exception as e:
        return f"Error generating meal recommendations: {str(e)}"

def save_meal_insight(insight_content: str, meals_analyzed: int) -> None:
    """Save meal planning insight to JSON file."""
    insight = {
        'content': insight_content,
        'source': 'meal_planning',
        'timestamp': datetime.now().isoformat(),
        'meals_analyzed': meals_analyzed,
        'analysis_type': 'Meal Planning & Recommendations'
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

def get_meal_insights() -> List[Dict[str, Any]]:
    """Get all meal planning insights."""
    insights_file = "insights.json"
    
    if not os.path.exists(insights_file):
        return []
    
    try:
        with open(insights_file, 'r') as f:
            all_insights = json.load(f)
        
        # Filter for meal planning insights
        meal_insights = [insight for insight in all_insights if insight.get('source') == 'meal_planning']
        return meal_insights
    except (json.JSONDecodeError, FileNotFoundError):
        return []

def format_recipe_for_display(recipe: Dict[str, Any]) -> str:
    """Format a recipe for display."""
    title = recipe.get('title', 'No title')
    prep_time = recipe.get('prep_time', 'Unknown')
    cook_time = recipe.get('cook_time', 'Unknown')
    servings = recipe.get('servings', 'Unknown')
    
    ingredients = recipe.get('ingredients', [])
    steps = recipe.get('steps', [])
    
    display = f"**{title}**\n"
    display += f"⏱️ Prep: {prep_time} | 🍳 Cook: {cook_time} | 👥 Serves: {servings}\n\n"
    
    if ingredients:
        display += "**Ingredients:**\n"
        for i, ingredient in enumerate(ingredients, 1):
            display += f"{i}. {ingredient}\n"
        display += "\n"
    
    if steps:
        display += "**Steps:**\n"
        for i, step in enumerate(steps, 1):
            display += f"{i}. {step}\n"
    
    return display

def get_week_dates(week_start: date) -> List[Dict[str, Any]]:
    """Get the dates for a week starting from week_start."""
    week_dates = []
    for i in range(7):
        current_date = week_start + timedelta(days=i)
        week_dates.append({
            'date': current_date,
            'day_name': current_date.strftime('%A'),
            'date_str': current_date.strftime('%Y-%m-%d'),
            'display_date': current_date.strftime('%b %d')
        })
    return week_dates

def get_meal_statistics(meal_plans: List[Dict[str, Any]]) -> Dict[str, Any]:
    """Get meal planning statistics."""
    if not meal_plans:
        return {
            'total_plans': 0,
            'total_meals': 0,
            'recipes_used': 0,
            'grocery_items': 0
        }
    
    total_plans = len(meal_plans)
    total_meals = 0
    recipes_used = 0
    grocery_items = set()
    
    for plan in meal_plans:
        meals = plan.get('meals', {})
        for day_meals in meals.values():
            for meal_data in day_meals.values():
                total_meals += 1
                if meal_data.get('recipe_id'):
                    recipes_used += 1
                if meal_data.get('ingredients'):
                    grocery_items.update(meal_data['ingredients'])
    
    return {
        'total_plans': total_plans,
        'total_meals': total_meals,
        'recipes_used': recipes_used,
        'grocery_items': len(grocery_items)
    } 