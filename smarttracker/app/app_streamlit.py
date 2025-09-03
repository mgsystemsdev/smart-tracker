"""
Smart Tracker Streamlit Web Application.

A web-based interface for the Smart Tracker application using Streamlit.
"""

import streamlit as st
import pandas as pd
from datetime import date
from smarttracker import __version__

def show_home_page():
    """Display the home page content."""
    col1, col2, col3 = st.columns([1, 2, 1])
    
    with col2:
        st.markdown("## Hello, world! 👋")
        st.markdown("""
        Welcome to Smart Tracker! This is the foundation of your tracking application.
        
        ### Ready for Development
        - ✅ Streamlit web interface
        - ✅ Typer CLI interface  
        - ✅ Organized package structure
        - ✅ Domain and app layers
        - ✅ Testing framework ready
        
        ### Next Steps
        1. Implement your tracking models in `smarttracker/domain/`
        2. Add business logic and services
        3. Expand the web interface with tracking features
        4. Enhance the CLI with tracking commands
        5. Add comprehensive tests
        """)
        
        # Interactive demo section
        st.markdown("### Quick Demo")
        col_demo1, col_demo2, col_demo3 = st.columns(3)
        
        with col_demo1:
            if st.button("🎉 Click me!", type="primary"):
                st.balloons()
                st.success("Smart Tracker is working perfectly!")
        
        with col_demo2:
            if st.button("📚 Open Clean Dashboard", help="Opens the Clean Dashboard for learning session tracking"):
                st.session_state.current_page = "clean_dashboard"
                st.rerun()
        
        with col_demo3:
            if st.button("🎓 Smart Learning Tracker", help="Opens the Smart Learning Tracker Desktop app"):
                st.session_state.current_page = "learning_tracker"
                st.rerun()
        
        # Info about the application
        with st.expander("📖 About This Application"):
            st.markdown("""
            This Smart Tracker application is built with:
            - **Streamlit** for the web interface
            - **Typer** for the command-line interface
            - **Pydantic** for data validation (ready to use)
            - **Python 3.11+** compatibility
            
            The application follows a clean architecture with separated concerns:
            - `domain/` - Business logic and models
            - `app/` - User interface implementations
            - `cli.py` - Command-line interface
            """)

def show_clean_dashboard():
    """Display the Clean Dashboard interface."""
    st.title("📚 Clean Dashboard - Ready for Enrollers")
    
    # Back button
    if st.button("← Back to Home"):
        st.session_state.current_page = "home"
        st.rerun()
    
    st.markdown("---")
    
    # Main dashboard table
    col1, col2 = st.columns([3, 1])
    
    with col1:
        st.subheader("Learning Sessions")
        
        # Table headers
        headers = ["Date", "Language", "Type", "Work Item Name", "Topic", "Difficulty", "Status", "Tags", "Hours", "Target Time", "Points", "Progress %", "ID", "Notes"]
        
        # Create empty dataframe
        df = pd.DataFrame(columns=headers)
        
        # Display table
        st.dataframe(df, use_container_width=True, height=200)
    
    with col2:
        st.subheader("Quick Actions")
        if st.button("Add", use_container_width=True):
            st.success("Add function would be implemented here")
        if st.button("Save", use_container_width=True):
            st.success("Save function would be implemented here")
        if st.button("Cancel", use_container_width=True):
            st.info("Cancel function would be implemented here")
        if st.button("Clear Filters", use_container_width=True):
            st.info("Filters cleared")
        if st.button("Delete", use_container_width=True):
            st.warning("Delete function would be implemented here")
    
    # Learning Session Entry Form
    st.markdown("---")
    st.subheader("Learning Session Entry")
    
    col_left, col_right = st.columns(2)
    
    with col_left:
        session_date = st.date_input("Date", value=date.today())
        language = st.selectbox("Language", ["Python", "JavaScript", "Java", "C++", "Other"])
        work_item = st.text_input("Work Item", placeholder="Project or resource name...")
        topic = st.text_input("Topic", placeholder="Variables")
        difficulty = st.selectbox("Difficulty", ["Easy", "Medium", "Hard"])
        status = st.selectbox("Status", ["In Progress", "Completed", "Planned"])
    
    with col_right:
        session_type = st.selectbox("Type", ["Reading", "Coding", "Video", "Practice"])
        hours_spent = st.number_input("Hours", min_value=0.0, value=0.0, step=0.1)
        target_hours = st.number_input("Target", min_value=0.0, value=0.0, step=0.1)
        tags = st.text_input("Tags", placeholder="basics")
        progress = st.slider("Progress %", 0, 100, 0)
        notes = st.text_area("Notes", placeholder="Quick notes about this session...")
    
    # Save button
    if st.button("Save Session", type="primary", use_container_width=True):
        st.success("Session saved successfully!")
        st.balloons()
    
    st.info("📊 Records: 0")

