import streamlit as st
import pandas as pd
import os
from datetime import datetime, date, timedelta
from utils.data_utils import (
    save_food_entry, 
    get_todays_entries, 
    format_entry_for_display,
    get_entries_by_date_range
)
from utils.insight_utils import (
    generate_ai_insights,
    save_insight,
    load_insights,
    format_insight_for_display,
    get_recent_insights
)
from utils.oura_utils import (
    parse_oura_csv,
    get_oura_summary_stats,
    generate_oura_insights,
    save_oura_insight,
    get_oura_insights,
    format_oura_insight_for_display,
    create_sleep_food_correlation_data
)
from utils.task_utils import (
    save_task,
    load_tasks,
    get_todays_tasks,
    get_upcoming_tasks,
    get_overdue_tasks,
    mark_task_complete,
    delete_task,
    get_task_statistics,
    generate_task_insights,
    save_task_insight,
    get_task_insights,
    format_task_for_display,
    suggest_priority_tasks
)
from utils.goal_utils import (
    save_goal,
    load_goals,
    get_todays_goals,
    get_weekly_goals,
    get_monthly_goals,
    get_overdue_goals,
    mark_goal_complete,
    delete_goal,
    get_goal_statistics,
    generate_goal_insights,
    save_goal_insight,
    get_goal_insights,
    format_goal_for_display,
    calculate_goal_progress,
    detect_missing_goals
)
from utils.meal_utils import (
    save_meal_plan,
    load_meal_plans,
    get_current_week_plan,
    create_weekly_meal_plan,
    update_meal_plan,
    delete_meal_plan,
    save_recipe,
    load_recipes,
    get_recipe_by_id,
    update_recipe,
    delete_recipe,
    search_recipes,
    generate_grocery_list,
    generate_meal_recommendations,
    save_meal_insight,
    get_meal_insights,
    format_recipe_for_display,
    get_week_dates,
    get_meal_statistics
)
from utils.selfcare_utils import (
    save_selfcare_task,
    load_selfcare_tasks,
    get_todays_selfcare_tasks,
    get_upcoming_selfcare_tasks,
    get_overdue_selfcare_tasks,
    mark_selfcare_task_complete,
    delete_selfcare_task,
    get_selfcare_statistics,
    generate_selfcare_insights,
    save_selfcare_insight,
    get_selfcare_insights,
    format_selfcare_task_for_display,
    get_selfcare_task_completion_status,
    detect_missed_routines
)

# Page configuration
st.set_page_config(
    page_title="AI Food Journal",
    page_icon="🍎",
    layout="wide",
    initial_sidebar_state="expanded",
    menu_items={
        'Get Help': None,
        'Report a bug': None,
        'About': None
    }
)

# Custom CSS for better styling
st.markdown("""
<style>
    .main-header {
        font-size: 2.5rem;
        color: #1f77b4;
        text-align: center;
        margin-bottom: 2rem;
    }
    .section-header {
        font-size: 1.5rem;
        color: #2c3e50;
        margin-bottom: 1rem;
        border-bottom: 2px solid #3498db;
        padding-bottom: 0.5rem;
    }
    .entry-card {
        background-color: #f8f9fa;
        padding: 1rem;
        border-radius: 10px;
        margin: 0.5rem 0;
        border-left: 4px solid #3498db;
    }
    .insight-card {
        background-color: #f8f9fa;
        padding: 1.5rem;
        border-radius: 10px;
        margin: 0.5rem 0;
        border-left: 4px solid #3498db;
        color: #2c3e50;
        font-weight: 500;
        line-height: 1.6;
        box-shadow: 0 2px 4px rgba(0,0,0,0.1);
    }
    .insight-card strong {
        color: #1a252f;
        font-weight: 600;
    }
    .stButton > button {
        background-color: #3498db;
        color: white;
        border-radius: 5px;
        padding: 0.5rem 1rem;
        border: none;
    }
    .stButton > button:hover {
        background-color: #2980b9;
    }
</style>
""", unsafe_allow_html=True)

def main():
    st.markdown('<h1 class="main-header">🍎 AI Food Journal</h1>', unsafe_allow_html=True)
    
    # Sidebar for navigation
    st.sidebar.title("Navigation")
    page = st.sidebar.selectbox(
        "Choose a page",
        ["Food Journal", "OURA Analysis", "Task Manager", "Goal Tracker", "Meal Planning", "Self-Care", "Analytics", "Settings"]
    )
    
    if page == "Food Journal":
        food_journal_page()
    elif page == "OURA Analysis":
        oura_analysis_page()
    elif page == "Task Manager":
        task_manager_page()
    elif page == "Goal Tracker":
        goal_tracker_page()
    elif page == "Meal Planning":
        meal_planning_page()
    elif page == "Self-Care":
        selfcare_page()
    elif page == "Analytics":
        analytics_page()
    elif page == "Settings":
        settings_page()

def food_journal_page():
    st.markdown('<h2 class="section-header">📝 Log Your Food & Health</h2>', unsafe_allow_html=True)
    
    # Create two columns for the form
    col1, col2 = st.columns(2)
    
    with col1:
        st.subheader("Meal Information")
        
        # Meal type selection
        meal_type = st.selectbox(
            "Meal Type",
            ["Breakfast", "Lunch", "Dinner", "Snack", "Other"]
        )
        
        # Food items input
        food_input = st.text_area(
            "Food Items (one per line)",
            placeholder="Enter each food item on a new line\nExample:\nOatmeal\nBanana\nAlmonds"
        )
        
        # Convert food input to list
        food_items = [item.strip() for item in food_input.split('\n') if item.strip()] if food_input else []
        
        # Supplements input
        supplements_input = st.text_area(
            "Supplements (one per line)",
            placeholder="Enter each supplement on a new line\nExample:\nVitamin D\nOmega-3"
        )
        
        # Convert supplements input to list
        supplements = [item.strip() for item in supplements_input.split('\n') if item.strip()] if supplements_input else []
    
    with col2:
        st.subheader("Health Information")
        
        # Symptoms input
        symptoms_input = st.text_area(
            "Symptoms (one per line)",
            placeholder="Enter any symptoms you experienced\nExample:\nBloating\nFatigue\nHeadache"
        )
        
        # Convert symptoms input to list
        symptoms = [item.strip() for item in symptoms_input.split('\n') if item.strip()] if symptoms_input else []
        
        # Additional notes
        notes = st.text_area(
            "Additional Notes",
            placeholder="Any additional observations or notes..."
        )
        
        # Meal time
        meal_time = st.time_input(
            "Meal Time",
            value=datetime.now().time()
        )
    
    # Submit button
    if st.button("💾 Save Entry", type="primary"):
        if not food_items:
            st.error("Please enter at least one food item.")
        else:
            # Create entry
            entry = {
                'meal_type': meal_type,
                'food_items': food_items,
                'supplements': supplements,
                'symptoms': symptoms,
                'notes': notes,
                'meal_time': meal_time.strftime("%H:%M")
            }
            
            # Save entry
            save_food_entry(entry)
            st.success("✅ Entry saved successfully!")
            
            # Clear form
            st.rerun()
    
    # Display today's entries
    st.markdown('<h3 class="section-header">📅 Today\'s Entries</h3>', unsafe_allow_html=True)
    
    todays_entries = get_todays_entries()
    
    if todays_entries:
        for entry in todays_entries:
            st.markdown(f'<div class="entry-card">{format_entry_for_display(entry)}</div>', unsafe_allow_html=True)
    else:
        st.info("No entries for today yet. Start logging your meals!")
    
    # AI Insights Section
    st.markdown('<h3 class="section-header">🤖 AI Insights</h3>', unsafe_allow_html=True)
    
    # Get all entries for analysis (last 30 days)
    from datetime import timedelta
    end_date = date.today().isoformat()
    start_date = (date.today() - timedelta(days=30)).isoformat()
    recent_entries = get_entries_by_date_range(start_date, end_date)
    
    if recent_entries:
        if st.button("🔍 Generate AI Insights", type="secondary"):
            with st.spinner("Analyzing your food journal data..."):
                insight_content = generate_ai_insights(recent_entries)
                
                if insight_content and not insight_content.startswith("Error"):
                    # Save the insight
                    insight = {
                        'content': insight_content,
                        'entries_analyzed': len(recent_entries),
                        'date_range': f"{start_date} to {end_date}"
                    }
                    save_insight(insight)
                    st.success("✅ Insights generated and saved!")
                
                st.markdown(f'<div class="insight-card"><strong>🤖 AI Analysis:</strong><br>{insight_content}</div>', unsafe_allow_html=True)
        else:
            st.info("Add some entries to generate AI insights!")
        
        # Display past insights
        st.markdown('<h4>📊 Recent Insights</h4>', unsafe_allow_html=True)
    
    recent_insights = get_recent_insights(3)
    if recent_insights:
        for insight in recent_insights:
            st.markdown(f'<div class="insight-card"><strong>📊 Previous Analysis:</strong><br>{format_insight_for_display(insight)}</div>', unsafe_allow_html=True)
    else:
        st.info("No insights generated yet. Generate your first insight!")

