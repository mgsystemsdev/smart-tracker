"""
Smart Tracker Streamlit Web Application.

A web-based interface for the Smart Tracker application using Streamlit.
"""

import streamlit as st
import pandas as pd
from datetime import date, datetime
import logging
import os
import sys
from pathlib import Path

# Add parent directory to path for imports
sys.path.insert(0, str(Path(__file__).parent.parent.parent))

from smarttracker.domain.storage import JSONStorage, TECH_CATEGORIES

__version__ = "0.1.0"

# Setup logging
os.makedirs("logs", exist_ok=True)
logging.basicConfig(
    filename="logs/activity.log",
    level=logging.INFO,
    format="%(asctime)s | %(levelname)s | %(message)s"
)

def validate_session(session_date, technology, hours):
    """Validate session data. Returns (is_valid, error_message)."""
    # Check hours
    if hours < 0 or hours > 12:
        return False, "⚠️ Hours must be between 0 and 12 (inclusive)"
    
    # Check future date
    if session_date > date.today():
        return False, "⚠️ Cannot log sessions for future dates"
    
    # Check technology not empty
    if not technology or not technology.strip():
        return False, "⚠️ Technology cannot be empty"
    
    return True, ""

PLANNING_BLUEPRINT = {
    "🌐 Core Full-Stack Development": {
        "subsections": [
            {
                "name": "🖥️ Front-End",
                "tools": [
                    {"name": "HTML", "min_hours": 20, "max_hours": 30},
                    {"name": "CSS", "min_hours": 20, "max_hours": 30},
                    {"name": "JavaScript (ES6+)", "min_hours": 60, "max_hours": 80},
                    {"name": "React", "min_hours": 70, "max_hours": 90},
                    {"name": "Tailwind CSS", "min_hours": 15, "max_hours": 25}
                ]
            },
            {
                "name": "⚙️ Back-End",
                "tools": [
                    {"name": "Django", "min_hours": 80, "max_hours": 100},
                    {"name": "PostgreSQL", "min_hours": 40, "max_hours": 50}
                ]
            },
            {
                "name": "🔗 Lightweight APIs / Model Serving",
                "tools": [
                    {"name": "FastAPI", "min_hours": 40, "max_hours": 60}
                ]
            },
            {
                "name": "🌉 Integration (optional)",
                "tools": [
                    {"name": "Next.js", "min_hours": 40, "max_hours": 60}
                ]
            },
            {
                "name": "☁️ Deployment",
                "tools": [
                    {"name": "AWS (S3 + EC2 + Lambda)", "min_hours": 80, "max_hours": 100},
                    {"name": "GitHub Actions", "min_hours": 25, "max_hours": 40}
                ]
            }
        ]
    },
    "📊 Data Science & Machine Learning": {
        "subsections": [
            {
                "name": "🧮 Core Libraries",
                "tools": [
                    {"name": "Pandas", "min_hours": 80, "max_hours": 100},
                    {"name": "NumPy", "min_hours": 25, "max_hours": 35},
                    {"name": "SciPy", "min_hours": 15, "max_hours": 20}
                ]
            },
            {
                "name": "📈 Visualization",
                "tools": [
                    {"name": "Matplotlib", "min_hours": 25, "max_hours": 35},
                    {"name": "Seaborn", "min_hours": 20, "max_hours": 25},
                    {"name": "Streamlit", "min_hours": 50, "max_hours": 70}
                ]
            },
            {
                "name": "🤖 Machine Learning",
                "tools": [
                    {"name": "scikit-learn", "min_hours": 60, "max_hours": 80},
                    {"name": "PyTorch", "min_hours": 60, "max_hours": 80},
                    {"name": "TensorFlow", "min_hours": 60, "max_hours": 80},
                    {"name": "CUDA (optional)", "min_hours": 20, "max_hours": 30}
                ]
            },
            {
                "name": "🔄 Pipelines",
                "tools": [
                    {"name": "Apache Airflow", "min_hours": 50, "max_hours": 70}
                ]
            },
            {
                "name": "🗄️ Databases (for data work)",
                "tools": [
                    {"name": "PostgreSQL", "min_hours": 40, "max_hours": 60}
                ]
            }
        ]
    },
    "📑 Excel Automation & Data Handling": {
        "subsections": [
            {
                "name": "",
                "tools": [
                    {"name": "OpenPyXL", "min_hours": 20, "max_hours": 30},
                    {"name": "xlwings", "min_hours": 25, "max_hours": 40}
                ]
            }
        ]
    },
    "⚙️ Core Automation (Support Layer)": {
        "subsections": [
            {
                "name": "",
                "tools": [
                    {"name": "Python (automation scripting)", "min_hours": 50, "max_hours": 70},
                    {"name": "Cron Jobs + Airflow", "min_hours": 20, "max_hours": 30},
                    {"name": "Selenium / Playwright", "min_hours": 40, "max_hours": 60},
                    {"name": "Requests + aiohttp", "min_hours": 25, "max_hours": 40},
                    {"name": "GitHub Actions (CI/CD automation)", "min_hours": 20, "max_hours": 30}
                ]
            }
        ]
    },
    "🔒 Reliability & Security": {
        "subsections": [
            {
                "name": "",
                "tools": [
                    {"name": "pytest (testing)", "min_hours": 30, "max_hours": 50},
                    {"name": "OAuth 2.0 + Web App Security", "min_hours": 40, "max_hours": 60}
                ]
            }
        ]
    },
    "🧰 Supporting Skills": {
        "subsections": [
            {
                "name": "",
                "tools": [
                    {"name": "Git (version control)", "min_hours": 25, "max_hours": 40},
                    {"name": "REST + GraphQL APIs", "min_hours": 40, "max_hours": 60},
                    {"name": "Jira + Agile Collaboration", "min_hours": 20, "max_hours": 30}
                ]
            }
        ]
    }
}

def get_tech_list(tech_stack):
    """Get list of technology names from tech stack."""
    if not tech_stack:
        return ["Python", "Pandas", "Streamlit", "FastAPI", "SQL", "AI/ML"]
    return [tech['name'] for tech in tech_stack]

def ensure_tech_in_stack(technology, tech_stack, storage, category="❓ Uncategorized"):
    """Add technology to tech stack if it doesn't exist."""
    tech_names = [tech['name'] for tech in tech_stack]
    if technology not in tech_names:
        new_tech = {
            "name": technology,
            "category": category,
            "goal_hours": 50,
            "date_added": str(date.today())
        }
        tech_stack.append(new_tech)
        storage.save_tech_stack(tech_stack)
        logging.info(f"Auto-added technology to stack: {technology} in category: {category}")
        return True
    return False