def show_learning_tracker():
    """Display the Smart Learning Tracker interface."""
    st.title("🎓 Smart Learning Tracker - Desktop")
    
    # Back button
    if st.button("← Back to Home"):
        st.session_state.current_page = "home"
        st.rerun()
    
    st.markdown("---")
    
    # Create the form layout similar to the desktop app
    col_left, col_main = st.columns([1, 3])
    
    with col_left:
        st.subheader("Session Details")
        
        # Form fields matching the desktop app
        session_date = st.date_input("Session Date", value=date.today())
        language = st.selectbox("Language", ["Python", "JavaScript", "Java", "C#", "Other"])
        work_item = st.text_input("Work Item", placeholder="Enter work item...")
        skill = st.text_input("Skill", placeholder="Enter skill...")
        
        category_type = st.selectbox("Category Type", ["Framework", "Language", "Tool", "Concept"])
        category_name = st.text_input("Category Name", placeholder="Enter category...")
        category_source = st.text_input("Category Source", placeholder="Enter source...")
        
        difficulty = st.selectbox("Difficulty", ["Beginner", "Intermediate", "Advanced"])
        status = st.selectbox("Status", ["In Progress", "Completed", "Planned"])
        
        hours_spent = st.number_input("Hours Spent", min_value=0.0, value=0.0, step=0.1)
        target_hours = st.number_input("Target Hours", min_value=0.0, value=0.0, step=0.1)
        
        tags = st.text_area("Tags", placeholder="Enter tags separated by commas...")
        notes = st.text_area("Notes", placeholder="Additional notes about this session...")
        
        # Save button
        if st.button("Save Session", type="primary", use_container_width=True):
            st.success("Learning session saved!")
            st.balloons()
        
        st.caption("Ready")
    
    with col_main:
        st.subheader("Session Overview")
        
        # Display a table with the session data
        st.markdown("### Current Session Data")
        
        # Create a preview of the current session
        if st.button("Show Session Preview"):
            session_data = {
                "Field": ["Session Date", "Language", "Work Item", "Skill", "Category Type", 
                         "Category Name", "Category Source", "Difficulty", "Status", 
                         "Hours Spent", "Target Hours", "Tags", "Notes"],
                "Value": [str(session_date), language, work_item or "Not set", skill or "Not set",
                         category_type, category_name or "Not set", category_source or "Not set",
                         difficulty, status, hours_spent, target_hours, 
                         tags or "No tags", notes or "No notes"]
            }
            
            df = pd.DataFrame(session_data)
            st.dataframe(df, use_container_width=True, hide_index=True)
        
        # Statistics
        st.markdown("### Quick Stats")
        col1, col2, col3, col4 = st.columns(4)
        
        with col1:
            st.metric("Total Sessions", "0")
        with col2:
            st.metric("Hours Logged", "0.0")
        with col3:
            st.metric("Current Streak", "0 days")
        with col4:
            st.metric("Skills Tracked", "0")

def main():
    """Main Streamlit application function."""
    # Page configuration
    st.set_page_config(
        page_title="Smart Tracker",
        page_icon="📊",
        layout="wide",
        initial_sidebar_state="expanded"
    )
    
    # Initialize session state
    if "current_page" not in st.session_state:
        st.session_state.current_page = "home"
    
    # Main header
    st.title("📊 Smart Tracker")
    st.subheader("Your Personal Tracking Application")
    
    # Version info in sidebar
    with st.sidebar:
        st.info(f"Version: {__version__}")
        st.markdown("---")
        st.markdown("### Navigation")
        
        # Navigation buttons
        if st.button("🏠 Home", use_container_width=True):
            st.session_state.current_page = "home"
            st.rerun()
        
        if st.button("📚 Clean Dashboard", use_container_width=True):
            st.session_state.current_page = "clean_dashboard"
            st.rerun()
            
        if st.button("🎓 Learning Tracker", use_container_width=True):
            st.session_state.current_page = "learning_tracker"
            st.rerun()
        
        st.markdown("---")
        st.markdown("Welcome to Smart Tracker! Use the navigation above to explore different tracking interfaces.")
    
    # Display the appropriate page
    if st.session_state.current_page == "home":
        show_home_page()
    elif st.session_state.current_page == "clean_dashboard":
        show_clean_dashboard()
    elif st.session_state.current_page == "learning_tracker":
        show_learning_tracker()

if __name__ == "__main__":
    main()