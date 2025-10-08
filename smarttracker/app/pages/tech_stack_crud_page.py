"""
Tech Stack CRUD Page - Dedicated management interface for technologies.
Provides Create, Read, Update, Delete operations for the tech stack.
"""

import streamlit as st
from datetime import datetime
from smarttracker.domain.db_storage import DatabaseStorage
import logging

def show_tech_stack_crud_page():
    """Display the Tech Stack CRUD management page."""
    
    # Header with MG branding
    st.markdown("""
    <div style="background: linear-gradient(135deg, #1a1a2e 0%, #16213e 50%, #0f3460 100%); padding: 1.5rem; border-radius: 15px; margin-bottom: 2rem; border: 2px solid #FFD700;">
        <h1 style="color: #FFD700; margin: 0; text-align: center;">🎯 Tech Stack Management</h1>
        <p style="color: #C0C0C0; text-align: center; margin: 0.5rem 0 0 0;">Create, Update, Delete Technologies</p>
    </div>
    """, unsafe_allow_html=True)
    
    # Back button
    if st.button("← Back to Home", help="Return to main page"):
        st.session_state.current_page = "home"
        st.rerun()
    
    # Initialize database
    if 'db' not in st.session_state:
        st.session_state.db = DatabaseStorage()
    
    db = st.session_state.db
    
    # Create two columns for Add and Manage
    tab1, tab2 = st.tabs(["➕ Add Technology", "📋 Manage Technologies"])
    
    with tab1:
        st.markdown("### Add New Technology to Stack")
        
        with st.form("add_tech_form"):
            col1, col2 = st.columns(2)
            
            with col1:
                tech_name = st.text_input("Technology Name *", placeholder="e.g., Python, React, PostgreSQL")
                goal_hours = st.number_input("Goal Hours *", min_value=1.0, value=50.0, step=5.0)
            
            with col2:
                # Get all categories
                categories = db.get_all_categories()
                category = st.selectbox("Category *", options=categories)
                date_added = st.date_input("Date Added", value=datetime.now())
            
            submitted = st.form_submit_button("💾 Add Technology", type="primary")
            
            if submitted:
                if tech_name and tech_name.strip():
                    tech_id = db.add_technology(
                        name=tech_name.strip(),
                        category=category,
                        goal_hours=goal_hours,
                        date_added=str(date_added)
                    )
                    
                    if tech_id > 0:
                        st.success(f"✅ Added {tech_name} to tech stack!")
                        logging.info(f"Added technology: {tech_name} (ID: {tech_id})")
                        st.rerun()
                    elif tech_id == -1:
                        st.error(f"❌ {tech_name} already exists in the stack")
                    else:
                        st.error("Failed to add technology")
                else:
                    st.error("Please enter a technology name")
    
    with tab2:
        st.markdown("### Current Tech Stack")
        
        # Get all technologies
        tech_stack = db.get_all_tech_stack()
        
        if not tech_stack:
            st.info("📚 No technologies in your stack yet. Add your first one!")
        else:
            # Display summary
            total_goal_hours = sum(tech.get('goal_hours', 0) for tech in tech_stack)
            total_logged_hours = sum(db.get_hours_by_technology(tech['name']) for tech in tech_stack)
            
            col1, col2, col3 = st.columns(3)
            with col1:
                st.metric("Total Technologies", len(tech_stack))
            with col2:
                st.metric("Total Goal Hours", f"{total_goal_hours:.0f}")
            with col3:
                st.metric("Total Logged Hours", f"{total_logged_hours:.1f}")
            
            st.markdown("---")
            
            # Group by category
            by_category = {}
            for tech in tech_stack:
                cat = tech.get('category', 'Uncategorized')
                if cat not in by_category:
                    by_category[cat] = []
                by_category[cat].append(tech)
            
            # Display by category (default closed)
            for category, techs in sorted(by_category.items()):
                with st.expander(f"**{category}** ({len(techs)} technologies)", expanded=False):
                    for tech in sorted(techs, key=lambda x: x['name']):
                        tech_id = tech['id']
                        tech_name = tech['name']
                        goal_hours = tech.get('goal_hours', 50)
                        date_added = tech.get('date_added', 'Unknown')
                        logged_hours = db.get_hours_by_technology(tech_name)
                        progress_pct = (logged_hours / goal_hours * 100) if goal_hours > 0 else 0
                        
                        # Technology card
                        with st.container():
                            st.markdown(f"""
                            <div style="background: linear-gradient(135deg, #1a1a2e 0%, #16213e 100%); padding: 1rem; border-radius: 10px; border: 1px solid #FFD700; margin-bottom: 1rem;">
                                <h4 style="color: #FFD700; margin: 0;">{tech_name}</h4>
                                <p style="color: #C0C0C0; margin: 0.5rem 0 0 0; font-size: 0.9rem;">Added: {date_added}</p>
                            </div>
                            """, unsafe_allow_html=True)
                            
                            col_a, col_b, col_c = st.columns(3)
                            with col_a:
                                st.metric("Goal", f"{goal_hours:.0f}h")
                            with col_b:
                                st.metric("Logged", f"{logged_hours:.1f}h")
                            with col_c:
                                st.metric("Progress", f"{progress_pct:.1f}%")
                            
                            # Progress bar
                            st.progress(min(progress_pct / 100, 1.0))
                            
                            # Edit and Delete buttons
                            col_edit, col_del = st.columns(2)
                            
                            with col_edit:
                                if st.button(f"✏️ Edit", key=f"edit_{tech_id}", use_container_width=True):
                                    st.session_state.editing_tech = tech_id
                                    st.rerun()
                            
                            with col_del:
                                if st.button(f"🗑️ Delete", key=f"del_{tech_id}", use_container_width=True):
                                    st.session_state.deleting_tech = tech_id
                                    st.rerun()
                            
                            # Edit form (appears when edit clicked)
                            if st.session_state.get('editing_tech') == tech_id:
                                with st.form(f"edit_form_{tech_id}"):
                                    st.markdown("##### Edit Technology")
                                    
                                    edit_name = st.text_input("Name", value=tech_name, key=f"edit_name_{tech_id}")
                                    edit_category = st.selectbox("Category", options=db.get_all_categories(), 
                                                                index=db.get_all_categories().index(tech.get('category', 'Uncategorized')) if tech.get('category') in db.get_all_categories() else 0,
                                                                key=f"edit_cat_{tech_id}")
                                    edit_goal = st.number_input("Goal Hours", value=float(goal_hours), min_value=1.0, step=5.0, key=f"edit_goal_{tech_id}")
                                    
                                    col_save, col_cancel = st.columns(2)
                                    with col_save:
                                        if st.form_submit_button("💾 Save Changes", use_container_width=True):
                                            if db.update_technology(tech_id, name=edit_name, category=edit_category, goal_hours=edit_goal):
                                                st.success(f"✅ Updated {edit_name}")
                                                logging.info(f"Updated technology ID {tech_id}: {edit_name}")
                                                st.session_state.editing_tech = None
                                                st.rerun()
                                            else:
                                                st.error("Failed to update")
                                    
                                    with col_cancel:
                                        if st.form_submit_button("❌ Cancel", use_container_width=True):
                                            st.session_state.editing_tech = None
                                            st.rerun()
                            
                            # Delete confirmation
                            if st.session_state.get('deleting_tech') == tech_id:
                                st.warning(f"⚠️ Are you sure you want to delete **{tech_name}**? This action cannot be undone!")
                                col_confirm, col_cancel_del = st.columns(2)
                                
                                with col_confirm:
                                    if st.button("✅ Yes, Delete", key=f"confirm_del_{tech_id}", use_container_width=True, type="primary"):
                                        if db.delete_technology(tech_id):
                                            st.success(f"🗑️ Deleted {tech_name}")
                                            logging.info(f"Deleted technology ID {tech_id}: {tech_name}")
                                            st.session_state.deleting_tech = None
                                            st.rerun()
                                        else:
                                            st.error("Failed to delete")
                                
                                with col_cancel_del:
                                    if st.button("❌ Cancel", key=f"cancel_del_{tech_id}", use_container_width=True):
                                        st.session_state.deleting_tech = None
                                        st.rerun()
                        
                        st.markdown("---")
