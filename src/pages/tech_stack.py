"""
Tech Stack Dashboard - Visual overview of technologies with KPIs.
Read-only display showing technology cards grouped by category with progress metrics.
"""

import streamlit as st
from src.database.operations import DatabaseStorage
from src.services.cached_queries import CachedQueryService

def show_tech_stack_crud_page():
    """Display the Tech Stack visual dashboard."""
    
    # Header with MG branding
    st.markdown("""
    <div style="background: linear-gradient(135deg, #1a1a2e 0%, #16213e 50%, #0f3460 100%); padding: 1.5rem; border-radius: 15px; margin-bottom: 2rem; border: 2px solid #FFD700;">
        <h1 style="color: #FFD700; margin: 0; text-align: center;">🎯 Tech Stack Dashboard</h1>
        <p style="color: #C0C0C0; text-align: center; margin: 0.5rem 0 0 0;">Visual Overview of Your Learning Journey</p>
    </div>
    """, unsafe_allow_html=True)
    
    # Back button
    if st.button("← Back to Home", help="Return to main page"):
        st.session_state.current_page = "home_v2"
        st.rerun()
    
    # Initialize database
    if 'db' not in st.session_state:
        st.session_state.db = DatabaseStorage()
    
    db = st.session_state.db
    
    # Info banner
    st.info("📝 **Note:** To add or edit technologies, use the Dropdown Manager page")
    
    st.markdown("---")
    
    # Get all technologies WITH metrics in ONE query (cached)
    tech_stack = CachedQueryService.get_tech_stack_with_metrics(db)
    
    if not tech_stack:
        st.markdown("""
        <div style="background: linear-gradient(135deg, #1a1a2e 0%, #16213e 100%); padding: 2rem; border-radius: 15px; border: 2px solid #FFD700; text-align: center;">
            <h3 style="color: #FFD700; margin: 0;">📚 No Technologies Yet</h3>
            <p style="color: #C0C0C0; margin: 1rem 0;">Add your first technology in the Dropdown Manager to start tracking your learning progress!</p>
        </div>
        """, unsafe_allow_html=True)
    else:
        # Display summary KPIs
        total_tech_count = len(tech_stack)
        total_goal_hours = sum(tech.get('goal_hours', 0) for tech in tech_stack)
        total_logged_hours = sum(tech.get('logged_hours', 0) for tech in tech_stack)
        total_sessions = sum(tech.get('session_count', 0) for tech in tech_stack)
        avg_progress = sum(tech.get('progress_pct', 0) for tech in tech_stack) / len(tech_stack) if tech_stack else 0
        
        # Top KPI metrics
        st.markdown("### 📊 Overall Statistics")
        col1, col2, col3, col4, col5 = st.columns(5)
        
        with col1:
            st.metric("Technologies", total_tech_count, help="Total number of technologies you're learning")
        with col2:
            st.metric("Goal Hours", f"{total_goal_hours:.0f}h", help="Combined learning goals")
        with col3:
            st.metric("Logged Hours", f"{total_logged_hours:.1f}h", help="Total time invested")
        with col4:
            st.metric("Sessions", total_sessions, help="Total learning sessions logged")
        with col5:
            st.metric("Avg Progress", f"{avg_progress:.1f}%", help="Average completion across all technologies")
        
        st.markdown("---")
        
        # Group technologies by category
        by_category = {}
        for tech in tech_stack:
            cat = tech.get('category', '❓ Uncategorized')
            if cat not in by_category:
                by_category[cat] = []
            by_category[cat].append(tech)
        
        # Display technologies as visual cards grouped by category
        st.markdown("### 🗂️ Technologies by Category")
        
        for category, techs in sorted(by_category.items()):
            # Category header
            st.markdown(f"#### {category}")
            st.caption(f"{len(techs)} technologies • {sum(t.get('logged_hours', 0) for t in techs):.1f} hours logged")
            
            # Display technology cards in a grid
            for tech in sorted(techs, key=lambda x: x.get('logged_hours', 0), reverse=True):
                tech_name = tech['name']
                goal_hours = tech.get('goal_hours', 50)
                logged_hours = tech.get('logged_hours', 0)
                progress_pct = tech.get('progress_pct', 0)
                session_count = tech.get('session_count', 0)
                date_added = tech.get('date_added', 'Unknown')
                
                # Determine progress color
                if progress_pct >= 100:
                    progress_color = "#00FF00"
                    status_emoji = "✅"
                elif progress_pct >= 75:
                    progress_color = "#FFD700"
                    status_emoji = "🟡"
                elif progress_pct >= 25:
                    progress_color = "#FFA500"
                    status_emoji = "🟠"
                else:
                    progress_color = "#FF4500"
                    status_emoji = "🔴"
                
                # Technology card
                st.markdown(f"""
                <div style="background: linear-gradient(135deg, #1a1a2e 0%, #16213e 100%); padding: 1.5rem; border-radius: 12px; border: 2px solid {progress_color}; margin-bottom: 1.5rem; box-shadow: 0 4px 6px rgba(0, 0, 0, 0.3);">
                    <div style="display: flex; justify-content: space-between; align-items: center; margin-bottom: 1rem;">
                        <h3 style="color: #FFD700; margin: 0;">{status_emoji} {tech_name}</h3>
                        <span style="color: {progress_color}; font-size: 1.2rem; font-weight: bold;">{progress_pct:.1f}%</span>
                    </div>
                    <p style="color: #C0C0C0; margin: 0.5rem 0; font-size: 0.9rem;">📅 Added: {date_added}</p>
                </div>
                """, unsafe_allow_html=True)
                
                # Metrics row
                col_a, col_b, col_c, col_d = st.columns(4)
                
                with col_a:
                    st.metric("🎯 Goal", f"{goal_hours:.0f}h")
                with col_b:
                    st.metric("⏱️ Logged", f"{logged_hours:.1f}h")
                with col_c:
                    st.metric("📝 Sessions", session_count)
                with col_d:
                    hours_remaining = max(0, goal_hours - logged_hours)
                    st.metric("⏳ Remaining", f"{hours_remaining:.1f}h")
                
                # Progress bar
                st.progress(min(progress_pct / 100, 1.0))
                
                # Status message
                if progress_pct >= 100:
                    st.success("🎉 Goal completed! Great work!")
                elif progress_pct >= 75:
                    st.info(f"🚀 Almost there! {hours_remaining:.1f} hours to go")
                elif progress_pct > 0:
                    st.warning(f"💪 Keep going! {hours_remaining:.1f} hours remaining")
                else:
                    st.caption("🆕 No sessions logged yet - time to start learning!")
                
                st.markdown("---")
            
            st.markdown("")  # Add spacing between categories
        
        # Bottom section: Category breakdown
        st.markdown("---")
        st.markdown("### 📈 Category Breakdown")
        
        category_data = []
        for cat, techs in by_category.items():
            cat_hours = sum(t.get('logged_hours', 0) for t in techs)
            cat_sessions = sum(t.get('session_count', 0) for t in techs)
            category_data.append({
                'category': cat,
                'technologies': len(techs),
                'hours': cat_hours,
                'sessions': cat_sessions
            })
        
        # Sort by hours logged
        category_data.sort(key=lambda x: x['hours'], reverse=True)
        
        for cat_info in category_data:
            with st.expander(f"**{cat_info['category']}** - {cat_info['hours']:.1f}h logged", expanded=False):
                col1, col2, col3 = st.columns(3)
                with col1:
                    st.metric("Technologies", cat_info['technologies'])
                with col2:
                    st.metric("Total Hours", f"{cat_info['hours']:.1f}h")
                with col3:
                    st.metric("Sessions", cat_info['sessions'])