def get_studying_practice_breakdown(sessions, technology=None):
    """Calculate studying vs practice hours breakdown.
    
    Args:
        sessions: List of session dictionaries
        technology: Optional technology name to filter by
    
    Returns:
        dict with total_hours, studying_hours, studying_pct, practice_hours, practice_pct
    """
    # Filter sessions if technology is specified
    if technology:
        sessions = [s for s in sessions if s.get('technology') == technology]
    
    total_hours = sum(s.get('hours', 0) for s in sessions)
    studying_hours = sum(s.get('hours', 0) for s in sessions if s.get('type') == 'Studying')
    practice_hours = sum(s.get('hours', 0) for s in sessions if s.get('type') == 'Practice')
    
    # Calculate percentages
    studying_pct = (studying_hours / total_hours * 100) if total_hours > 0 else 0
    practice_pct = (practice_hours / total_hours * 100) if total_hours > 0 else 0
    
    return {
        'total_hours': total_hours,
        'studying_hours': studying_hours,
        'studying_pct': studying_pct,
        'practice_hours': practice_hours,
        'practice_pct': practice_pct
    }

def show_clean_dashboard():
    """Display the Personal Development Dashboard."""
    # Header with MG branding
    st.markdown("""
    <div style="background: linear-gradient(135deg, #1a1a2e 0%, #16213e 50%, #0f3460 100%); padding: 1.5rem; border-radius: 15px; margin-bottom: 2rem; border: 2px solid #FFD700;">
        <h1 style="color: #FFD700; margin: 0; text-align: center;">📚 Personal Development Dashboard</h1>
        <p style="color: #C0C0C0; text-align: center; margin: 0.5rem 0 0 0;">Track Your Learning Journey</p>
    </div>
    """, unsafe_allow_html=True)
    
    # Back button
    if st.button("← Back to Home", help="Return to main page"):
        st.session_state.current_page = "home_v2"
        st.rerun()
    
    # Initialize learning sessions in session state
    if "learning_sessions" not in st.session_state:
        st.session_state.learning_sessions = []
    
    # Edit Session Dialog
    if st.session_state.get("editing_session") is not None:
        edit_index = st.session_state.editing_session
        
        if 0 <= edit_index < len(st.session_state.learning_sessions):
            session = st.session_state.learning_sessions[edit_index]
            
            st.markdown("""
            <div style="background: linear-gradient(135deg, #1a1a2e 0%, #16213e 100%); padding: 2rem; border-radius: 15px; border: 2px solid #FFD700; margin: 1rem 0;">
            """, unsafe_allow_html=True)
            
            st.markdown("### ✏️ Edit Learning Session")
            
            with st.form(f"edit_form_{edit_index}"):
                col1, col2 = st.columns(2)
                
                # Get available technologies from tech stack
                tech_list = get_tech_list(st.session_state.tech_stack)
                
                with col1:
                    edit_date = st.date_input("Date", value=pd.to_datetime(session['date']).date())
                    st.markdown("**Technology**")
                    current_tech = session.get('technology', '')
                    edit_technology = st.text_input("tech_edit_input", value=current_tech, label_visibility="collapsed", placeholder="Type technology name...", key=f"tech_edit_input_{edit_index}")
                    
                    # Show suggestions if available
                    if tech_list:
                        st.caption(f"💡 Recent: {', '.join(tech_list[:8])}")
                    edit_topic = st.text_input("Topic/Subject", value=session.get('topic', ''))
                    edit_type = st.selectbox("Session Type", ["Coding", "Reading", "Tutorial", "Practice", "Project", "Course"],
                        index=["Coding", "Reading", "Tutorial", "Practice", "Project", "Course"].index(session.get('type', 'Coding')) if session.get('type') in ["Coding", "Reading", "Tutorial", "Practice", "Project", "Course"] else 0)
                
                with col2:
                    edit_difficulty = st.selectbox("Difficulty", ["Beginner", "Intermediate", "Advanced", "Expert"],
                        index=["Beginner", "Intermediate", "Advanced", "Expert"].index(session.get('difficulty', 'Beginner')) if session.get('difficulty') in ["Beginner", "Intermediate", "Advanced", "Expert"] else 0)
                    edit_hours = st.number_input("Hours Spent", min_value=0.0, value=float(session.get('hours', 1.0)), step=0.25)
                    edit_status = st.selectbox("Status", ["In Progress", "Completed", "Paused", "Planned"],
                        index=["In Progress", "Completed", "Paused", "Planned"].index(session.get('status', 'In Progress')) if session.get('status') in ["In Progress", "Completed", "Paused", "Planned"] else 0)
                
                edit_tags = st.text_input("Tags", value=session.get('tags', ''))
                edit_notes = st.text_area("Notes", value=session.get('notes', ''))
                
                col_save, col_cancel = st.columns(2)
                
                with col_save:
                    submitted = st.form_submit_button("💾 Save Changes", type="primary")
                
                with col_cancel:
                    cancel = st.form_submit_button("❌ Cancel")
                
                if submitted:
                    # Validate session
                    is_valid, error_msg = validate_session(edit_date, edit_technology, edit_hours)
                    
                    if not is_valid:
                        st.error(error_msg)
                        logging.warning(f"Edit validation failed: {error_msg} | Session #{edit_index}")
                    else:
                        # Ensure technology is in stack
                        ensure_tech_in_stack(edit_technology, st.session_state.tech_stack, st.session_state.storage)
                        
                        # Update the session
                        st.session_state.learning_sessions[edit_index] = {
                            "date": str(edit_date),
                            "technology": edit_technology,
                            "topic": edit_topic,
                            "work_item": session.get('work_item', edit_topic),
                            "skill": session.get('skill', edit_topic),
                            "type": edit_type,
                            "category_type": session.get('category_type', ''),
                            "category_name": session.get('category_name', ''),
                            "category_source": session.get('category_source', ''),
                            "difficulty": edit_difficulty,
                            "status": edit_status,
                            "hours": edit_hours,
                            "tags": edit_tags,
                            "notes": edit_notes
                        }
                        # Save to JSON
                        st.session_state.storage.save_sessions(st.session_state.learning_sessions)
                        logging.info(f"Edited session #{edit_index}: {edit_hours}h {edit_technology} ({edit_date})")
                        st.session_state.editing_session = None
                        st.success("✅ Session updated successfully!")
                        st.rerun()
                
                if cancel:
                    st.session_state.editing_session = None
                    st.rerun()
            
            st.markdown("</div>", unsafe_allow_html=True)
            st.markdown("---")
    
    # Dashboard metrics
    st.markdown("### 📊 Learning Metrics")
    col1, col2, col3, col4 = st.columns(4)
    
    total_sessions = len(st.session_state.learning_sessions)
    total_hours = sum(session.get("hours", 0) for session in st.session_state.learning_sessions)
    completed_sessions = len([s for s in st.session_state.learning_sessions if s.get("status") == "Completed"])
    completion_rate = (completed_sessions / total_sessions * 100) if total_sessions > 0 else 0
    
    with col1:
        st.metric("Total Sessions", total_sessions)
    with col2:
        st.metric("Hours Logged", f"{total_hours:.1f}")
    with col3:
        st.metric("Completed", completed_sessions)
    with col4:
        st.metric("Completion Rate", f"{completion_rate:.1f}%")
    
    st.markdown("---")
    
    # Filters and Sorting Section
    st.markdown("### 🔍 Filters & Sorting")
    
    # Initialize filtered_sessions
    filtered_sessions = st.session_state.learning_sessions.copy() if st.session_state.learning_sessions else []
    
    if st.session_state.learning_sessions:
        # Create filter controls
        col_filter1, col_filter2, col_filter3, col_sort = st.columns(4)
        
        # Get unique values for filters
        df_temp = pd.DataFrame(st.session_state.learning_sessions)
        unique_technologies = ['All'] + sorted(df_temp['technology'].unique().tolist())
        unique_types = ['All'] + sorted(df_temp['type'].unique().tolist())
        unique_statuses = ['All'] + sorted(df_temp['status'].unique().tolist())
        
        with col_filter1:
            tech_filter = st.selectbox("Technology", unique_technologies, key="tech_filter")
        
        with col_filter2:
            type_filter = st.selectbox("Session Type", unique_types, key="type_filter")
        
        with col_filter3:
            status_filter = st.selectbox("Status", unique_statuses, key="status_filter")
        
        with col_sort:
            sort_options = ['Date (Newest)', 'Date (Oldest)', 'Hours (Most)', 'Hours (Least)']
            sort_by = st.selectbox("Sort By", sort_options, key="sort_filter")
        
        # Apply filters
        filtered_sessions = st.session_state.learning_sessions.copy()
        
        if tech_filter != 'All':
            filtered_sessions = [s for s in filtered_sessions if s['technology'] == tech_filter]
        
        if type_filter != 'All':
            filtered_sessions = [s for s in filtered_sessions if s['type'] == type_filter]
        
        if status_filter != 'All':
            filtered_sessions = [s for s in filtered_sessions if s['status'] == status_filter]
        
        # Apply sorting
        if sort_by == 'Date (Newest)':
            filtered_sessions = sorted(filtered_sessions, key=lambda x: x['date'], reverse=True)
        elif sort_by == 'Date (Oldest)':
            filtered_sessions = sorted(filtered_sessions, key=lambda x: x['date'])
        elif sort_by == 'Hours (Most)':
            filtered_sessions = sorted(filtered_sessions, key=lambda x: x['hours'], reverse=True)
        elif sort_by == 'Hours (Least)':
            filtered_sessions = sorted(filtered_sessions, key=lambda x: x['hours'])
        
        # Clear filters button
        if st.button("🗑️ Clear All Filters"):
            st.session_state.tech_filter = 'All'
            st.session_state.type_filter = 'All'
            st.session_state.status_filter = 'All'
            st.session_state.sort_filter = 'Date (Newest)'
            st.rerun()
    
    st.markdown("---")
    
    # Main content area
    col_left, col_right = st.columns([2, 1])
    
    with col_left:
        if st.session_state.learning_sessions:
            # Show filtered results count
            total_sessions = len(st.session_state.learning_sessions)
            filtered_count = len(filtered_sessions)
            
            st.subheader(f"📚 Learning Sessions ({filtered_count} of {total_sessions})")
            
            if filtered_sessions:
                # Display filtered and sorted sessions
                for display_idx, session in enumerate(filtered_sessions):
                    # Create unique key using hash of session data
                    session_key = hash(f"{session['date']}_{session['technology']}_{session.get('hours')}_{display_idx}")
                    
                    # Get the actual index in the full sessions list for operations
                    try:
                        session_index = st.session_state.learning_sessions.index(session)
                    except ValueError:
                        continue
                    
                    # Color-code status
                    status_color = {
                        'Completed': '🟢',
                        'In Progress': '🟡', 
                        'Paused': '🟠',
                        'Planned': '⚪'
                    }.get(session['status'], '⚫')
                    
                    with st.expander(f"{status_color} {session['date']} - {session['topic']} ({session['technology']})"):
                        col_info, col_stats = st.columns(2)
                        
                        with col_info:
                            st.write(f"**Technology:** {session['technology']}")
                            st.write(f"**Type:** {session['type']}")
                            st.write(f"**Difficulty:** {session['difficulty']}")
                            st.write(f"**Status:** {session['status']}")
                        
                        with col_stats:
                            st.write(f"**Hours:** {session['hours']}")
                            st.write(f"**Tags:** {session.get('tags', 'None')}")
                        
                        if session.get('notes'):
                            st.write(f"**Notes:** {session['notes']}")
                        
                        # Action buttons
                        st.markdown("---")
                        col_edit, col_delete, col_spacer = st.columns([1, 1, 2])
                        
                        with col_edit:
                            if st.button("✏️ Edit", key=f"edit_{session_key}", type="secondary"):
                                st.session_state.editing_session = session_index
                                st.rerun()
                        
                        with col_delete:
                            if st.button("🗑️ Delete", key=f"delete_{session_key}", type="secondary"):
                                # Log before deleting to capture session info
                                deleted_session = st.session_state.learning_sessions[session_index]
                                logging.info(f"Deleted session #{session_index}: {deleted_session.get('hours')}h {deleted_session.get('technology')} ({deleted_session.get('date')})")
                                # Delete the session
                                st.session_state.learning_sessions.pop(session_index)
                                # Save to JSON
                                st.session_state.storage.save_sessions(st.session_state.learning_sessions)
                                st.success("Session deleted!")
                                st.rerun()
            else:
                st.info("No sessions match your current filters. Try adjusting the filters above.")
        else:
            st.subheader("📚 Learning Sessions")
            st.info("No learning sessions recorded yet. Use the Smart Learning Tracker to add your first session!")
    
    with col_right:
        st.subheader("🎯 Quick Actions")
        
        # Export to CSV
        if st.session_state.learning_sessions:
            st.markdown("#### 📥 Export Data")
            
            # Create CSV from sessions
            df_export = pd.DataFrame(st.session_state.learning_sessions)
            csv = df_export.to_csv(index=False)
            
            st.download_button(
                label="📄 Download CSV",
                data=csv,
                file_name="learning_sessions.csv",
                mime="text/csv",
                help="Download all your learning sessions as CSV"
            )
            
            st.markdown("---")
        
        # Technology breakdown
        if st.session_state.learning_sessions:
            st.markdown("#### 📊 Technology Focus")
            tech_count = {}
            for session in st.session_state.learning_sessions:
                tech = session.get('technology', 'Unknown')
                tech_count[tech] = tech_count.get(tech, 0) + 1
            
            for tech, count in sorted(tech_count.items(), key=lambda x: x[1], reverse=True):
                st.write(f"**{tech}:** {count} sessions")
        
        st.markdown("---")
        
        # Learning streak
        st.markdown("#### 🔥 Learning Streak")
        if st.session_state.learning_sessions:
            recent_dates = [session['date'] for session in st.session_state.learning_sessions]
            unique_dates = len(set(recent_dates))
            st.metric("Unique Learning Days", unique_dates)
        else:
            st.metric("Learning Streak", "0 days")
    
    # Technology Cards - Expandable view
    st.markdown("---")
    st.subheader("🎯 My Learning Progress")
    
    if st.session_state.learning_sessions:
        # Group sessions by technology
        tech_sessions = {}
        for session in st.session_state.learning_sessions:
            tech = session.get('technology', 'Other')
            if tech not in tech_sessions:
                tech_sessions[tech] = []
            tech_sessions[tech].append(session)
        
        # Display cards for each technology
        for tech, sessions in sorted(tech_sessions.items()):
            # Calculate stats for this technology
            total_logged_hours = sum(s.get('hours', 0) for s in sessions)
            total_sessions = len(sessions)
            last_session_date = max(s.get('date', '') for s in sessions)
            
            # Get goal_hours from tech_stack
            goal_hours = 100  # default
            for tech_obj in st.session_state.tech_stack:
                if tech_obj.get('name') == tech:
                    goal_hours = tech_obj.get('goal_hours', 100)
                    break
            
            # Calculate progress percentage
            progress_percentage = (total_logged_hours / goal_hours * 100) if goal_hours > 0 else 0
            
            # Get studying/practice breakdown
            breakdown = get_studying_practice_breakdown(sessions, tech)
            
            # Card styling with expandable content showing progress
            with st.expander(f"**{tech}**: {total_logged_hours:.1f}/{goal_hours} hrs ({progress_percentage:.0f}%) • {total_sessions} sessions • Last: {last_session_date}", expanded=False):
                st.markdown(f"### {tech} - Learning Progress")
                
                # Progress bar visualization
                st.progress(min(progress_percentage / 100, 1.0))
                st.write(f"**Progress:** {total_logged_hours:.1f} / {goal_hours} hours ({progress_percentage:.1f}%)")
                
                # Studying vs Practice breakdown
                st.markdown("---")
                st.markdown("#### 📊 Session Type Breakdown")
                col1, col2, col3 = st.columns(3)
                with col1:
                    st.metric("Total", f"{breakdown['total_hours']:.1f}h", help="Total hours logged")
                with col2:
                    st.metric("📚 Studying", f"{breakdown['studying_hours']:.1f}h ({breakdown['studying_pct']:.0f}%)", help="Hours spent studying")
                with col3:
                    st.metric("💪 Practice", f"{breakdown['practice_hours']:.1f}h ({breakdown['practice_pct']:.0f}%)", help="Hours spent practicing")
                
                st.markdown("---")
                st.markdown("#### All Sessions")
                
                # Display all sessions for this technology
                for idx, session in enumerate(reversed(sessions)):  # Most recent first
                    # Create unique key for this session
                    session_key = hash(f"{tech}_{session['date']}_{session.get('hours')}_{idx}")
                    
                    # Find the actual index in the full sessions list
                    try:
                        session_index = st.session_state.learning_sessions.index(session)
                    except ValueError:
                        continue
                    
                    st.markdown("---")
                    col_info, col_actions = st.columns([3, 1])
                    
                    with col_info:
                        st.write(f"**📅 {session['date']}** - {session.get('topic', 'Untitled')}")
                        st.write(f"**Type:** {session.get('type', 'N/A')} | **Hours:** {session.get('hours', 0)} | **Status:** {session.get('status', 'N/A')}")
                        st.write(f"**Difficulty:** {session.get('difficulty', 'N/A')}")
                        if session.get('tags'):
                            st.write(f"**Tags:** {session['tags']}")
                        if session.get('notes'):
                            st.write(f"**Notes:** {session['notes']}")
                    
                    with col_actions:
                        if st.button("✏️ Edit", key=f"edit_card_{session_key}"):
                            st.session_state.editing_session = session_index
                            st.rerun()
                        
                        if st.button("🗑️ Delete", key=f"delete_card_{session_key}"):
                            # Log before deleting to capture session info
                            deleted_session = st.session_state.learning_sessions[session_index]
                            logging.info(f"Deleted session #{session_index}: {deleted_session.get('hours')}h {deleted_session.get('technology')} ({deleted_session.get('date')})")
                            st.session_state.learning_sessions.pop(session_index)
                            st.session_state.storage.save_sessions(st.session_state.learning_sessions)
                            st.success("Session deleted!")
                            st.rerun()
    
    else:
        # Empty state
        st.markdown("""
        <div style="text-align: center; padding: 3rem; background: linear-gradient(135deg, #1a1a2e 0%, #16213e 100%); border-radius: 10px; border: 1px solid #FFD700;">
            <h3 style="color: #FFD700;">🚀 Start Tracking Your Work</h3>
            <p style="color: #C0C0C0; font-size: 1.1rem;">
                Log your learning sessions and watch your progress grow automatically.
            </p>
            <p style="color: #00CED1; font-size: 0.9rem;">
                Use the Smart Learning Tracker to add your first session!
            </p>
        </div>
        """, unsafe_allow_html=True)
    
    # Session management
    if st.session_state.learning_sessions:
        st.markdown("---")
        st.subheader("🗂️ Manage Sessions")
        
        if st.button("📊 View All Sessions"):
            st.session_state.show_all_sessions = not st.session_state.get("show_all_sessions", False)
            st.rerun()
        
        if st.session_state.get("show_all_sessions", False):
            st.markdown("#### All Learning Sessions")
            
            # Convert to DataFrame for better display
            df = pd.DataFrame(st.session_state.learning_sessions)
            if not df.empty:
                # Reorder columns for better display
                display_columns = ['date', 'technology', 'topic', 'type', 'difficulty', 'hours', 'status']
                available_columns = [col for col in display_columns if col in df.columns]
                df_display = df[available_columns]
                st.dataframe(df_display, height=300)
                
                # Clear all sessions button with protection
                with st.expander("⚠️ Danger Zone", expanded=False):
                    st.warning("⚠️ **WARNING:** Clearing all sessions is permanent and cannot be undone!")
                    st.markdown("To confirm deletion, type **DELETE** (case-sensitive) in the box below:")
                    
                    delete_confirmation = st.text_input("Type DELETE to confirm:", key="delete_confirm")
                    
                    if st.button("🗑️ Clear All Sessions", type="secondary"):
                        if delete_confirmation == "DELETE":
                            session_count = len(st.session_state.learning_sessions)
                            logging.warning(f"Cleared all sessions: {session_count} sessions deleted")
                            st.session_state.learning_sessions = []
                            # Save empty list to JSON file
                            st.session_state.storage.save_sessions([])
                            st.success("All sessions cleared!")
                            st.rerun()
                        else:
                            st.error("You must type 'DELETE' exactly to clear all sessions.")