def oura_analysis_page():
    st.markdown('<h2 class="section-header">📊 OURA Sleep & Activity Analysis</h2>', unsafe_allow_html=True)
    
    # File upload section
    st.subheader("📁 Upload OURA CSV Data")
    
    uploaded_file = st.file_uploader(
        "Choose your OURA CSV file",
        type=['csv'],
        help="Upload your OURA ring data export (CSV format)"
    )
    
    # Initialize session state for OURA data
    if 'oura_data' not in st.session_state:
        st.session_state.oura_data = None
    if 'oura_stats' not in st.session_state:
        st.session_state.oura_stats = None
    
    if uploaded_file is not None:
        try:
            # Save uploaded file temporarily
            with open("temp_oura.csv", "wb") as f:
                f.write(uploaded_file.getbuffer())
            
            # Parse OURA data
            oura_df = parse_oura_csv("temp_oura.csv")
            st.session_state.oura_data = oura_df
            st.session_state.oura_stats = get_oura_summary_stats(oura_df)
            
            # Clean up temp file
            os.remove("temp_oura.csv")
            
            st.success(f"✅ Successfully loaded {len(oura_df)} days of OURA data!")
            
        except Exception as e:
            st.error(f"❌ Error parsing OURA file: {str(e)}")
            st.info("Please ensure your CSV file contains OURA ring data with columns like 'Date', 'Sleep Score', 'Readiness Score', etc.")
    
    # Display OURA data if available
    if st.session_state.oura_data is not None:
        oura_df = st.session_state.oura_data
        stats = st.session_state.oura_stats
        
        # Summary statistics
        st.subheader("📈 Summary Statistics")
        
        col1, col2, col3, col4 = st.columns(4)
        
        with col1:
            if 'avg_sleep_score' in stats:
                st.metric("Avg Sleep Score", f"{stats['avg_sleep_score']:.1f}")
            if 'avg_sleep_hours' in stats:
                st.metric("Avg Sleep Hours", f"{stats['avg_sleep_hours']:.1f}")
        
        with col2:
            if 'avg_readiness' in stats:
                st.metric("Avg Readiness", f"{stats['avg_readiness']:.1f}")
            if 'avg_activity' in stats:
                st.metric("Avg Activity", f"{stats['avg_activity']:.1f}")
        
        with col3:
            if 'best_sleep_score' in stats:
                st.metric("Best Sleep Score", f"{stats['best_sleep_score']:.1f}")
            if 'total_steps' in stats:
                st.metric("Total Steps", f"{stats['total_steps']:,}")
        
        with col4:
            if 'worst_sleep_score' in stats:
                st.metric("Worst Sleep Score", f"{stats['worst_sleep_score']:.1f}")
            if 'total_sleep_hours' in stats:
                st.metric("Total Sleep Hours", f"{stats['total_sleep_hours']:.1f}")
        
        # Data table
        st.subheader("📋 OURA Data Table")
        
        # Select columns to display
        available_columns = ['date', 'sleep_score', 'sleep_hours', 'sleep_efficiency', 
                           'readiness_score', 'activity_score', 'activity_steps', 'avg_heart_rate']
        display_columns = [col for col in available_columns if col in oura_df.columns]
        
        if display_columns:
            display_df = oura_df[display_columns].copy()
            display_df['date'] = display_df['date'].dt.strftime('%Y-%m-%d')
            st.dataframe(display_df, use_container_width=True)
        
        # Charts
        st.subheader("📊 Charts & Visualizations")
        
        tab1, tab2, tab3 = st.tabs(["Sleep Trends", "Activity Patterns", "Correlation Analysis"])
        
        with tab1:
            if 'sleep_score' in oura_df.columns and 'date' in oura_df.columns:
                chart_data = oura_df[['date', 'sleep_score']].dropna()
                if not chart_data.empty:
                    st.line_chart(chart_data.set_index('date'))
                    st.caption("Sleep Score Over Time")
        
        with tab2:
            if 'activity_score' in oura_df.columns and 'date' in oura_df.columns:
                chart_data = oura_df[['date', 'activity_score']].dropna()
                if not chart_data.empty:
                    st.line_chart(chart_data.set_index('date'))
                    st.caption("Activity Score Over Time")
        
        with tab3:
            if 'readiness_score' in oura_df.columns and 'date' in oura_df.columns:
                chart_data = oura_df[['date', 'readiness_score']].dropna()
                if not chart_data.empty:
                    st.line_chart(chart_data.set_index('date'))
                    st.caption("Readiness Score Over Time")
        
        # AI Insights Generation
        st.subheader("🤖 AI Insights: Sleep & Food Correlation")
        
        # Get food journal entries for comparison
        from utils.data_utils import load_food_entries
        food_entries = load_food_entries()
        
        if food_entries:
            st.info(f"Found {len(food_entries)} food journal entries for correlation analysis.")
            
            if st.button("🔍 Generate OURA + Food Insights", type="secondary"):
                with st.spinner("Analyzing sleep patterns and food correlations..."):
                    insight_content = generate_oura_insights(oura_df, food_entries)
                    
                    if insight_content and not insight_content.startswith("Error"):
                        # Save the insight
                        save_oura_insight(insight_content, len(oura_df), len(food_entries))
                        st.success("✅ OURA insights generated and saved!")
                    
                    st.markdown(f'<div class="insight-card"><strong>🤖 OURA Analysis:</strong><br>{insight_content}</div>', unsafe_allow_html=True)
        else:
            st.warning("No food journal entries found. Add some food entries to enable correlation analysis.")
        
        # Display past OURA insights
        st.subheader("📊 Previous OURA Insights")
        
        oura_insights = get_oura_insights()
        if oura_insights:
            for insight in oura_insights[-3:]:  # Show last 3 insights
                st.markdown(f'<div class="insight-card"><strong>📊 OURA Analysis:</strong><br>{format_oura_insight_for_display(insight)}</div>', unsafe_allow_html=True)
        else:
            st.info("No OURA insights generated yet. Generate your first insight!")
    
    else:
        st.info("📁 Please upload your OURA CSV file to begin analysis.")
        st.markdown("""
        **How to export YOURA data:**
        1. Open the OURA app
        2. Go to Insights → Sleep/Activity
        3. Select date range
        4. Export as CSV
        5. Upload the file here
        """)

