"""
Smart Tracker Streamlit Web Application.

A web-based interface for the Smart Tracker application using Streamlit.
"""

import streamlit as st
import pandas as pd
from datetime import date
from smarttracker import __version__
from smarttracker.domain.storage import JSONStorage

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
    
    # Professional stats section with tech stack management
    st.markdown("---")
    
    # Initialize tech stack from storage if not exists
    if "tech_stack" not in st.session_state:
        loaded_tech_stack = st.session_state.storage.load_tech_stack()
        if loaded_tech_stack:
            st.session_state.tech_stack = loaded_tech_stack
        else:
            st.session_state.tech_stack = [
                {"name": "Python", "category": "Language", "goal_hours": 100, "date_added": "2025-10-04"}
            ]
            st.session_state.storage.save_tech_stack(st.session_state.tech_stack)
    
    # Tech stack in a styled box
    st.markdown("""
    <div style="background: linear-gradient(135deg, #1a1a2e 0%, #16213e 50%, #0f3460 100%); padding: 2rem; border-radius: 15px; border: 2px solid #FFD700; margin: 1rem 0;">
    """, unsafe_allow_html=True)
    
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
    # Create rows of technologies (4 per row)
    tech_stack = st.session_state.tech_stack
    rows = [tech_stack[i:i+4] for i in range(0, len(tech_stack), 4)]
    
    for row in rows:
        cols = st.columns(4)
        for i, tech in enumerate(row):
            with cols[i]:
                st.markdown(f"""
                <div style="text-align: center; padding: 1rem; background: rgba(0, 206, 209, 0.1); border-radius: 8px; margin: 0.25rem;">
                    <div style="color: #00CED1; font-size: 1.2rem; font-weight: bold; margin-bottom: 0.5rem;">{tech['name']}</div>
                    <div style="color: #C0C0C0; font-size: 0.8rem;">{tech['category']}</div>
                </div>
                """, unsafe_allow_html=True)
        
        # Fill empty columns if row is not complete
        for i in range(len(row), 4):
            with cols[i]:
                st.empty()
    
    # Close the container
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
            col_name, col_cat, col_goal = st.columns(3)
            
            with col_name:
                new_tech_name = st.text_input("Technology Name", placeholder="e.g., Streamlit, JavaScript, SQL")
            
            with col_cat:
                new_tech_category = st.selectbox("Category", ["Language", "Framework", "Library", "Tool", "Database", "Platform", "Concept"])
            
            with col_goal:
                new_goal_hours = st.number_input("Goal Hours", min_value=1, step=1, value=100)
            
            col_add, col_close = st.columns(2)
            
            with col_add:
                if st.button("➕ Add Technology", type="primary"):
                    if new_tech_name and new_tech_category:
                        from datetime import date
                        st.session_state.tech_stack.append({
                            "name": new_tech_name,
                            "category": new_tech_category,
                            "goal_hours": new_goal_hours,
                            "date_added": str(date.today())
                        })
                        # Save to JSON file
                        st.session_state.storage.save_tech_stack(st.session_state.tech_stack)
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
        st.session_state.current_page = "home"
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
                
                with col1:
                    edit_date = st.date_input("Date", value=pd.to_datetime(session['date']).date())
                    edit_technology = st.selectbox("Technology", 
                        ["Python", "JavaScript", "React", "Node.js", "Java", "C#", "SQL", "Docker", "AWS", "Other"],
                        index=["Python", "JavaScript", "React", "Node.js", "Java", "C#", "SQL", "Docker", "AWS", "Other"].index(session.get('technology', 'Python')) if session.get('technology') in ["Python", "JavaScript", "React", "Node.js", "Java", "C#", "SQL", "Docker", "AWS", "Other"] else 0)
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
            # Ensure filtered_sessions exists
            if 'filtered_sessions' not in locals():
                filtered_sessions = st.session_state.learning_sessions
            
            # Show filtered results count
            total_sessions = len(st.session_state.learning_sessions)
            filtered_count = len(filtered_sessions)
            
            st.subheader(f"📚 Learning Sessions ({filtered_count} of {total_sessions})")
            
            if filtered_sessions:
                # Display filtered and sorted sessions
                for i, session in enumerate(filtered_sessions):
                    # Get the actual index in the full sessions list
                    session_index = st.session_state.learning_sessions.index(session)
                    
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
                            if st.button("✏️ Edit", key=f"edit_{session_index}", type="secondary"):
                                st.session_state.editing_session = session_index
                                st.rerun()
                        
                        with col_delete:
                            if st.button("🗑️ Delete", key=f"delete_{session_index}", type="secondary"):
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
            
            # Card styling with expandable content showing progress
            with st.expander(f"**{tech}**: {total_logged_hours:.1f}/{goal_hours} hrs ({progress_percentage:.0f}%) • {total_sessions} sessions • Last: {last_session_date}", expanded=False):
                st.markdown(f"### {tech} - Learning Progress")
                
                # Progress bar visualization
                st.progress(min(progress_percentage / 100, 1.0))
                st.write(f"**Progress:** {total_logged_hours:.1f} / {goal_hours} hours ({progress_percentage:.1f}%)")
                st.markdown("---")
                st.markdown("#### All Sessions")
                
                # Display all sessions for this technology
                for idx, session in enumerate(reversed(sessions)):  # Most recent first
                    # Find the actual index in the full sessions list
                    session_index = st.session_state.learning_sessions.index(session)
                    
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
                        if st.button("✏️ Edit", key=f"edit_card_{session_index}"):
                            st.session_state.editing_session = session_index
                            st.rerun()
                        
                        if st.button("🗑️ Delete", key=f"delete_card_{session_index}"):
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
                
                # Clear all sessions button
                if st.button("🗑️ Clear All Sessions", help="This will delete all your learning sessions"):
                    st.session_state.learning_sessions = []
                    # Save empty list to JSON file
                    st.session_state.storage.save_sessions([])
                    st.success("All sessions cleared!")
                    st.rerun()

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
        st.session_state.current_page = "home"
        st.rerun()
    
    # Initialize learning sessions if not exists
    if "learning_sessions" not in st.session_state:
        st.session_state.learning_sessions = []
    
    st.markdown("---")
    
    # Create the form layout similar to the desktop app
    col_left, col_main = st.columns([1, 2])
    
    with col_left:
        st.subheader("📝 Session Entry")
        
        with st.form("smart_tracker_form"):
            # Form fields matching the desktop app
            session_date = st.date_input("Session Date", value=date.today())
            technology = st.selectbox("Technology", ["Python", "JavaScript", "Java", "C#", "React", "Node.js", "SQL", "Docker", "AWS", "Other"])
            work_item = st.text_input("Work Item", placeholder="Enter project or resource...")
            skill = st.text_input("Skill/Topic", placeholder="Enter specific skill or topic...")
            
            category_type = st.selectbox("Category Type", ["Framework", "Language", "Tool", "Concept", "Project"])
            category_name = st.text_input("Category Name", placeholder="Enter category...")
            category_source = st.text_input("Category Source", placeholder="Course, book, tutorial...")
            
            difficulty = st.selectbox("Difficulty", ["Beginner", "Intermediate", "Advanced", "Expert"])
            status = st.selectbox("Status", ["In Progress", "Completed", "Paused", "Planned"])
            
            hours_spent = st.number_input("Hours Spent", min_value=0.0, value=1.0, step=0.25)
            session_type = st.selectbox("Session Type", ["Coding", "Reading", "Tutorial", "Practice", "Project", "Course"])
            
            tags = st.text_area("Tags", placeholder="Enter tags separated by commas...")
            notes = st.text_area("Notes", placeholder="Detailed notes about this session...")
            
            # Save button
            submitted = st.form_submit_button("💾 Save Session", type="primary")
            
            if submitted:
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
        page_title="MG Smart Tracker | System Dev",
        page_icon="⚡",
        layout="wide",
        initial_sidebar_state="expanded"
    )
    
    # Initialize JSON storage
    if "storage" not in st.session_state:
        st.session_state.storage = JSONStorage()
    
    # Initialize session state
    if "current_page" not in st.session_state:
        st.session_state.current_page = "home"
    
    # Load learning sessions from JSON file
    if "learning_sessions" not in st.session_state:
        st.session_state.learning_sessions = st.session_state.storage.load_sessions()
    
    # Load tech stack from JSON file
    if "tech_stack_loaded" not in st.session_state:
        loaded_tech_stack = st.session_state.storage.load_tech_stack()
        if loaded_tech_stack:
            st.session_state.tech_stack = loaded_tech_stack
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
        if st.button("🏠 Home", width="stretch"):
            st.session_state.current_page = "home"
            st.rerun()
        
        if st.button("📚 Dashboard", width="stretch"):
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