def show_tech_stack_page():
    """Display the Tech Stack Goals page organized by categories."""
    # Header with MG branding
    st.markdown("""
    <div style="background: linear-gradient(135deg, #1a1a2e 0%, #16213e 50%, #0f3460 100%); padding: 1.5rem; border-radius: 15px; margin-bottom: 2rem; border: 2px solid #FFD700;">
        <h1 style="color: #FFD700; margin: 0; text-align: center;">🎯 My Tech Stack</h1>
        <p style="color: #C0C0C0; text-align: center; margin: 0.5rem 0 0 0;">Goal Tracking & Progress Overview by Category</p>
    </div>
    """, unsafe_allow_html=True)
    
    # Back button
    if st.button("← Back to Home", help="Return to main page"):
        st.session_state.current_page = "home_v2"
        st.rerun()
    
    # Initialize tech stack
    if "tech_stack" not in st.session_state or not st.session_state.tech_stack:
        st.info("No technologies in your stack yet. Add some from the Learning Tracker!")
        return
    
    # Calculate aggregate statistics
    total_goal_hours = sum(tech.get('goal_hours', 0) for tech in st.session_state.tech_stack)
    
    # Calculate total hours logged across all technologies
    total_hours_logged = 0
    for tech in st.session_state.tech_stack:
        tech_name = tech['name']
        tech_sessions = [s for s in st.session_state.learning_sessions if s.get('technology') == tech_name]
        total_hours_logged += sum(s.get('hours', 0) for s in tech_sessions)
    
    # Calculate overall completion percentage
    overall_completion = (total_hours_logged / total_goal_hours * 100) if total_goal_hours > 0 else 0
    hours_remaining = max(0, total_goal_hours - total_hours_logged)
    
    # Summary Banner
    st.markdown("""
    <div style="background: linear-gradient(135deg, #16213e 0%, #0f3460 100%); padding: 2rem; border-radius: 15px; border: 2px solid #FFD700; margin-bottom: 2rem;">
    """, unsafe_allow_html=True)
    
    st.markdown("### 📊 My Tech Stack - Total Progress")
    
    col1, col2, col3, col4 = st.columns(4)
    
    with col1:
        st.metric("Hours Done", f"{total_hours_logged:.1f}")
    
    with col2:
        st.metric("Total Goal", f"{total_goal_hours:.0f} hrs")
    
    with col3:
        st.metric("% Complete", f"{overall_completion:.1f}%")
    
    with col4:
        st.metric("Hours Missing", f"{hours_remaining:.1f}")
    
    # Overall progress bar
    st.markdown("#### Overall Progress")
    st.progress(min(overall_completion / 100, 1.0))
    
    st.markdown("</div>", unsafe_allow_html=True)
    
    st.markdown("---")
    
    # Group technologies by category
    techs_by_category = {}
    for tech in st.session_state.tech_stack:
        category = tech.get('category', '❓ Uncategorized')
        if category not in techs_by_category:
            techs_by_category[category] = []
        techs_by_category[category].append(tech)
    
    # Display technologies grouped by category
    all_categories = st.session_state.storage.get_all_categories()
    for category in all_categories:
        if category not in techs_by_category:
            continue
        
        category_techs = techs_by_category[category]
        
        # Calculate category subtotals
        category_goal_hours = sum(tech.get('goal_hours', 0) for tech in category_techs)
        category_hours_logged = 0
        for tech in category_techs:
            tech_name = tech['name']
            tech_sessions = [s for s in st.session_state.learning_sessions if s.get('technology') == tech_name]
            category_hours_logged += sum(s.get('hours', 0) for s in tech_sessions)
        
        category_completion = (category_hours_logged / category_goal_hours * 100) if category_goal_hours > 0 else 0
        
        # Category header with subtotals
        with st.expander(f"**{category}** - {category_hours_logged:.1f}/{category_goal_hours:.0f} hrs ({category_completion:.1f}%)", expanded=True):
            # Individual Technology Cards
            for tech in category_techs:
                tech_name = tech['name']
                goal_hours = tech.get('goal_hours', 0)
                category = tech.get('category', 'Unknown')
                
                # Calculate hours logged for this technology
                tech_sessions = [s for s in st.session_state.learning_sessions if s.get('technology') == tech_name]
                hours_logged = sum(s.get('hours', 0) for s in tech_sessions)
                session_count = len(tech_sessions)
                
                # Calculate progress
                progress_pct = (hours_logged / goal_hours * 100) if goal_hours > 0 else 0
                hours_left = max(0, goal_hours - hours_logged)
                
                # Determine status color
                if progress_pct >= 100:
                    status_icon = "✅"
                    status_color = "#00FF00"
                elif progress_pct >= 75:
                    status_icon = "🟢"
                    status_color = "#90EE90"
                elif progress_pct >= 50:
                    status_icon = "🟡"
                    status_color = "#FFD700"
                elif progress_pct >= 25:
                    status_icon = "🟠"
                    status_color = "#FFA500"
                else:
                    status_icon = "🔴"
                    status_color = "#FF6B6B"
                
                # Card display
                with st.container():
                    st.markdown(f"""
                    <div style="background: linear-gradient(135deg, #1a1a2e 0%, #16213e 100%); padding: 1.5rem; border-radius: 12px; border: 2px solid {status_color}; margin-bottom: 1rem; box-shadow: 0 4px 15px rgba(255, 215, 0, 0.2);">
                        <h3 style="color: #FFD700; margin: 0 0 0.5rem 0;">{status_icon} {tech_name}</h3>
                        <p style="color: #C0C0C0; margin: 0 0 1rem 0; font-size: 0.9rem;"><em>{category}</em></p>
                    </div>
                    """, unsafe_allow_html=True)
                    
                    col_a, col_b, col_c, col_d = st.columns(4)
                    
                    with col_a:
                        st.metric("Hours Done", f"{hours_logged:.1f}")
                    
                    with col_b:
                        st.metric("Goal", f"{goal_hours:.0f} hrs")
                    
                    with col_c:
                        st.metric("Progress", f"{progress_pct:.1f}%")
                    
                    with col_d:
                        st.metric("Remaining", f"{hours_left:.1f} hrs")
                    
                    # Progress bar
                    st.progress(min(progress_pct / 100, 1.0))
                    st.caption(f"📚 {session_count} sessions logged")
                    
                    # Studying vs Practice breakdown
                    if tech_sessions:
                        breakdown = get_studying_practice_breakdown(tech_sessions)
                        st.markdown("##### 📊 Session Type Breakdown")
                        col_sp1, col_sp2, col_sp3 = st.columns(3)
                        with col_sp1:
                            st.metric("Total", f"{breakdown['total_hours']:.1f}h")
                        with col_sp2:
                            st.metric("📚 Studying", f"{breakdown['studying_hours']:.1f}h ({breakdown['studying_pct']:.0f}%)")
                        with col_sp3:
                            st.metric("💪 Practice", f"{breakdown['practice_hours']:.1f}h ({breakdown['practice_pct']:.0f}%)")
                    
                    # Category management
                    with st.expander("⚙️ Manage Tech Settings", expanded=False):
                        # Quick add new category
                        st.markdown("**Add New Category**")
                        col_cat_input, col_cat_btn = st.columns([3, 1])
                        with col_cat_input:
                            new_cat_inline = st.text_input("Category name", key=f"inline_cat_{tech_name}", placeholder="e.g., Mobile", label_visibility="collapsed")
                        with col_cat_btn:
                            if st.button("➕", key=f"inline_cat_btn_{tech_name}", help="Add category"):
                                if new_cat_inline and new_cat_inline.strip():
                                    if st.session_state.storage.add_custom_category(new_cat_inline):
                                        st.success(f"✅ Added: {new_cat_inline}")
                                        st.rerun()
                                    else:
                                        st.error("Already exists!")
                        
                        st.markdown("---")
                        st.markdown("**Change Category**")
                        current_category = tech.get('category', '❓ Uncategorized')
                        all_cats = st.session_state.storage.get_all_categories()
                        current_category_index = all_cats.index(current_category) if current_category in all_cats else len(all_cats) - 1
                        
                        new_category = st.selectbox(
                            f"Category for {tech_name}",
                            all_cats,
                            index=current_category_index,
                            key=f"category_selector_{tech_name}",
                            label_visibility="collapsed"
                        )
                        
                        if st.button(f"Update Category", key=f"update_category_{tech_name}"):
                            if new_category != current_category:
                                tech['category'] = new_category
                                st.session_state.storage.save_tech_stack(st.session_state.tech_stack)
                                logging.info(f"Updated category for {tech_name}: {current_category} -> {new_category}")
                                st.success(f"✅ Moved {tech_name} to {new_category}")
                                st.rerun()
                            else:
                                st.info("Category unchanged")