def task_manager_page():
    st.markdown('<h2 class="section-header">📋 Task Manager</h2>', unsafe_allow_html=True)
    
    # Initialize session state for task ID counter
    if 'task_id_counter' not in st.session_state:
        st.session_state.task_id_counter = 0
    
    # Task creation form
    st.subheader("➕ Add New Task")
    
    col1, col2 = st.columns(2)
    
    with col1:
        task_title = st.text_input(
            "Task Title",
            placeholder="Enter task title..."
        )
        
        task_category = st.selectbox(
            "Category",
            ["Work", "Health", "Personal"]
        )
        
        task_priority = st.selectbox(
            "Priority",
            ["High", "Medium", "Low"]
        )
    
    with col2:
        task_description = st.text_area(
            "Description (Optional)",
            placeholder="Add task description..."
        )
        
        task_due_date = st.date_input(
            "Due Date",
            value=date.today()
        )
    
    # Add task button
    if st.button("💾 Add Task", type="primary"):
        if not task_title:
            st.error("Please enter a task title.")
        else:
            # Generate unique task ID
            st.session_state.task_id_counter += 1
            task_id = f"task_{st.session_state.task_id_counter}"
            
            # Create task
            task = {
                'id': task_id,
                'title': task_title,
                'category': task_category,
                'priority': task_priority,
                'description': task_description,
                'due_date': task_due_date.isoformat(),
                'completed': False
            }
            
            # Save task
            save_task(task)
            st.success("✅ Task added successfully!")
            st.rerun()
    
    # Task overview
    st.subheader("📊 Task Overview")
    
    # Get task statistics
    stats = get_task_statistics()
    
    col1, col2, col3, col4 = st.columns(4)
    
    with col1:
        st.metric("Total Tasks", stats['total_tasks'])
    
    with col2:
        st.metric("Completed", stats['completed_tasks'])
    
    with col3:
        st.metric("Pending", stats['pending_tasks'])
    
    with col4:
        st.metric("Overdue", stats['overdue_tasks'])
    
    # Progress bar for completion rate
    st.progress(stats['completion_rate'] / 100)
    st.caption(f"Completion Rate: {stats['completion_rate']:.1f}%")
    
    # Task lists
    tab1, tab2, tab3, tab4 = st.tabs(["Today's Tasks", "Upcoming Tasks", "Overdue Tasks", "All Tasks"])
    
    with tab1:
        st.subheader("📅 Today's Tasks")
        todays_tasks = get_todays_tasks()
        
        if todays_tasks:
            for task in todays_tasks:
                col1, col2, col3 = st.columns([3, 1, 1])
                
                with col1:
                    st.markdown(f"**{task['title']}**")
                    st.caption(f"{task['category']} • {task['priority']} Priority")
                    if task.get('description'):
                        st.caption(task['description'])
                
                with col2:
                    if not task.get('completed', False):
                        if st.button("✅ Complete", key=f"complete_{task['id']}"):
                            mark_task_complete(task['id'])
                            st.success("Task completed!")
                            st.rerun()
                
                with col3:
                    if st.button("🗑️ Delete", key=f"delete_{task['id']}"):
                        delete_task(task['id'])
                        st.success("Task deleted!")
                        st.rerun()
                
                st.divider()
        else:
            st.info("No tasks due today! 🎉")
    
    with tab2:
        st.subheader("📅 Upcoming Tasks (Next 7 Days)")
        upcoming_tasks = get_upcoming_tasks(7)
        
        if upcoming_tasks:
            for task in upcoming_tasks:
                col1, col2, col3 = st.columns([3, 1, 1])
                
                with col1:
                    st.markdown(f"**{task['title']}**")
                    due_date = datetime.fromisoformat(task['due_date']).strftime("%b %d, %Y")
                    st.caption(f"{task['category']} • {task['priority']} Priority • Due: {due_date}")
                    if task.get('description'):
                        st.caption(task['description'])
                
                with col2:
                    if not task.get('completed', False):
                        if st.button("✅ Complete", key=f"complete_up_{task['id']}"):
                            mark_task_complete(task['id'])
                            st.success("Task completed!")
                            st.rerun()
                
                with col3:
                    if st.button("🗑️ Delete", key=f"delete_up_{task['id']}"):
                        delete_task(task['id'])
                        st.success("Task deleted!")
                        st.rerun()
                
                st.divider()
        else:
            st.info("No upcoming tasks! 📅")
    
    with tab3:
        st.subheader("⚠️ Overdue Tasks")
        overdue_tasks = get_overdue_tasks()
        
        if overdue_tasks:
            for task in overdue_tasks:
                col1, col2, col3 = st.columns([3, 1, 1])
                
                with col1:
                    st.markdown(f"**{task['title']}**")
                    due_date = datetime.fromisoformat(task['due_date']).strftime("%b %d, %Y")
                    st.caption(f"{task['category']} • {task['priority']} Priority • Overdue since {due_date}")
                    if task.get('description'):
                        st.caption(task['description'])
                
                with col2:
                    if st.button("✅ Complete", key=f"complete_over_{task['id']}"):
                        mark_task_complete(task['id'])
                        st.success("Task completed!")
                        st.rerun()
                
                with col3:
                    if st.button("🗑️ Delete", key=f"delete_over_{task['id']}"):
                        delete_task(task['id'])
                        st.success("Task deleted!")
                        st.rerun()
                
                st.divider()
        else:
            st.info("No overdue tasks! 🎉")
    
    with tab4:
        st.subheader("📋 All Tasks")
        all_tasks = load_tasks()
        
        if all_tasks:
            # Filter options
            col1, col2 = st.columns(2)
            
            with col1:
                category_filter = st.selectbox(
                    "Filter by Category",
                    ["All", "Work", "Health", "Personal"]
                )
            
            with col2:
                status_filter = st.selectbox(
                    "Filter by Status",
                    ["All", "Completed", "Pending"]
                )
            
            # Apply filters
            filtered_tasks = all_tasks
            
            if category_filter != "All":
                filtered_tasks = [t for t in filtered_tasks if t.get('category') == category_filter]
            
            if status_filter == "Completed":
                filtered_tasks = [t for t in filtered_tasks if t.get('completed', False)]
            elif status_filter == "Pending":
                filtered_tasks = [t for t in filtered_tasks if not t.get('completed', False)]
            
            # Display filtered tasks
            for task in filtered_tasks:
                col1, col2, col3 = st.columns([3, 1, 1])
                
                with col1:
                    status_emoji = "✅" if task.get('completed', False) else "⏳"
                    st.markdown(f"{status_emoji} **{task['title']}**")
                    due_date = datetime.fromisoformat(task['due_date']).strftime("%b %d, %Y")
                    st.caption(f"{task['category']} • {task['priority']} Priority • Due: {due_date}")
                    if task.get('description'):
                        st.caption(task['description'])
                
                with col2:
                    if not task.get('completed', False):
                        if st.button("✅ Complete", key=f"complete_all_{task['id']}"):
                            mark_task_complete(task['id'])
                            st.success("Task completed!")
                            st.rerun()
                
                with col3:
                    if st.button("🗑️ Delete", key=f"delete_all_{task['id']}"):
                        delete_task(task['id'])
                        st.success("Task deleted!")
                        st.rerun()
                
                st.divider()
        else:
            st.info("No tasks created yet. Add your first task above! 📝")
    
    # AI Insights Section
    st.subheader("🤖 AI Task Insights")
    
    all_tasks = load_tasks()
    
    if all_tasks:
        if st.button("🔍 Generate Task Insights", type="secondary"):
            with st.spinner("Analyzing your task patterns..."):
                insight_content = generate_task_insights(all_tasks)
                
                if insight_content and not insight_content.startswith("Error"):
                    # Save the insight
                    save_task_insight(insight_content, len(all_tasks))
                    st.success("✅ Task insights generated and saved!")
                
                st.markdown(f'<div class="insight-card"><strong>🤖 Task Analysis:</strong><br>{insight_content}</div>', unsafe_allow_html=True)
    else:
        st.info("Add some tasks to generate AI insights!")
    
    # Display past task insights
    st.subheader("📊 Previous Task Insights")
    
    task_insights = get_task_insights()
    if task_insights:
        for insight in task_insights[-3:]:  # Show last 3 insights
            timestamp = datetime.fromisoformat(insight['timestamp'])
            date_str = timestamp.strftime("%B %d, %Y at %I:%M %p")
            st.markdown(f'<div class="insight-card"><strong>📊 Task Analysis - {date_str}:</strong><br>{insight.get("content", "No content")}</div>', unsafe_allow_html=True)
    else:
        st.info("No task insights generated yet. Generate your first insight!")

