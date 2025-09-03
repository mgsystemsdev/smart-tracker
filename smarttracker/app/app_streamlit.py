"""
Smart Tracker Streamlit Web Application.

A web-based interface for the Smart Tracker application using Streamlit.
"""

import streamlit as st
import pandas as pd
from datetime import date
from smarttracker import __version__

def show_home_page():
    """Display the professional home page with MG System Dev branding."""
    
    # Custom CSS for MG System Dev styling
    st.markdown("""
    <style>
    .main-header {
        background: linear-gradient(135deg, #1a1a2e 0%, #16213e 50%, #0f3460 100%);
        padding: 2rem;
        border-radius: 15px;
        margin-bottom: 2rem;
        border: 2px solid #FFD700;
        box-shadow: 0 8px 32px rgba(255, 215, 0, 0.3);
    }
    
    .mg-title {
        font-size: 3rem;
        font-weight: bold;
        color: #FFD700;
        text-align: center;
        margin: 0;
        text-shadow: 2px 2px 4px rgba(0,0,0,0.8);
        letter-spacing: 2px;
    }
    
    .mg-subtitle {
        font-size: 1.2rem;
        color: #C0C0C0;
        text-align: center;
        margin-top: 0.5rem;
        letter-spacing: 1px;
    }
    
    .feature-card {
        background: linear-gradient(145deg, #1a1a2e 0%, #16213e 100%);
        padding: 1.5rem;
        border-radius: 12px;
        border: 1px solid #FFD700;
        margin: 1rem 0;
        box-shadow: 0 4px 15px rgba(255, 215, 0, 0.2);
        transition: transform 0.3s ease;
    }
    
    .feature-card:hover {
        transform: translateY(-5px);
        box-shadow: 0 8px 25px rgba(255, 215, 0, 0.4);
    }
    
    .feature-title {
        color: #FFD700;
        font-size: 1.3rem;
        font-weight: bold;
        margin-bottom: 0.8rem;
        display: flex;
        align-items: center;
    }
    
    .feature-text {
        color: #E8E8E8;
        line-height: 1.6;
    }
    
    .demo-button {
        background: linear-gradient(145deg, #FFD700 0%, #FFA500 100%);
        color: #000;
        border: none;
        padding: 12px 24px;
        border-radius: 8px;
        font-weight: bold;
        font-size: 1rem;
        cursor: pointer;
        transition: all 0.3s ease;
        width: 100%;
        margin: 0.5rem 0;
    }
    
    .demo-button:hover {
        background: linear-gradient(145deg, #FFA500 0%, #FFD700 100%);
        transform: translateY(-2px);
        box-shadow: 0 4px 15px rgba(255, 215, 0, 0.5);
    }
    
    .stats-container {
        background: linear-gradient(135deg, #16213e 0%, #1a1a2e 100%);
        padding: 1.5rem;
        border-radius: 10px;
        border: 1px solid #C0C0C0;
        margin: 1rem 0;
    }
    
    .tech-accent {
        color: #00CED1;
        font-weight: bold;
    }
    </style>
    """, unsafe_allow_html=True)
    
    # Main header section
    st.markdown("""
    <div class="main-header">
        <h1 class="mg-title">MG SMART TRACKER</h1>
        <p class="mg-subtitle">SYSTEM DEV | Professional Development Tracking Platform</p>
    </div>
    """, unsafe_allow_html=True)
    
    # Welcome section
    col1, col2, col3 = st.columns([1, 2, 1])
    
    with col2:
        st.markdown("""
        <div style="text-align: center; margin: 2rem 0;">
            <h2 style="color: #FFD700; margin-bottom: 1rem;">🚀 My Personal Development Tracker</h2>
            <p style="color: #C0C0C0; font-size: 1.1rem; line-height: 1.6;">
                Built with <span class="tech-accent">MG System Dev</span> expertise, this is my personal 
                tracking system to monitor my learning progress, skills development, and coding journey.
            </p>
        </div>
        """, unsafe_allow_html=True)
    
    # Feature cards
    col_left, col_right = st.columns(2)
    
    with col_left:
        st.markdown("""
        <div class="feature-card">
            <div class="feature-title">⚡ Progress Analytics</div>
            <div class="feature-text">
                Track my learning sessions, coding hours, and skill development 
                with detailed insights and progress visualization.
            </div>
        </div>
        """, unsafe_allow_html=True)
        
        st.markdown("""
        <div class="feature-card">
            <div class="feature-title">🎯 Personal Goals</div>
            <div class="feature-text">
                Set and monitor my coding goals, learning milestones, and 
                development targets to stay motivated and focused.
            </div>
        </div>
        """, unsafe_allow_html=True)
    
    with col_right:
        st.markdown("""
        <div class="feature-card">
            <div class="feature-title">🔧 Learning Management</div>
            <div class="feature-text">
                Organize my study sessions, coding projects, and learning resources 
                all in one centralized personal system.
            </div>
        </div>
        """, unsafe_allow_html=True)
        
        st.markdown("""
        <div class="feature-card">
            <div class="feature-title">📊 Personal Dashboard</div>
            <div class="feature-text">
                Clean, focused interface designed for my personal use with 
                customizable views to track my development journey.
            </div>
        </div>
        """, unsafe_allow_html=True)
    
    # Demo section with professional styling
    st.markdown("---")
    st.markdown("""
    <div style="text-align: center; margin: 2rem 0;">
        <h3 style="color: #FFD700; margin-bottom: 1rem;">🎮 My Tracking Interfaces</h3>
        <p style="color: #C0C0C0;">Choose my preferred tracking mode</p>
    </div>
    """, unsafe_allow_html=True)
    
    col_demo1, col_demo2, col_demo3 = st.columns(3)
    
    with col_demo1:
        if st.button("🎉 System Demo", help="Experience the MG System capabilities"):
            st.balloons()
            st.success("🚀 MG System Dev - Tracking Excellence Activated!")
    
    with col_demo2:
        if st.button("📚 Clean Dashboard", help="Professional learning session tracking interface"):
            st.session_state.current_page = "clean_dashboard"
            st.rerun()
    
    with col_demo3:
        if st.button("🎓 Learning Tracker", help="Advanced desktop-style tracking application"):
            st.session_state.current_page = "learning_tracker"
            st.rerun()
    
    # Professional stats section with tech stack management
    st.markdown("---")
    
    # Initialize tech stack in session state if not exists
    if "tech_stack" not in st.session_state:
        st.session_state.tech_stack = [
            {"name": "Python 3.11+", "category": "Core Engine"},
            {"name": "Streamlit", "category": "Web Interface"},
            {"name": "Typer CLI", "category": "Command Line"},
            {"name": "Pydantic", "category": "Validation"}
        ]
    
    # Tech stack header with update button
    col_title, col_button = st.columns([3, 1])
    
    with col_title:
        st.markdown("""
        <h4 style="color: #FFD700; margin-bottom: 1rem;">🏗️ My Tech Stack</h4>
        """, unsafe_allow_html=True)
    
    with col_button:
        if st.button("⚙️ Update Stack", help="Add or modify technologies in your stack"):
            st.session_state.show_tech_dialog = True
            st.rerun()
    
    # Display current tech stack using dynamic Streamlit components
    with st.container():
        st.markdown("""
        <div class="stats-container">
        """, unsafe_allow_html=True)
        
        # Create rows of technologies (4 per row)
        tech_stack = st.session_state.tech_stack
        rows = [tech_stack[i:i+4] for i in range(0, len(tech_stack), 4)]
        
        for row in rows:
            cols = st.columns(4)
            for i, tech in enumerate(row):
                with cols[i]:
                    st.markdown(f"""
                    <div style="text-align: center; padding: 1rem;">
                        <div style="color: #00CED1; font-size: 1.5rem; font-weight: bold;">{tech['name']}</div>
                        <div style="color: #C0C0C0; font-size: 0.9rem;">{tech['category']}</div>
                    </div>
                    """, unsafe_allow_html=True)
            
            # Fill empty columns if row is not complete
            for i in range(len(row), 4):
                with cols[i]:
                    st.empty()
        
        st.markdown("</div>", unsafe_allow_html=True)
    
    # Tech stack update dialog
    if st.session_state.get("show_tech_dialog", False):
        with st.container():
            st.markdown("""
            <div style="background: linear-gradient(135deg, #1a1a2e 0%, #16213e 100%); padding: 2rem; border-radius: 15px; border: 2px solid #FFD700; margin: 1rem 0;">
            """, unsafe_allow_html=True)
            
            st.markdown("### ⚙️ Update Tech Stack")
            
            # Add new technology
            st.markdown("#### Add New Technology")
            col_name, col_cat = st.columns(2)
            
            with col_name:
                new_tech_name = st.text_input("Technology Name", placeholder="e.g., React, Docker, PostgreSQL")
            
            with col_cat:
                new_tech_category = st.text_input("Category", placeholder="e.g., Frontend, DevOps, Database")
            
            col_add, col_close = st.columns(2)
            
            with col_add:
                if st.button("➕ Add Technology", type="primary"):
                    if new_tech_name and new_tech_category:
                        st.session_state.tech_stack.append({
                            "name": new_tech_name,
                            "category": new_tech_category
                        })
                        st.success(f"Added {new_tech_name} to your tech stack!")
                        st.rerun()
                    else:
                        st.error("Please enter both technology name and category.")
            
            with col_close:
                if st.button("❌ Close Dialog"):
                    st.session_state.show_tech_dialog = False
                    st.rerun()
            
            # Manage existing technologies
            if len(st.session_state.tech_stack) > 4:  # Show management only if there are added technologies
                st.markdown("#### Manage Existing Technologies")
                
                for i, tech in enumerate(st.session_state.tech_stack[4:], start=4):  # Skip the default 4
                    col_tech, col_remove = st.columns([3, 1])
                    
                    with col_tech:
                        st.write(f"**{tech['name']}** - *{tech['category']}*")
                    
                    with col_remove:
                        if st.button(f"🗑️", key=f"remove_{i}", help=f"Remove {tech['name']}"):
                            st.session_state.tech_stack.pop(i)
                            st.success(f"Removed {tech['name']} from your tech stack!")
                            st.rerun()
            
            st.markdown("</div>", unsafe_allow_html=True)
    
    # Footer with personal branding
    st.markdown("""
    <div style="text-align: center; margin-top: 3rem; padding: 1rem; color: #C0C0C0;">
        <hr style="border-color: #FFD700;">
        <p style="margin: 0.5rem 0;">Built by <span style="color: #FFD700; font-weight: bold;">MG SYSTEM DEV</span></p>
        <p style="margin: 0; font-size: 0.9rem;">Personal Development • Learning Tracker • Progress Monitor</p>
    </div>
    """, unsafe_allow_html=True)

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
        page_title="MG Smart Tracker | System Dev",
        page_icon="⚡",
        layout="wide",
        initial_sidebar_state="expanded"
    )
    
    # Initialize session state
    if "current_page" not in st.session_state:
        st.session_state.current_page = "home"
    
    # Main header with MG branding
    st.markdown("""
    <div style="text-align: center; padding: 1rem 0; background: linear-gradient(90deg, #1a1a2e 0%, #16213e 50%, #1a1a2e 100%); border-radius: 10px; margin-bottom: 1rem;">
        <h1 style="color: #FFD700; margin: 0; font-size: 2.5rem; font-weight: bold; text-shadow: 2px 2px 4px rgba(0,0,0,0.8);">⚡ MG SMART TRACKER</h1>
        <p style="color: #C0C0C0; margin: 0.5rem 0 0 0; font-size: 1.1rem;">Professional Development Tracking Platform</p>
    </div>
    """, unsafe_allow_html=True)
    
    # Professional sidebar with MG branding
    with st.sidebar:
        st.markdown("""
        <div style="background: linear-gradient(135deg, #1a1a2e 0%, #16213e 100%); padding: 1rem; border-radius: 10px; border: 1px solid #FFD700; margin-bottom: 1rem;">
            <h3 style="color: #FFD700; text-align: center; margin: 0;">⚡ MG SYSTEM</h3>
            <p style="color: #C0C0C0; text-align: center; margin: 0.5rem 0 0 0; font-size: 0.9rem;">v{}</p>
        </div>
        """.format(__version__), unsafe_allow_html=True)
        
        st.markdown("### 🎯 Navigation")
        
        # Navigation buttons with professional styling
        if st.button("🏠 Home", width="stretch"):
            st.session_state.current_page = "home"
            st.rerun()
        
        if st.button("📚 Clean Dashboard", width="stretch"):
            st.session_state.current_page = "clean_dashboard"
            st.rerun()
            
        if st.button("🎓 Learning Tracker", width="stretch"):
            st.session_state.current_page = "learning_tracker"
            st.rerun()
        
        st.markdown("---")
        
        # Professional info section
        st.markdown("""
        <div style="background: linear-gradient(135deg, #16213e 0%, #1a1a2e 100%); padding: 1rem; border-radius: 8px; border: 1px solid #C0C0C0;">
            <h4 style="color: #FFD700; margin-top: 0;">🔧 System Status</h4>
            <p style="color: #00CED1; margin: 0.5rem 0;"><strong>Status:</strong> <span style="color: #90EE90;">Online</span></p>
            <p style="color: #00CED1; margin: 0.5rem 0;"><strong>Mode:</strong> Development</p>
            <p style="color: #00CED1; margin: 0.5rem 0;"><strong>Build:</strong> Professional</p>
        </div>
        """, unsafe_allow_html=True)
        
        st.markdown("---")
        st.markdown("""
        <div style="text-align: center; color: #C0C0C0; font-size: 0.9rem;">
            <p><strong style="color: #FFD700;">MG System Dev</strong></p>
            <p>Personal learning & development tracking</p>
        </div>
        """, unsafe_allow_html=True)
    
    # Display the appropriate page
    if st.session_state.current_page == "home":
        show_home_page()
    elif st.session_state.current_page == "clean_dashboard":
        show_clean_dashboard()
    elif st.session_state.current_page == "learning_tracker":
        show_learning_tracker()

if __name__ == "__main__":
    main()