def show_planning_page():
    """Display dynamic learning roadmap showing user's technologies by category with actual hours."""
    # Header with MG branding
    st.markdown("""
    <div style="background: linear-gradient(135deg, #1a1a2e 0%, #16213e 50%, #0f3460 100%); padding: 1.5rem; border-radius: 15px; margin-bottom: 2rem; border: 2px solid #FFD700;">
        <h1 style="color: #FFD700; margin: 0; text-align: center;">📋 Learning Roadmap & Planning</h1>
        <p style="color: #C0C0C0; text-align: center; margin: 0.5rem 0 0 0;">Your Technologies Grouped by Category</p>
    </div>
    """, unsafe_allow_html=True)
    
    # Back button
    if st.button("← Back to Home", help="Return to main page"):
        st.session_state.current_page = "home_v2"
        st.rerun()
    
    st.markdown("---")
    
    # Group technologies by category
    tech_stack = st.session_state.tech_stack
    learning_sessions = st.session_state.learning_sessions
    
    if not tech_stack:
        st.info("📚 No technologies added yet. Visit the **Learning Tracker** page to add your first session!")
        return
    
    # Calculate hours for each technology from sessions
    tech_hours = {}
    for session in learning_sessions:
        tech_name = session.get('technology', '')
        hours = session.get('hours', 0)
        tech_hours[tech_name] = tech_hours.get(tech_name, 0) + hours
    
    # Group technologies by category
    categories_data = {}
    for tech in tech_stack:
        tech_name = tech['name']
        category = tech.get('category', '❓ Uncategorized')
        
        if category not in categories_data:
            categories_data[category] = []
        
        categories_data[category].append({
            'name': tech_name,
            'logged_hours': tech_hours.get(tech_name, 0),
            'goal_hours': tech.get('goal_hours', 50)
        })
    
    # Track grand totals
    grand_total_logged = 0
    grand_total_goal = 0
    category_summaries = []
    
    # Display each category (in order from all categories)
    all_categories = st.session_state.storage.get_all_categories()
    for category in all_categories:
        if category not in categories_data:
            continue
        
        st.markdown(f"## {category}")
        
        techs = categories_data[category]
        category_logged = 0
        category_goal = 0
        
        # Create table data
        table_data = []
        for tech in sorted(techs, key=lambda x: x['name']):
            logged = tech['logged_hours']
            goal = tech['goal_hours']
            completion = f"{int((logged / goal) * 100)}%" if goal > 0 else "0%"
            
            # Get studying/practice breakdown
            tech_sessions = [s for s in learning_sessions if s.get('technology') == tech['name']]
            breakdown = get_studying_practice_breakdown(tech_sessions)
            
            table_data.append({
                "Technology": tech['name'],
                "Logged": f"{logged:.1f} h",
                "Goal": f"{goal} h",
                "📚 Studying": f"{breakdown['studying_hours']:.1f}h ({breakdown['studying_pct']:.0f}%)",
                "💪 Practice": f"{breakdown['practice_hours']:.1f}h ({breakdown['practice_pct']:.0f}%)",
                "Progress": completion
            })
            
            category_logged += logged
            category_goal += goal
        
        # Display table
        df = pd.DataFrame(table_data)
        st.table(df)
        
        # Category total
        category_completion = int((category_logged / category_goal) * 100) if category_goal > 0 else 0
        st.markdown(f"**Category Total → {category_logged:.1f} / {category_goal} h ({category_completion}%)**")
        st.markdown("---")
        
        # Track for grand total
        category_summaries.append({
            "Category": category,
            "Logged": f"{category_logged:.1f} h",
            "Goal": f"{category_goal} h",
            "Progress": f"{category_completion}%"
        })
        
        grand_total_logged += category_logged
        grand_total_goal += category_goal
    
    # Grand Total Summary
    st.markdown("## 🧮 GRAND TOTAL")
    
    grand_total_df = pd.DataFrame(category_summaries)
    st.table(grand_total_df)
    
    grand_completion = int((grand_total_logged / grand_total_goal) * 100) if grand_total_goal > 0 else 0
    st.markdown(f"### 🎯 Overall Total: **{grand_total_logged:.1f} / {grand_total_goal} hours ({grand_completion}%)**")
    
    # Progress indicator
    st.markdown("")
    st.info("💡 This roadmap dynamically reflects your actual progress. Visit the **Tech Stack** page to manage technologies and set goals!")