def goal_tracker_page():
    st.markdown('<h2 class="section-header">🎯 Goal Tracker</h2>', unsafe_allow_html=True)
    
    # Initialize session state for goal ID counter
    if 'goal_id_counter' not in st.session_state:
        st.session_state.goal_id_counter = 0
    
    # Goal creation form
    st.subheader("➕ Add New Goal")
    
    col1, col2 = st.columns(2)
    
    with col1:
        goal_title = st.text_input(
            "Goal Title",
            placeholder="Enter goal title..."
        )
        
        goal_timeframe = st.selectbox(
            "Timeframe",
            ["Daily", "Weekly", "Monthly"]
        )
        
        goal_deadline = st.date_input(
            "Deadline",
            value=date.today()
        )
    
    with col2:
        goal_description = st.text_area(
            "Description (Optional)",
            placeholder="Add goal description..."
        )
        
        goal_priority = st.selectbox(
            "Priority",
            ["High", "Medium", "Low"]
        )
    
    # Add goal button
    if st.button("💾 Add Goal", type="primary"):
        if not goal_title:
            st.error("Please enter a goal title.")
        else:
            # Generate unique goal ID
            st.session_state.goal_id_counter += 1
            goal_id = f"goal_{st.session_state.goal_id_counter}"
            
            # Create goal
            goal = {
                'id': goal_id,
                'title': goal_title,
                'description': goal_description,
                'timeframe': goal_timeframe,
                'priority': goal_priority,
                'deadline': goal_deadline.isoformat(),
                'completed': False
            }
            
            # Save goal
            save_goal(goal)
            st.success("✅ Goal added successfully!")
            st.rerun()
    
    # Goal overview
    st.subheader("📊 Goal Overview")
    
    # Get goal statistics
    stats = get_goal_statistics()
    
    col1, col2, col3, col4 = st.columns(4)
    
    with col1:
        st.metric("Total Goals", stats['total_goals'])
    
    with col2:
        st.metric("Completed", stats['completed_goals'])
    
    with col3:
        st.metric("Pending", stats['pending_goals'])
    
    with col4:
        st.metric("Overdue", stats['overdue_goals'])
    
    # Progress bar for completion rate
    st.progress(stats['completion_rate'] / 100)
    st.caption(f"Completion Rate: {stats['completion_rate']:.1f}%")
    
    # Goal breakdown by timeframe
    st.subheader("📈 Goal Breakdown")
    
    col1, col2, col3 = st.columns(3)
    
    with col1:
        st.metric("Daily Goals", stats['daily_goals'])
    
    with col2:
        st.metric("Weekly Goals", stats['weekly_goals'])
    
    with col3:
        st.metric("Monthly Goals", stats['monthly_goals'])
    
    # Goal lists
    tab1, tab2, tab3, tab4, tab5 = st.tabs(["Today's Goals", "Weekly Goals", "Monthly Goals", "Overdue Goals", "All Goals"])
    
    with tab1:
        st.subheader("📅 Today's Goals")
        todays_goals = get_todays_goals()
        
        if todays_goals:
            # Calculate progress for today's goals
            today_progress = calculate_goal_progress(todays_goals)
            st.progress(today_progress / 100)
            st.caption(f"Today's Progress: {today_progress:.1f}%")
            
            for goal in todays_goals:
                col1, col2, col3 = st.columns([3, 1, 1])
                
                with col1:
                    st.markdown(f"**{goal['title']}**")
                    st.caption(f"{goal['timeframe']} • {goal['priority']} Priority")
                    if goal.get('description'):
                        st.caption(goal['description'])
                
                with col2:
                    if not goal.get('completed', False):
                        if st.button("✅ Complete", key=f"complete_goal_{goal['id']}"):
                            mark_goal_complete(goal['id'])
                            st.success("Goal completed!")
                            st.rerun()
                
                with col3:
                    if st.button("🗑️ Delete", key=f"delete_goal_{goal['id']}"):
                        delete_goal(goal['id'])
                        st.success("Goal deleted!")
                        st.rerun()
                
                st.divider()
        else:
            st.info("No goals due today! 🎉")
    
    with tab2:
        st.subheader("📅 Weekly Goals")
        weekly_goals = get_weekly_goals()
        
        if weekly_goals:
            # Calculate progress for weekly goals
            weekly_progress = calculate_goal_progress(weekly_goals)
            st.progress(weekly_progress / 100)
            st.caption(f"Weekly Progress: {weekly_progress:.1f}%")
            
            for goal in weekly_goals:
                col1, col2, col3 = st.columns([3, 1, 1])
                
                with col1:
                    st.markdown(f"**{goal['title']}**")
                    deadline = datetime.fromisoformat(goal['deadline']).strftime("%b %d, %Y")
                    st.caption(f"{goal['timeframe']} • {goal['priority']} Priority • Due: {deadline}")
                    if goal.get('description'):
                        st.caption(goal['description'])
                
                with col2:
                    if not goal.get('completed', False):
                        if st.button("✅ Complete", key=f"complete_week_{goal['id']}"):
                            mark_goal_complete(goal['id'])
                            st.success("Goal completed!")
                            st.rerun()
                
                with col3:
                    if st.button("🗑️ Delete", key=f"delete_week_{goal['id']}"):
                        delete_goal(goal['id'])
                        st.success("Goal deleted!")
                        st.rerun()
                
                st.divider()
        else:
            st.info("No weekly goals! 📅")
    
    with tab3:
        st.subheader("📅 Monthly Goals")
        monthly_goals = get_monthly_goals()
        
        if monthly_goals:
            # Calculate progress for monthly goals
            monthly_progress = calculate_goal_progress(monthly_goals)
            st.progress(monthly_progress / 100)
            st.caption(f"Monthly Progress: {monthly_progress:.1f}%")
            
            for goal in monthly_goals:
                col1, col2, col3 = st.columns([3, 1, 1])
                
                with col1:
                    st.markdown(f"**{goal['title']}**")
                    deadline = datetime.fromisoformat(goal['deadline']).strftime("%b %d, %Y")
                    st.caption(f"{goal['timeframe']} • {goal['priority']} Priority • Due: {deadline}")
                    if goal.get('description'):
                        st.caption(goal['description'])
                
                with col2:
                    if not goal.get('completed', False):
                        if st.button("✅ Complete", key=f"complete_month_{goal['id']}"):
                            mark_goal_complete(goal['id'])
                            st.success("Goal completed!")
                            st.rerun()
                
                with col3:
                    if st.button("🗑️ Delete", key=f"delete_month_{goal['id']}"):
                        delete_goal(goal['id'])
                        st.success("Goal deleted!")
                        st.rerun()
                
                st.divider()
        else:
            st.info("No monthly goals! 📅")
    
    with tab4:
        st.subheader("⚠️ Overdue Goals")
        overdue_goals = get_overdue_goals()
        
        if overdue_goals:
            for goal in overdue_goals:
                col1, col2, col3 = st.columns([3, 1, 1])
                
                with col1:
                    st.markdown(f"**{goal['title']}**")
                    deadline = datetime.fromisoformat(goal['deadline']).strftime("%b %d, %Y")
                    st.caption(f"{goal['timeframe']} • {goal['priority']} Priority • Overdue since {deadline}")
                    if goal.get('description'):
                        st.caption(goal['description'])
                
                with col2:
                    if st.button("✅ Complete", key=f"complete_overdue_{goal['id']}"):
                        mark_goal_complete(goal['id'])
                        st.success("Goal completed!")
                        st.rerun()
                
                with col3:
                    if st.button("🗑️ Delete", key=f"delete_overdue_{goal['id']}"):
                        delete_goal(goal['id'])
                        st.success("Goal deleted!")
                        st.rerun()
                
                st.divider()
        else:
            st.info("No overdue goals! 🎉")
    
    with tab5:
        st.subheader("📋 All Goals")
        all_goals = load_goals()
        
        if all_goals:
            # Filter options
            col1, col2 = st.columns(2)
            
            with col1:
                timeframe_filter = st.selectbox(
                    "Filter by Timeframe",
                    ["All", "Daily", "Weekly", "Monthly"]
                )
            
            with col2:
                status_filter = st.selectbox(
                    "Filter by Status",
                    ["All", "Completed", "Pending"]
                )
            
            # Apply filters
            filtered_goals = all_goals
            
            if timeframe_filter != "All":
                filtered_goals = [g for g in filtered_goals if g.get('timeframe') == timeframe_filter]
            
            if status_filter == "Completed":
                filtered_goals = [g for g in filtered_goals if g.get('completed', False)]
            elif status_filter == "Pending":
                filtered_goals = [g for g in filtered_goals if not g.get('completed', False)]
            
            # Display filtered goals
            for goal in filtered_goals:
                col1, col2, col3 = st.columns([3, 1, 1])
                
                with col1:
                    status_emoji = "✅" if goal.get('completed', False) else "⏳"
                    st.markdown(f"{status_emoji} **{goal['title']}**")
                    deadline = datetime.fromisoformat(goal['deadline']).strftime("%b %d, %Y")
                    st.caption(f"{goal['timeframe']} • {goal['priority']} Priority • Due: {deadline}")
                    if goal.get('description'):
                        st.caption(goal['description'])
                
                with col2:
                    if not goal.get('completed', False):
                        if st.button("✅ Complete", key=f"complete_all_{goal['id']}"):
                            mark_goal_complete(goal['id'])
                            st.success("Goal completed!")
                            st.rerun()
                
                with col3:
                    if st.button("🗑️ Delete", key=f"delete_all_{goal['id']}"):
                        delete_goal(goal['id'])
                        st.success("Goal deleted!")
                        st.rerun()
                
                st.divider()
        else:
            st.info("No goals created yet. Add your first goal above! 🎯")
    
    # AI Insights Section
    st.subheader("🤖 AI Goal Insights")
    
    all_goals = load_goals()
    
    if all_goals:
        if st.button("🔍 Generate Goal Insights", type="secondary"):
            with st.spinner("Analyzing your goal patterns..."):
                insight_content = generate_goal_insights(all_goals)
                
                if insight_content and not insight_content.startswith("Error"):
                    # Save the insight
                    save_goal_insight(insight_content, len(all_goals))
                    st.success("✅ Goal insights generated and saved!")
                
                st.markdown(f'<div class="insight-card"><strong>🤖 Goal Analysis:</strong><br>{insight_content}</div>', unsafe_allow_html=True)
    else:
        st.info("Add some goals to generate AI insights!")
    
    # Display past goal insights
    st.subheader("📊 Previous Goal Insights")
    
    goal_insights = get_goal_insights()
    if goal_insights:
        for insight in goal_insights[-3:]:  # Show last 3 insights
            timestamp = datetime.fromisoformat(insight['timestamp'])
            date_str = timestamp.strftime("%B %d, %Y at %I:%M %p")
            st.markdown(f'<div class="insight-card"><strong>📊 Goal Analysis - {date_str}:</strong><br>{insight.get("content", "No content")}</div>', unsafe_allow_html=True)
    else:
        st.info("No goal insights generated yet. Generate your first insight!")

