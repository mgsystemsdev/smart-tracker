"""
Dropdown Manager Page - Centralized management of all dropdown data.
Allows users to view, edit, and delete dropdown values across the system.
"""

import streamlit as st
from smarttracker.domain.dropdown_manager import DropdownManager
from smarttracker.domain.db_storage import DatabaseStorage
import logging

def show_dropdown_manager_page():
    """Display the Dropdown Manager page."""
    
    # Header with MG branding
    st.markdown("""
    <div style="background: linear-gradient(135deg, #1a1a2e 0%, #16213e 50%, #0f3460 100%); padding: 1.5rem; border-radius: 15px; margin-bottom: 2rem; border: 2px solid #FFD700;">
        <h1 style="color: #FFD700; margin: 0; text-align: center;">📝 Dropdown Manager</h1>
        <p style="color: #C0C0C0; text-align: center; margin: 0.5rem 0 0 0;">Centralized Dropdown Data Management</p>
    </div>
    """, unsafe_allow_html=True)
    
    # Back button
    if st.button("← Back to Home", help="Return to main page"):
        st.session_state.current_page = "home_v2"
        st.rerun()
    
    # Initialize database and dropdown manager
    if 'db' not in st.session_state:
        st.session_state.db = DatabaseStorage()
    
    dropdown_manager = DropdownManager(st.session_state.db)
    
    st.markdown("---")
    
    # Get all dropdown data
    all_dropdowns = dropdown_manager.get_all_dropdown_data()
    
    # Display management interface
    st.markdown("### 🔧 Manage Dropdown Values")
    st.info("💡 Edit dropdown values here. Changes sync across all forms and pages instantly.")
    
    # Create tabs for different dropdown categories
    tab1, tab2, tab3 = st.tabs(["📂 Hierarchical Fields", "📋 Independent Fields", "➕ Add New Values"])
    
    with tab1:
        st.markdown("#### Hierarchical Dropdown Fields")
        st.caption("These fields have parent-child dependencies")
        
        # Hierarchical fields
        hierarchical_fields = {
            'category_name': '📂 Category Name',
            'technology': '🔧 Technology', 
            'work_item': '📋 Work Item',
            'skill_topic': '🎯 Skill / Topic'
        }
        
        for field_name, field_label in hierarchical_fields.items():
            with st.expander(f"{field_label} ({len(all_dropdowns.get(field_name, []))} items)", expanded=False):
                values = all_dropdowns.get(field_name, [])
                
                if values:
                    for value in values:
                        col1, col2 = st.columns([4, 1])
                        with col1:
                            st.text(value)
                        with col2:
                            if st.button("🗑️", key=f"del_{field_name}_{value}", help="Delete this value"):
                                if dropdown_manager.delete_dropdown_entry(field_name, value):
                                    st.success(f"Deleted: {value}")
                                    logging.info(f"Deleted dropdown: {field_name} = {value}")
                                    st.rerun()
                                else:
                                    st.error("Failed to delete")
                else:
                    st.caption("No values yet. Add from session entry form.")
    
    with tab2:
        st.markdown("#### Independent Dropdown Fields")
        st.caption("These fields have no dependencies")
        
        # Independent fields
        independent_fields = {
            'session_type': '📝 Session Type',
            'category_source': '📚 Category Source',
            'difficulty': '⚡ Difficulty',
            'status': '✅ Status'
        }
        
        for field_name, field_label in independent_fields.items():
            with st.expander(f"{field_label} ({len(all_dropdowns.get(field_name, []))} items)", expanded=False):
                values = all_dropdowns.get(field_name, [])
                
                if values:
                    for value in values:
                        col1, col2 = st.columns([4, 1])
                        with col1:
                            st.text(value)
                        with col2:
                            if st.button("🗑️", key=f"del_{field_name}_{value}", help="Delete this value"):
                                if dropdown_manager.delete_dropdown_entry(field_name, value):
                                    st.success(f"Deleted: {value}")
                                    logging.info(f"Deleted dropdown: {field_name} = {value}")
                                    st.rerun()
                                else:
                                    st.error("Failed to delete")
                else:
                    st.caption("No values yet.")
    
    with tab3:
        st.markdown("#### Add New Dropdown Values")
        st.caption("Manually add dropdown values to the system")
        
        with st.form("add_dropdown_form"):
            st.markdown("##### Add New Value")
            
            # Select field type
            all_fields = {**hierarchical_fields, **independent_fields}
            selected_field = st.selectbox("Select Field", options=list(all_fields.keys()), format_func=lambda x: all_fields[x])
            
            # Input new value
            new_value = st.text_input("New Value", placeholder="Enter new dropdown value...")
            
            # For hierarchical fields, show parent selector
            if selected_field in hierarchical_fields and selected_field != 'category_name':
                parent_info = dropdown_manager.hierarchy[selected_field]
                parent_field = parent_info['parent']
                
                if parent_field:
                    parent_values = all_dropdowns.get(parent_field, [])
                    if parent_values:
                        parent_value = st.selectbox(f"Parent {all_fields.get(parent_field, parent_field)}", options=parent_values)
                    else:
                        st.warning(f"No parent values available for {parent_field}. Add them first.")
                        parent_value = None
                else:
                    parent_value = None
            else:
                parent_value = None
                parent_field = None
            
            submitted = st.form_submit_button("➕ Add Value", type="primary")
            
            if submitted:
                if new_value and new_value.strip():
                    # Add to database
                    if st.session_state.db.add_dropdown_value(
                        selected_field, 
                        new_value.strip(),
                        parent_field=parent_field if parent_field else None,
                        parent_value=parent_value if parent_value else None
                    ):
                        st.success(f"✅ Added {new_value} to {all_fields[selected_field]}")
                        logging.info(f"Manually added dropdown: {selected_field} = {new_value}")
                        st.rerun()
                    else:
                        st.error("Value already exists or failed to add")
                else:
                    st.error("Please enter a value")
    
    st.markdown("---")
    
    # Statistics
    st.markdown("### 📊 Dropdown Statistics")
    col1, col2, col3 = st.columns(3)
    
    with col1:
        total_hierarchical = sum(len(all_dropdowns.get(f, [])) for f in hierarchical_fields.keys())
        st.metric("Hierarchical Values", total_hierarchical)
    
    with col2:
        total_independent = sum(len(all_dropdowns.get(f, [])) for f in independent_fields.keys())
        st.metric("Independent Values", total_independent)
    
    with col3:
        total_all = total_hierarchical + total_independent
        st.metric("Total Values", total_all)