def show_learning_tracker():
    """Display the Smart Learning Tracker interface."""
    # Header with MG branding
    st.markdown("""
    <div style="background: linear-gradient(135deg, #1a1a2e 0%, #16213e 50%, #0f3460 100%); padding: 1.5rem; border-radius: 15px; margin-bottom: 2rem; border: 2px solid #FFD700;">
        <h1 style="color: #FFD700; margin: 0; text-align: center;">🎓 Smart Learning Tracker</h1>
        <p style="color: #C0C0C0; text-align: center; margin: 0.5rem 0 0 0;">Desktop-Style Session Entry</p>
    </div>
    """, unsafe_allow_html=True)
    
    # Back button
    if st.button("← Back to Home"):
        st.session_state.current_page = "home_v2"
        st.rerun()
    
    # Initialize learning sessions if not exists
    if "learning_sessions" not in st.session_state:
        st.session_state.learning_sessions = []
    
    st.markdown("---")
    
    # Create the form layout similar to the desktop app
    col_left, col_main = st.columns([1, 2])
    
    with col_left:
        st.subheader("📝 Session Entry")
        
        # Quick add category (outside form)
        with st.expander("➕ Add New Category", expanded=False):
            new_cat_quick = st.text_input("New category name", key="quick_cat_learning", placeholder="e.g., Mobile Development")
            if st.button("Add Category", key="quick_cat_btn_learning"):
                if new_cat_quick and new_cat_quick.strip():
                    if st.session_state.storage.add_custom_category(new_cat_quick):
                        st.success(f"✅ Added: {new_cat_quick}")
                        st.rerun()
                    else:
                        st.error("Category already exists!")
                else:
                    st.error("Please enter a category name.")
        
        # Get available technologies from tech stack
        tech_list = get_tech_list(st.session_state.tech_stack)
        
        with st.form("smart_tracker_form"):
            # Form fields matching the desktop app
            session_date = st.date_input("Session Date", value=date.today())
            
            # Technology selection with dropdown
            st.markdown("**Technology**")
            
            # Create dropdown options: existing technologies + option to add new
            tech_options = ["➕ Type New Technology..."] + tech_list if tech_list else ["➕ Type New Technology..."]
            
            selected_option = st.selectbox(
                "tech_dropdown",
                options=tech_options,
                label_visibility="collapsed",
                help="Select from existing technologies or choose '➕ Type New Technology...' to add a new one"
            )
            
            # If user wants to add new tech, show text input
            if selected_option == "➕ Type New Technology...":
                technology = st.text_input("New technology name", placeholder="Type technology name...", key="new_tech_input")
            else:
                technology = selected_option

            
            st.markdown("**Category** _(for new technologies)_")
            all_cats = st.session_state.storage.get_all_categories()
            tech_category = st.selectbox("Select category for new techs", all_cats[:-1], label_visibility="collapsed", help="Select which category this technology belongs to if it's new")
            
            work_item = st.text_input("Work Item", placeholder="Enter project or resource...")
            skill = st.text_input("Skill/Topic", placeholder="Enter specific skill or topic...")
            
            category_type = st.selectbox("Category Type", ["Framework", "Language", "Tool", "Concept", "Project"])
            category_name = st.text_input("Category Name", placeholder="Enter category...")
            category_source = st.text_input("Category Source", placeholder="Course, book, tutorial...")
            
            difficulty = st.selectbox("Difficulty", ["Beginner", "Intermediate", "Advanced", "Expert"])
            status = st.selectbox("Status", ["In Progress", "Completed", "Paused", "Planned"])
            
            hours_spent = st.number_input("Hours Spent", min_value=0.0, value=1.0, step=0.25)
            session_type = st.selectbox("Session Type", ["Studying", "Practice"])
            
            tags = st.text_area("Tags", placeholder="Enter tags separated by commas...")
            notes = st.text_area("Notes", placeholder="Detailed notes about this session...")
            
            # Save button
            submitted = st.form_submit_button("💾 Save Session", type="primary")
            
            if submitted:
                # Validate session
                is_valid, error_msg = validate_session(session_date, technology, hours_spent)
                
                if not is_valid:
                    st.error(error_msg)
                    logging.warning(f"Validation failed: {error_msg} | Date: {session_date}, Tech: {technology}, Hours: {hours_spent}")
                else:
                    # Ensure technology is in stack (with specified category for new techs)
                    ensure_tech_in_stack(technology, st.session_state.tech_stack, st.session_state.storage, category=tech_category)
                    
                    # Create session object compatible with dashboard
                    new_session = {
                        "date": str(session_date),
                        "technology": technology,
                        "topic": skill or work_item,  # Use skill as topic, fallback to work_item
                        "work_item": work_item,
                        "skill": skill,
                        "type": session_type,
                        "category_type": category_type,
                        "category_name": category_name,
                        "category_source": category_source,
                        "difficulty": difficulty,
                        "status": status,
                        "hours": hours_spent,
                        "tags": tags,
                        "notes": notes
                    }
                    
                    st.session_state.learning_sessions.append(new_session)
                    # Save to JSON file
                    st.session_state.storage.save_sessions(st.session_state.learning_sessions)
                    logging.info(f"Added session: {hours_spent}h {technology} ({session_date})")
                    st.success(f"✅ Session saved: {skill or work_item} ({technology})")
                    st.balloons()
                    st.rerun()
        
        # Status indicator
        st.markdown("""
        <div style="background: linear-gradient(135deg, #16213e 0%, #1a1a2e 100%); padding: 0.5rem; border-radius: 5px; text-align: center; margin-top: 1rem;">
            <span style="color: #90EE90;">● Ready</span>
        </div>
        """, unsafe_allow_html=True)
    
    with col_main:
        st.subheader("📊 Session Overview & History")
        
        # Quick stats
        total_sessions = len(st.session_state.learning_sessions)
        total_hours = sum(s.get("hours", 0) for s in st.session_state.learning_sessions)
        completed_sessions = len([s for s in st.session_state.learning_sessions if s.get("status") == "Completed"])
        
        # Get unique skills
        skills_tracked = len(set([s.get("skill", "") for s in st.session_state.learning_sessions if s.get("skill")]))
        
        # Calculate streak
        if st.session_state.learning_sessions:
            recent_dates = [s['date'] for s in st.session_state.learning_sessions]
            unique_dates = len(set(recent_dates))
        else:
            unique_dates = 0
        
        # Display stats
        col1, col2, col3, col4 = st.columns(4)
        
        with col1:
            st.metric("Total Sessions", total_sessions)
        with col2:
            st.metric("Hours Logged", f"{total_hours:.1f}")
        with col3:
            st.metric("Learning Days", unique_dates)
        with col4:
            st.metric("Skills Tracked", skills_tracked)
        
        st.markdown("---")
        
        # Recent sessions display
        if st.session_state.learning_sessions:
            st.markdown("### 📚 Recent Sessions")
            
            # Show last 5 sessions
            recent_sessions = list(reversed(st.session_state.learning_sessions[-5:]))
            
            for session in recent_sessions:
                with st.expander(f"{session['date']} - {session.get('skill', session.get('topic', 'Untitled'))} ({session['technology']})"):
                    col_info, col_progress = st.columns([2, 1])
                    
                    with col_info:
                        st.write(f"**Work Item:** {session.get('work_item', 'N/A')}")
                        st.write(f"**Technology:** {session['technology']}")
                        st.write(f"**Category:** {session.get('category_type', 'N/A')} - {session.get('category_name', 'N/A')}")
                        st.write(f"**Source:** {session.get('category_source', 'N/A')}")
                        st.write(f"**Difficulty:** {session['difficulty']}")
                        st.write(f"**Status:** {session['status']}")
                    
                    with col_progress:
                        st.metric("Hours", session['hours'])
                        st.metric("Type", session.get('type', 'N/A'))
                    
                    if session.get('tags'):
                        st.write(f"**Tags:** {session['tags']}")
                    
                    if session.get('notes'):
                        st.write(f"**Notes:** {session['notes']}")
            
            # Link to dashboard
            st.markdown("---")
            if st.button("📊 View Full Analytics Dashboard", type="secondary"):
                st.session_state.current_page = "clean_dashboard"
                st.rerun()
        
        else:
            st.info("No sessions recorded yet. Use the form on the left to add your first learning session!")
            
            # Sample session preview
            st.markdown("### 📋 Session Preview")
            st.markdown("""
            <div style="background: linear-gradient(135deg, #16213e 0%, #1a1a2e 100%); padding: 1rem; border-radius: 10px; border: 1px solid #C0C0C0;">
                <p style="color: #FFD700; margin: 0;"><strong>Your sessions will appear here once saved</strong></p>
                <p style="color: #C0C0C0; margin: 0.5rem 0 0 0; font-size: 0.9rem;">
                    Fill out the form and click "Save Session" to start tracking your learning journey.
                </p>
            </div>
            """, unsafe_allow_html=True)