def meal_planning_page():
    st.markdown('<h2 class="section-header">🍽️ Meal Planning</h2>', unsafe_allow_html=True)
    
    # Initialize session state for IDs
    if 'recipe_id_counter' not in st.session_state:
        st.session_state.recipe_id_counter = 0
    
    # Tabs for different sections
    tab1, tab2, tab3, tab4 = st.tabs(["📅 Weekly Meal Plan", "📖 Recipe Book", "🛒 Grocery List", "🤖 AI Recommendations"])
    
    with tab1:
        st.subheader("📅 Weekly Meal Plan")
        
        # Week selection
        col1, col2 = st.columns(2)
        
        with col1:
            week_start = st.date_input(
                "Week Starting",
                value=date.today() - timedelta(days=date.today().weekday()),
                help="Select the start of the week for meal planning"
            )
        
        with col2:
            current_plan = get_current_week_plan()
            if current_plan:
                st.info(f"📋 Current week plan: {len(current_plan.get('meals', {}))} days planned")
            else:
                st.info("📋 No meal plan for this week yet")
        
        # Get week dates
        week_dates = get_week_dates(week_start)
        
        # Meal planning interface
        st.subheader("🍽️ Plan Your Meals")
        
        # Create meal plan structure
        meals = {}
        
        for day_info in week_dates:
            day_key = day_info['date_str']
            day_name = day_info['day_name']
            display_date = day_info['display_date']
            
            st.markdown(f"**{day_name}, {display_date}**")
            
            col1, col2, col3 = st.columns(3)
            
            with col1:
                breakfast = st.text_input(
                    "Breakfast",
                    key=f"breakfast_{day_key}",
                    placeholder="e.g., Oatmeal with berries"
                )
            
            with col2:
                lunch = st.text_input(
                    "Lunch",
                    key=f"lunch_{day_key}",
                    placeholder="e.g., Grilled chicken salad"
                )
            
            with col3:
                dinner = st.text_input(
                    "Dinner",
                    key=f"dinner_{day_key}",
                    placeholder="e.g., Salmon with vegetables"
                )
            
            # Store meals for this day
            day_meals = {}
            if breakfast:
                day_meals['breakfast'] = {'meal': breakfast, 'type': 'breakfast'}
            if lunch:
                day_meals['lunch'] = {'meal': lunch, 'type': 'lunch'}
            if dinner:
                day_meals['dinner'] = {'meal': dinner, 'type': 'dinner'}
            
            if day_meals:
                meals[day_key] = day_meals
            
            st.divider()
        
        # Save meal plan
        if st.button("💾 Save Meal Plan", type="primary"):
            if meals:
                meal_plan = create_weekly_meal_plan(week_start, meals)
                save_meal_plan(meal_plan)
                st.success("✅ Meal plan saved successfully!")
                st.rerun()
            else:
                st.warning("Please add at least one meal to save the plan.")
        
        # Display current meal plan
        if current_plan:
            st.subheader("📋 Current Week's Plan")
            
            current_meals = current_plan.get('meals', {})
            for day_key, day_meals in current_meals.items():
                try:
                    day_date = datetime.fromisoformat(day_key).date()
                    day_name = day_date.strftime('%A')
                    display_date = day_date.strftime('%b %d')
                    
                    st.markdown(f"**{day_name}, {display_date}**")
                    
                    for meal_type, meal_data in day_meals.items():
                        meal_name = meal_data.get('meal', 'No meal planned')
                        st.markdown(f"- **{meal_type.title()}**: {meal_name}")
                    
                    st.divider()
                except (ValueError, TypeError):
                    continue
    
    with tab2:
        st.subheader("📖 Recipe Book")
        
        # Recipe creation form
        with st.expander("➕ Add New Recipe", expanded=False):
            col1, col2 = st.columns(2)
            
            with col1:
                recipe_title = st.text_input("Recipe Title")
                recipe_prep_time = st.text_input("Prep Time", placeholder="e.g., 15 minutes")
                recipe_cook_time = st.text_input("Cook Time", placeholder="e.g., 30 minutes")
                recipe_servings = st.number_input("Servings", min_value=1, value=4)
            
            with col2:
                recipe_ingredients = st.text_area(
                    "Ingredients (one per line)",
                    placeholder="2 cups flour\n1 cup sugar\n3 eggs\n..."
                )
                recipe_steps = st.text_area(
                    "Steps (one per line)",
                    placeholder="1. Preheat oven to 350°F\n2. Mix dry ingredients\n3. Add wet ingredients\n..."
                )
            
            if st.button("💾 Save Recipe", type="secondary"):
                if recipe_title and recipe_ingredients and recipe_steps:
                    # Generate unique recipe ID
                    st.session_state.recipe_id_counter += 1
                    recipe_id = f"recipe_{st.session_state.recipe_id_counter}"
                    
                    # Parse ingredients and steps
                    ingredients_list = [ing.strip() for ing in recipe_ingredients.split('\n') if ing.strip()]
                    steps_list = [step.strip() for step in recipe_steps.split('\n') if step.strip()]
                    
                    recipe = {
                        'id': recipe_id,
                        'title': recipe_title,
                        'prep_time': recipe_prep_time,
                        'cook_time': recipe_cook_time,
                        'servings': recipe_servings,
                        'ingredients': ingredients_list,
                        'steps': steps_list
                    }
                    
                    save_recipe(recipe)
                    st.success("✅ Recipe saved successfully!")
                    st.rerun()
                else:
                    st.error("Please fill in title, ingredients, and steps.")
        
        # Recipe search
        search_query = st.text_input("🔍 Search Recipes", placeholder="Search by title or ingredients...")
        
        # Display recipes
        recipes = load_recipes()
        
        if search_query:
            recipes = search_recipes(search_query)
        
        if recipes:
            st.subheader(f"📖 Recipes ({len(recipes)} found)")
            
            for recipe in recipes:
                with st.expander(f"📖 {recipe['title']}", expanded=False):
                    st.markdown(format_recipe_for_display(recipe))
                    
                    col1, col2 = st.columns(2)
                    
                    with col1:
                        if st.button("✏️ Edit", key=f"edit_recipe_{recipe['id']}"):
                            st.session_state.editing_recipe = recipe['id']
                    
                    with col2:
                        if st.button("🗑️ Delete", key=f"delete_recipe_{recipe['id']}"):
                            delete_recipe(recipe['id'])
                            st.success("Recipe deleted!")
                            st.rerun()
        else:
            st.info("No recipes found. Add your first recipe above!")
    
    with tab3:
        st.subheader("🛒 Grocery List")
        
        # Get current meal plan
        current_plan = get_current_week_plan()
        
        if current_plan:
            # Generate grocery list
            recipes = load_recipes()
            grocery_items = generate_grocery_list(current_plan, recipes)
            
            if grocery_items:
                st.subheader(f"📋 Grocery List ({len(grocery_items)} items)")
                
                # Display grocery items
                for i, item in enumerate(grocery_items, 1):
                    st.markdown(f"{i}. {item}")
                
                # Export options
                col1, col2 = st.columns(2)
                
                with col1:
                    if st.button("📄 Copy to Clipboard"):
                        grocery_text = "\n".join([f"{i}. {item}" for i, item in enumerate(grocery_items, 1)])
                        st.code(grocery_text)
                        st.success("Grocery list copied to clipboard!")
                
                with col2:
                    if st.button("📱 Send to Phone"):
                        st.info("SMS/Email functionality coming soon!")
            else:
                st.info("No grocery items found. Add meals with ingredients to generate a list.")
        else:
            st.info("No meal plan found. Create a meal plan first to generate a grocery list.")
    
    with tab4:
        st.subheader("🤖 AI Meal Recommendations")
        
        # Get food journal entries for analysis
        from utils.data_utils import load_food_entries
        food_entries = load_food_entries()
        
        if food_entries:
            # Current symptoms input
            current_symptoms = st.text_input(
                "Current Symptoms (optional)",
                placeholder="e.g., bloating, fatigue, headache"
            )
            
            symptoms_list = []
            if current_symptoms:
                symptoms_list = [s.strip() for s in current_symptoms.split(',')]
            
            if st.button("🔍 Generate Meal Recommendations", type="secondary"):
                with st.spinner("Analyzing your food patterns and generating recommendations..."):
                    recommendations = generate_meal_recommendations(food_entries, symptoms_list)
                    
                    if recommendations and not recommendations.startswith("Error"):
                        # Save the insight
                        save_meal_insight(recommendations, len(food_entries))
                        st.success("✅ Meal recommendations generated and saved!")
                    
                    st.markdown(f'<div class="insight-card"><strong>🤖 Meal Recommendations:</strong><br>{recommendations}</div>', unsafe_allow_html=True)
        else:
            st.info("No food journal entries found. Log some meals first to get personalized recommendations!")
        
        # Display past meal insights
        st.subheader("📊 Previous Meal Insights")
        
        meal_insights = get_meal_insights()
        if meal_insights:
            for insight in meal_insights[-3:]:  # Show last 3 insights
                timestamp = datetime.fromisoformat(insight['timestamp'])
                date_str = timestamp.strftime("%B %d, %Y at %I:%M %p")
                st.markdown(f'<div class="insight-card"><strong>📊 Meal Analysis - {date_str}:</strong><br>{insight.get("content", "No content")}</div>', unsafe_allow_html=True)
        else:
            st.info("No meal insights generated yet. Generate your first recommendation!")

