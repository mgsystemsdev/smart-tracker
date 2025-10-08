"""
Dropdown Manager - Handles hierarchical cascading dropdown logic.
Implements the dependency chain: Category → Technology → Work Item → Skill/Topic
"""

import streamlit as st
from typing import List, Dict, Optional, Tuple
from smarttracker.domain.db_storage import DatabaseStorage

class DropdownManager:
    """Manages hierarchical dropdown dependencies and auto-population."""
    
    def __init__(self, db: DatabaseStorage):
        self.db = db
        
        # Define the dependency hierarchy
        self.hierarchy = {
            'category_name': {'parent': None, 'label': '📂 Category Name', 'placeholder': 'Select or type category...'},
            'technology': {'parent': 'category_name', 'label': '🔧 Technology', 'placeholder': 'Select or type technology...'},
            'work_item': {'parent': 'technology', 'label': '📋 Work Item', 'placeholder': 'Select or type work item...'},
            'skill_topic': {'parent': 'work_item', 'label': '🎯 Skill / Topic', 'placeholder': 'Select or type skill...'}
        }
        
        # Independent dropdown fields
        self.independent_fields = {
            'session_type': {'label': '📝 Session Type', 'options': ['Studying', 'Practice']},
            'category_source': {'label': '📚 Category Source', 'placeholder': 'Course, docs, project...'},
            'difficulty': {'label': '⚡ Difficulty', 'options': ['Beginner', 'Intermediate', 'Advanced', 'Expert']},
            'status': {'label': '✅ Status', 'options': ['Planned', 'In Progress', 'Completed', 'Blocked']}
        }
    
    def render_cascading_dropdown(
        self, 
        field_name: str, 
        parent_value: Optional[str] = None,
        key_suffix: str = "",
        allow_new: bool = True
    ) -> str:
        """Render a single cascading dropdown with type-to-add functionality."""
        
        if field_name not in self.hierarchy:
            return ""
        
        field_config = self.hierarchy[field_name]
        parent_field = field_config['parent']
        
        # Get existing values from database
        if parent_field and parent_value:
            existing_values = self.db.get_dropdown_values(field_name, parent_field, parent_value)
        else:
            existing_values = self.db.get_dropdown_values(field_name)
        
        # Display label
        st.markdown(f"**{field_config['label']}**")
        
        if allow_new:
            # Dropdown with option to add new
            options = ["➕ Type New..."] + existing_values if existing_values else ["➕ Type New..."]
            
            selected = st.selectbox(
                f"{field_name}_dropdown_{key_suffix}",
                options=options,
                label_visibility="collapsed",
                key=f"{field_name}_select_{key_suffix}"
            )
            
            # If user wants to add new, show text input
            if selected == "➕ Type New...":
                new_value = st.text_input(
                    f"New {field_config['label']}",
                    placeholder=field_config['placeholder'],
                    key=f"{field_name}_new_{key_suffix}",
                    label_visibility="collapsed"
                )
                
                if new_value and new_value.strip():
                    # Auto-save on Enter (when value is provided)
                    if parent_field and parent_value:
                        self.db.add_dropdown_value(field_name, new_value.strip(), parent_field, parent_value)
                    else:
                        self.db.add_dropdown_value(field_name, new_value.strip())
                    return new_value.strip()
                return ""
            else:
                return selected
        else:
            # Simple selectbox without add-new option
            if existing_values:
                return st.selectbox(
                    field_config['label'],
                    options=existing_values,
                    key=f"{field_name}_select_{key_suffix}"
                )
            else:
                st.info(f"No {field_config['label'].lower()} available. Add from parent dropdown.")
                return ""
    
    def render_hierarchical_form(self, key_suffix: str = "") -> Dict[str, str]:
        """Render complete hierarchical dropdown form and return selected values."""
        
        selected_values = {}
        
        # Category Name (root)
        category = self.render_cascading_dropdown('category_name', key_suffix=key_suffix)
        selected_values['category_name'] = category
        
        # Technology (depends on Category)
        if category:
            technology = self.render_cascading_dropdown('technology', parent_value=category, key_suffix=key_suffix)
            selected_values['technology'] = technology
        else:
            st.info("👆 Select a category first to choose technology")
            selected_values['technology'] = ""
        
        # Work Item (depends on Technology)
        if selected_values.get('technology'):
            work_item = self.render_cascading_dropdown('work_item', parent_value=selected_values['technology'], key_suffix=key_suffix)
            selected_values['work_item'] = work_item
        else:
            if category:  # Only show if category is selected
                st.info("👆 Select a technology first to choose work item")
            selected_values['work_item'] = ""
        
        # Skill/Topic (depends on Work Item)
        if selected_values.get('work_item'):
            skill = self.render_cascading_dropdown('skill_topic', parent_value=selected_values['work_item'], key_suffix=key_suffix)
            selected_values['skill_topic'] = skill
        else:
            if selected_values.get('technology'):  # Only show if technology is selected
                st.info("👆 Select a work item first to choose skill/topic")
            selected_values['skill_topic'] = ""
        
        return selected_values
    
    def render_independent_dropdown(self, field_name: str, key_suffix: str = "") -> str:
        """Render independent dropdown fields (no hierarchy)."""
        
        if field_name not in self.independent_fields:
            return ""
        
        field_config = self.independent_fields[field_name]
        
        if 'options' in field_config:
            # Fixed options dropdown
            return st.selectbox(
                field_config['label'],
                options=field_config['options'],
                key=f"{field_name}_indep_{key_suffix}"
            )
        else:
            # Text input with auto-populate suggestions
            existing = self.db.get_dropdown_values(field_name)
            
            value = st.text_input(
                field_config['label'],
                placeholder=field_config.get('placeholder', ''),
                key=f"{field_name}_indep_{key_suffix}"
            )
            
            # Show suggestions if available
            if existing and not value:
                st.caption(f"💡 Recent: {', '.join(existing[:5])}")
            
            # Auto-save if value provided
            if value and value.strip():
                self.db.add_dropdown_value(field_name, value.strip())
            
            return value if value else ""
    
    def get_all_dropdown_data(self) -> Dict[str, List[str]]:
        """Get all dropdown values organized by field name."""
        
        all_data = {}
        
        # Get hierarchical fields
        for field_name in self.hierarchy.keys():
            all_data[field_name] = self.db.get_dropdown_values(field_name)
        
        # Get independent fields
        for field_name in ['category_source', 'session_type', 'difficulty', 'status']:
            all_data[field_name] = self.db.get_dropdown_values(field_name)
        
        return all_data
    
    def delete_dropdown_entry(self, field_name: str, field_value: str) -> bool:
        """Delete a dropdown entry."""
        return self.db.delete_dropdown_value(field_name, field_value)
    
    def get_dependency_chain(self, field_name: str) -> List[str]:
        """Get the full dependency chain for a field."""
        chain = []
        current = field_name
        
        while current:
            chain.insert(0, current)
            parent = self.hierarchy.get(current, {}).get('parent')
            current = parent
        
        return chain