def main():
    """Main Streamlit application function."""
    # Page configuration
    st.set_page_config(
        page_title="MG Smart Tracker v2.0 | System Dev",
        page_icon="⚡",
        layout="wide",
        initial_sidebar_state="expanded"
    )
    
    # Hide default Streamlit page navigation
    st.markdown("""
        <style>
            [data-testid="stSidebarNav"] {
                display: none;
            }
        </style>
    """, unsafe_allow_html=True)
    
    # Initialize database (v2.0)
    if "db" not in st.session_state:
        from smarttracker.domain.db_storage import DatabaseStorage
        st.session_state.db = DatabaseStorage()
    
    # Initialize JSON storage (legacy compatibility)
    if "storage" not in st.session_state:
        st.session_state.storage = JSONStorage()
    
    # Initialize session state
    if "current_page" not in st.session_state:
        st.session_state.current_page = "home_v2"
    
    # Load learning sessions from database
    if "learning_sessions" not in st.session_state:
        all_sessions = st.session_state.db.get_all_sessions()
        # Transform to old format for compatibility with legacy dashboard code
        transformed_sessions = []
        for session in all_sessions:
            transformed_sessions.append({
                'date': session.get('session_date', session.get('date', '')),
                'technology': session.get('technology', ''),
                'topic': session.get('skill_topic', session.get('topic', '')),
                'notes': session.get('notes', ''),
                'tags': session.get('tags', ''),
                'type': session.get('session_type', session.get('type', '')),
                'difficulty': session.get('difficulty', ''),
                'status': session.get('status', ''),
                'hours': session.get('hours_spent', session.get('hours', 0))
            })
        st.session_state.learning_sessions = transformed_sessions
    
    # Load tech stack from database
    if "tech_stack_loaded" not in st.session_state:
        tech_stack = st.session_state.db.get_all_tech_stack()
        st.session_state.tech_stack = tech_stack if tech_stack else []
        st.session_state.tech_stack_loaded = True
    
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
        if st.button("🏠 Home Dashboard", width="stretch"):
            st.session_state.current_page = "home_v2"
            st.rerun()
        
        if st.button("📚 Sessions", width="stretch"):
            st.session_state.current_page = "clean_dashboard"
            st.rerun()
            
        if st.button("🎓 Log Session", width="stretch"):
            st.session_state.current_page = "learning_tracker"
            st.rerun()
        
        if st.button("🎯 Tech Stack CRUD", width="stretch"):
            st.session_state.current_page = "tech_stack_crud"
            st.rerun()
        
        if st.button("📋 Planning", width="stretch"):
            st.session_state.current_page = "planning"
            st.rerun()
        
        if st.button("🧮 Calculator", width="stretch"):
            st.session_state.current_page = "calculator"
            st.rerun()
        
        if st.button("📝 Dropdown Manager", width="stretch"):
            st.session_state.current_page = "dropdown_manager"
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
    if st.session_state.current_page == "home_v2":
        # Import and show new Home KPI Dashboard
        from smarttracker.app.pages.home_kpi_dashboard import show_home_kpi_dashboard
        show_home_kpi_dashboard()
    elif st.session_state.current_page == "tech_stack_crud":
        # Import and show Tech Stack CRUD page
        from smarttracker.app.pages.tech_stack_crud_page import show_tech_stack_crud_page
        show_tech_stack_crud_page()
    elif st.session_state.current_page == "calculator":
        # Import and show Calculator page
        from smarttracker.app.pages.calculator_page import show_calculator_page
        show_calculator_page()
    elif st.session_state.current_page == "dropdown_manager":
        # Import and show Dropdown Manager page
        from smarttracker.app.pages.dropdown_manager_page import show_dropdown_manager_page
        show_dropdown_manager_page()
    elif st.session_state.current_page == "clean_dashboard":
        show_clean_dashboard()
    elif st.session_state.current_page == "learning_tracker":
        show_learning_tracker()
    elif st.session_state.current_page == "tech_stack":
        show_tech_stack_page()
    elif st.session_state.current_page == "planning":
        show_planning_page()

if __name__ == "__main__":
    main()