def selfcare_page():
    st.markdown('<h2 class="section-header">🧘‍♀️ Self-Care Scheduler</h2>', unsafe_allow_html=True)
    
    # Initialize session state for task ID counter
    if 'selfcare_id_counter' not in st.session_state:
        st.session_state.selfcare_id_counter = 0
    
    # Self-care task creation form
    st.subheader("➕ Add New Self-Care Task")
    
    col1, col2 = st.columns(2)
    
    with col1:
        task_title = st.text_input(
            "Task Title",
            placeholder="e.g., Morning skincare routine"
        )
        
        task_category = st.selectbox(
            "Category",
            ["Grooming", "Cleaning", "Health", "Wellness", "Laundry", "Hygiene"]
        )
        
        task_frequency = st.selectbox(
            "Frequency",
            ["Daily", "Weekly", "Monthly"]
        )
    
    with col2:
        task_description = st.text_area(
            "Description (Optional)",
            placeholder="Add task details..."
        )
        
        task_time = st.time_input(
            "Scheduled Time",
            value=datetime.now().time()
        )
        
        # Additional scheduling options based on frequency
        if task_frequency == "Weekly":
            task_day = st.selectbox(
                "Day of Week",
                ["Monday", "Tuesday", "Wednesday", "Thursday", "Friday", "Saturday", "Sunday"]
            )
        elif task_frequency == "Monthly":
            task_day_of_month = st.number_input(
                "Day of Month",
                min_value=1,
                max_value=31,
                value=1
            )
    
    # Add task button
    if st.button("💾 Add Self-Care Task", type="primary"):
        if not task_title:
            st.error("Please enter a task title.")
        else:
            # Generate unique task ID
            st.session_state.selfcare_id_counter += 1
            task_id = f"selfcare_{st.session_state.selfcare_id_counter}"
            
            # Create task
            task = {
                'id': task_id,
                'title': task_title,
                'category': task_category,
                'description': task_description,
                'frequency': task_frequency,
                'scheduled_time': task_time.strftime("%H:%M"),
                'completions': []
            }
            
            # Add frequency-specific scheduling
            if task_frequency == "Weekly":
                # Calculate the next occurrence of the selected day
                today = date.today()
                day_names = ["Monday", "Tuesday", "Wednesday", "Thursday", "Friday", "Saturday", "Sunday"]
                target_day = day_names.index(task_day)
                current_day = today.weekday()
                days_until = (target_day - current_day) % 7
                if days_until == 0:
                    days_until = 7
                scheduled_date = today + timedelta(days=days_until)
                task['scheduled_day'] = scheduled_date.isoformat()
            
            elif task_frequency == "Monthly":
                task['scheduled_day_of_month'] = task_day_of_month
            
            # Save task
            save_selfcare_task(task)
            st.success("✅ Self-care task added successfully!")
            st.rerun()
    
    # Self-care overview
    st.subheader("📊 Self-Care Overview")
    
    # Get self-care statistics
    stats = get_selfcare_statistics()
    
    col1, col2, col3, col4 = st.columns(4)
    
    with col1:
        st.metric("Total Tasks", stats['total_tasks'])
    
    with col2:
        st.metric("Total Completions", stats['total_completions'])
    
    with col3:
        st.metric("Overdue Tasks", stats['overdue_tasks'])
    
    with col4:
        st.metric("Completion Rate", f"{stats['completion_rate']:.1f}%")
    
    # Task breakdown by frequency
    st.subheader("📈 Task Breakdown")
    
    col1, col2, col3 = st.columns(3)
    
    with col1:
        st.metric("Daily Tasks", stats['daily_tasks'])
    
    with col2:
        st.metric("Weekly Tasks", stats['weekly_tasks'])
    
    with col3:
        st.metric("Monthly Tasks", stats['monthly_tasks'])
    
    # Task lists
    tab1, tab2, tab3, tab4 = st.tabs(["Today's Tasks", "Upcoming Tasks", "Overdue Tasks", "All Tasks"])
    
    with tab1:
        st.subheader("📅 Today's Self-Care Tasks")
        todays_tasks = get_todays_selfcare_tasks()
        
        if todays_tasks:
            for task in todays_tasks:
                col1, col2, col3, col4 = st.columns([3, 1, 1, 1])
                
                with col1:
                    st.markdown(f"**{task['title']}**")
                    st.caption(f"{task['category']} • {task['frequency']} • {task['scheduled_time']}")
                    if task.get('description'):
                        st.caption(task['description'])
                    
                    # Show completion status
                    status = get_selfcare_task_completion_status(task)
                    st.caption(f"Status: {status}")
                
                with col2:
                    if st.button("✅ Complete", key=f"complete_selfcare_{task['id']}"):
                        mark_selfcare_task_complete(task['id'])
                        st.success("Task completed!")
                        st.rerun()
                
                with col3:
                    if st.button("📝 Edit", key=f"edit_selfcare_{task['id']}"):
                        st.session_state.editing_selfcare = task['id']
                
                with col4:
                    if st.button("🗑️ Delete", key=f"delete_selfcare_{task['id']}"):
                        delete_selfcare_task(task['id'])
                        st.success("Task deleted!")
                        st.rerun()
                
                st.divider()
        else:
            st.info("No self-care tasks scheduled for today! 🎉")
    
    with tab2:
        st.subheader("📅 Upcoming Self-Care Tasks")
        upcoming_tasks = get_upcoming_selfcare_tasks(7)  # Next 7 days
        
        if upcoming_tasks:
            for task in upcoming_tasks:
                col1, col2, col3, col4 = st.columns([3, 1, 1, 1])
                
                with col1:
                    st.markdown(f"**{task['title']}**")
                    next_date = datetime.fromisoformat(task['next_occurrence']).strftime("%b %d, %Y")
                    st.caption(f"{task['category']} • {task['frequency']} • {task['scheduled_time']} • Next: {next_date}")
                    if task.get('description'):
                        st.caption(task['description'])
                
                with col2:
                    if st.button("✅ Complete", key=f"complete_upcoming_{task['id']}"):
                        mark_selfcare_task_complete(task['id'])
                        st.success("Task completed!")
                        st.rerun()
                
                with col3:
                    if st.button("📝 Edit", key=f"edit_upcoming_{task['id']}"):
                        st.session_state.editing_upcoming = task['id']
                
                with col4:
                    if st.button("🗑️ Delete", key=f"delete_upcoming_{task['id']}"):
                        delete_selfcare_task(task['id'])
                        st.success("Task deleted!")
                        st.rerun()
                
                st.divider()
        else:
            st.info("No upcoming self-care tasks! 📅")
    
    with tab3:
        st.subheader("⚠️ Overdue Self-Care Tasks")
        overdue_tasks = get_overdue_selfcare_tasks()
        
        if overdue_tasks:
            for task in overdue_tasks:
                col1, col2, col3, col4 = st.columns([3, 1, 1, 1])
                
                with col1:
                    st.markdown(f"**{task['title']}**")
                    st.caption(f"{task['category']} • {task['frequency']} • {task['scheduled_time']} • OVERDUE")
                    if task.get('description'):
                        st.caption(task['description'])
                
                with col2:
                    if st.button("✅ Complete", key=f"complete_overdue_{task['id']}"):
                        mark_selfcare_task_complete(task['id'])
                        st.success("Task completed!")
                        st.rerun()
                
                with col3:
                    if st.button("📝 Edit", key=f"edit_overdue_{task['id']}"):
                        st.session_state.editing_overdue = task['id']
                
                with col4:
                    if st.button("🗑️ Delete", key=f"delete_overdue_{task['id']}"):
                        delete_selfcare_task(task['id'])
                        st.success("Task deleted!")
                        st.rerun()
                
                st.divider()
        else:
            st.info("No overdue self-care tasks! 🎉")
    
    with tab4:
        st.subheader("📋 All Self-Care Tasks")
        all_tasks = load_selfcare_tasks()
        
        if all_tasks:
            # Filter options
            col1, col2 = st.columns(2)
            
            with col1:
                category_filter = st.selectbox(
                    "Filter by Category",
                    ["All", "Grooming", "Cleaning", "Health", "Wellness", "Laundry", "Hygiene"]
                )
            
            with col2:
                frequency_filter = st.selectbox(
                    "Filter by Frequency",
                    ["All", "Daily", "Weekly", "Monthly"]
                )
            
            # Apply filters
            filtered_tasks = all_tasks
            
            if category_filter != "All":
                filtered_tasks = [t for t in filtered_tasks if t.get('category') == category_filter]
            
            if frequency_filter != "All":
                filtered_tasks = [t for t in filtered_tasks if t.get('frequency') == frequency_filter]
            
            # Display filtered tasks
            for task in filtered_tasks:
                col1, col2, col3, col4 = st.columns([3, 1, 1, 1])
                
                with col1:
                    status_emoji = "✅" if get_selfcare_task_completion_status(task).startswith("Completed") else "⏳"
                    st.markdown(f"{status_emoji} **{task['title']}**")
                    st.caption(f"{task['category']} • {task['frequency']} • {task['scheduled_time']}")
                    if task.get('description'):
                        st.caption(task['description'])
                    
                    # Show completion status
                    status = get_selfcare_task_completion_status(task)
                    st.caption(f"Status: {status}")
                
                with col2:
                    if st.button("✅ Complete", key=f"complete_all_{task['id']}"):
                        mark_selfcare_task_complete(task['id'])
                        st.success("Task completed!")
                        st.rerun()
                
                with col3:
                    if st.button("📝 Edit", key=f"edit_all_{task['id']}"):
                        st.session_state.editing_all = task['id']
                
                with col4:
                    if st.button("🗑️ Delete", key=f"delete_all_{task['id']}"):
                        delete_selfcare_task(task['id'])
                        st.success("Task deleted!")
                        st.rerun()
                
                st.divider()
        else:
            st.info("No self-care tasks created yet. Add your first task above! 🧘‍♀️")
    
    # AI Insights Section
    st.subheader("🤖 AI Self-Care Insights")
    
    all_tasks = load_selfcare_tasks()
    
    if all_tasks:
        if st.button("🔍 Generate Self-Care Insights", type="secondary"):
            with st.spinner("Analyzing your self-care patterns..."):
                insight_content = generate_selfcare_insights(all_tasks)
                
                if insight_content and not insight_content.startswith("Error"):
                    # Save the insight
                    save_selfcare_insight(insight_content, len(all_tasks))
                    st.success("✅ Self-care insights generated and saved!")
                
                st.markdown(f'<div class="insight-card"><strong>🤖 Self-Care Analysis:</strong><br>{insight_content}</div>', unsafe_allow_html=True)
    else:
        st.info("Add some self-care tasks to generate AI insights!")
    
    # Display past self-care insights
    st.subheader("📊 Previous Self-Care Insights")
    
    selfcare_insights = get_selfcare_insights()
    if selfcare_insights:
        for insight in selfcare_insights[-3:]:  # Show last 3 insights
            timestamp = datetime.fromisoformat(insight['timestamp'])
            date_str = timestamp.strftime("%B %d, %Y at %I:%M %p")
            st.markdown(f'<div class="insight-card"><strong>📊 Self-Care Analysis - {date_str}:</strong><br>{insight.get("content", "No content")}</div>', unsafe_allow_html=True)
    else:
        st.info("No self-care insights generated yet. Generate your first insight!")

def analytics_page():
    st.markdown('<h2 class="section-header">📊 Analytics & Trends</h2>', unsafe_allow_html=True)
    
    # Date range selector with preset options
    st.subheader("📅 Select Date Range for Analysis")
    
    # Preset date ranges
    preset_option = st.selectbox(
        "Choose a preset or custom range:",
        ["Last 7 days", "Last 30 days", "Last 3 months", "Last 6 months", "Last year", "Custom range"]
    )
    
    # Calculate dates based on preset
    today = date.today()
    
    if preset_option == "Last 7 days":
        start_date = today - timedelta(days=7)
        end_date = today
    elif preset_option == "Last 30 days":
        start_date = today - timedelta(days=30)
        end_date = today
    elif preset_option == "Last 3 months":
        start_date = today - timedelta(days=90)
        end_date = today
    elif preset_option == "Last 6 months":
        start_date = today - timedelta(days=180)
        end_date = today
    elif preset_option == "Last year":
        start_date = today - timedelta(days=365)
        end_date = today
    else:  # Custom range
        col1, col2 = st.columns(2)
        with col1:
            start_date = st.date_input("Start Date", value=today - timedelta(days=7))
        with col2:
            end_date = st.date_input("End Date", value=today)
    
    # Display selected date range
    st.info(f"📅 Analyzing data from **{start_date.strftime('%B %d, %Y')}** to **{end_date.strftime('%B %d, %Y')}**")
    
    # Get entries for the selected date range
    entries = get_entries_by_date_range(start_date.isoformat(), end_date.isoformat())
    
    if entries:
        st.subheader(f"📈 Summary Statistics ({len(entries)} entries)")
        
        # Create summary statistics
        meal_types = [entry.get('meal_type', 'Unknown') for entry in entries]
        all_foods = []
        all_symptoms = []
        all_supplements = []
        
        for entry in entries:
            all_foods.extend(entry.get('food_items', []))
            all_symptoms.extend(entry.get('symptoms', []))
            all_supplements.extend(entry.get('supplements', []))
        
        # Display statistics in a more organized way
        col1, col2, col3, col4 = st.columns(4)
        
        with col1:
            st.metric("📊 Total Entries", len(entries))
            st.metric("🍽️ Unique Foods", len(set(all_foods)))
        
        with col2:
            st.metric("⚠️ Symptoms", len(set(all_symptoms)))
            st.metric("💊 Supplements", len(set(all_supplements)))
        
        with col3:
            most_common_meal = max(set(meal_types), key=meal_types.count) if meal_types else "None"
            st.metric("🏆 Most Common Meal", most_common_meal)
            
            # Calculate average meals per day
            if len(entries) > 0:
                date_range_days = (end_date - start_date).days + 1
                avg_meals_per_day = len(entries) / date_range_days
                st.metric("📅 Avg Meals/Day", f"{avg_meals_per_day:.1f}")
        
        with col4:
            # Calculate completion rate
            total_possible_meals = (end_date - start_date).days * 3  # 3 meals per day
            completion_rate = (len(entries) / total_possible_meals) * 100 if total_possible_meals > 0 else 0
            st.metric("📈 Completion Rate", f"{completion_rate:.1f}%")
            
            # Days with entries
            unique_days = len(set(entry.get('date', '') for entry in entries))
            st.metric("📅 Days with Entries", unique_days)
        
        # Additional analysis
        st.subheader("🔍 Detailed Analysis")
        
        # Food frequency analysis
        if all_foods:
            food_counts = {}
            for food in all_foods:
                food_counts[food] = food_counts.get(food, 0) + 1
            
            # Top 10 most eaten foods
            top_foods = sorted(food_counts.items(), key=lambda x: x[1], reverse=True)[:10]
            
            col1, col2 = st.columns(2)
            
            with col1:
                st.markdown("**🍽️ Top 10 Most Eaten Foods**")
                for i, (food, count) in enumerate(top_foods, 1):
                    st.markdown(f"{i}. **{food}** - {count} times")
            
            with col2:
                st.markdown("**⚠️ Symptoms Analysis**")
                if all_symptoms:
                    symptom_counts = {}
                    for symptom in all_symptoms:
                        symptom_counts[symptom] = symptom_counts.get(symptom, 0) + 1
                    
                    top_symptoms = sorted(symptom_counts.items(), key=lambda x: x[1], reverse=True)[:5]
                    for i, (symptom, count) in enumerate(top_symptoms, 1):
                        st.markdown(f"{i}. **{symptom}** - {count} times")
                else:
                    st.markdown("No symptoms recorded in this period")
        
        # Meal type distribution
        st.subheader("📊 Meal Type Distribution")
        if meal_types:
            meal_counts = {}
            for meal in meal_types:
                meal_counts[meal] = meal_counts.get(meal, 0) + 1
            
            col1, col2, col3 = st.columns(3)
            for i, (meal_type, count) in enumerate(meal_counts.items()):
                with [col1, col2, col3][i % 3]:
                    st.metric(f"{meal_type}", count)
        
        # Display detailed entries
        st.subheader("📋 Detailed Entries")
        
        # Add search/filter functionality
        search_term = st.text_input("🔍 Search entries (food, symptoms, notes):", placeholder="Enter search term...")
        
        filtered_entries = entries
        if search_term:
            search_term = search_term.lower()
            filtered_entries = []
            for entry in entries:
                food_items = ' '.join(entry.get('food_items', [])).lower()
                symptoms = ' '.join(entry.get('symptoms', [])).lower()
                notes = entry.get('notes', '').lower()
                
                if search_term in food_items or search_term in symptoms or search_term in notes:
                    filtered_entries.append(entry)
        
        if filtered_entries:
            st.info(f"Showing {len(filtered_entries)} entries (filtered from {len(entries)} total)")
            
            for entry in filtered_entries:
                st.markdown(f'<div class="entry-card">{format_entry_for_display(entry)}</div>', unsafe_allow_html=True)
        else:
            if search_term:
                st.warning(f"No entries found matching '{search_term}'")
            else:
                st.info("No entries to display")
    
    else:
        st.warning(f"❌ No food journal entries found for the selected date range ({start_date.strftime('%B %d, %Y')} to {end_date.strftime('%B %d, %Y')})")
        st.info("💡 Try selecting a different date range or add some food entries first!")

def settings_page():
    st.markdown('<h2 class="section-header">⚙️ Settings</h2>', unsafe_allow_html=True)
    
    st.subheader("API Configuration")
    
    # OpenAI API Key configuration
    openai_api_key = st.text_input(
        "OpenAI API Key",
        type="password",
        help="Enter your OpenAI API key to enable AI insights generation"
    )
    
    if openai_api_key:
        st.success("✅ OpenAI API key configured")
    
    # GROQ API Key configuration
    groq_api_key = st.text_input(
        "GROQ API Key",
        type="password",
        help="Enter your GROQ API key to enable task management insights"
    )
    
    if groq_api_key:
        st.success("✅ GROQ API key configured")
    
    st.subheader("Data Management")
    
    col1, col2 = st.columns(2)
    
    with col1:
        if st.button("📥 Export Data"):
            # Export functionality would go here
            st.info("Export functionality coming soon!")
    
    with col2:
        if st.button("🗑️ Clear All Data"):
            if st.checkbox("I understand this will delete all my data"):
                # Clear data functionality would go here
                st.warning("Clear data functionality coming soon!")

if __name__ == "__main__":
    main()
