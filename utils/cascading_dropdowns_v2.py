"""
Dropdown Manager V2 - Fixes form-dropdown race condition.
Collects dropdown values in session state and saves only on form submit.
"""

import streamlit as st
from typing import List, Dict, Optional
from database.operations import DatabaseStorage

class DropdownManagerV2:
    """Manages hierarchical dropdown dependencies without auto-save race conditions."""
    
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
        """Render cascading dropdown reading directly from source tables."""
        
        if field_name not in self.hierarchy:
            return ""
        
        field_config = self.hierarchy[field_name]
        parent_field = field_config['parent']
        
        # Get existing values from source tables (not dropdowns table)
        if field_name == 'category_name':
            # Read from categories table
            existing_values = self.db.get_all_categories()
        
        elif field_name == 'technology':
            if parent_value:
                # Read from tech_stack table filtered by category
                existing_values = self.db.get_technologies_by_category(parent_value)
            else:
                # No category selected - show empty
                existing_values = []
        
        elif field_name == 'work_item':
            if parent_value:
                # Read work items (hybrid: manual + auto-populated from sessions)
                existing_values = self.db.get_work_items_by_technology(parent_value)
            else:
                # No technology selected - show empty
                existing_values = []
        
        elif field_name == 'skill_topic':
            if parent_value:
                # Read skills (hybrid: manual + auto-populated from sessions)
                existing_values = self.db.get_skills_by_work_item(parent_value)
            else:
                # No work item selected - show empty
                existing_values = []
        
        else:
            # Fallback for any other fields
            existing_values = []
        
        # Display label
        st.markdown(f"**{field_config['label']}**")
        
        if allow_new:
            # Dropdown with option to add new
            options = ["➕ Type New..."] + existing_values if existing_values else ["➕ Type New..."]
            
            # Add helper text if parent is empty
            help_text = None
            if parent_field and not parent_value:
                help_text = f"Select {parent_field.replace('_', ' ')} first for filtered options"
            
            selected = st.selectbox(
                f"{field_name}_dropdown_{key_suffix}",
                options=options,
                label_visibility="collapsed",
                key=f"{field_name}_select_{key_suffix}",
                help=help_text
            )
            
            # If user wants to add new, show text input (NO AUTO-SAVE)
            if selected == "➕ Type New...":
                new_value = st.text_input(
                    f"New {field_config['label']}",
                    placeholder=field_config['placeholder'],
                    key=f"{field_name}_new_{key_suffix}",
                    label_visibility="collapsed"
                )
                
                # Store in session state for later save
                if new_value and new_value.strip():
                    pending_key = f"pending_{field_name}_{key_suffix}"
                    st.session_state[pending_key] = {
                        'field_name': field_name,
                        'field_value': new_value.strip(),
                        'parent_field': parent_field,
                        'parent_value': parent_value
                    }
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
    
    def render_simplified_form(self, key_suffix: str = "") -> Dict[str, str]:
        """Render simplified form - ALL options shown, NO parent filtering.
        Relationships are auto-paired in the background from database lookups.
        """
        
        selected_values = {}
        
        # Technology - Show ALL technologies (no category filter)
        st.markdown("**🔧 Technology**")
        all_techs = [tech['name'] for tech in self.db.get_all_tech_stack()]
        if all_techs:
            technology = st.selectbox(
                "technology_dropdown",
                options=all_techs,
                key=f"technology_simple_{key_suffix}",
                label_visibility="collapsed",
                help="Select the technology you worked on"
            )
            selected_values['technology'] = technology
        else:
            st.warning("⚠️ No technologies available. Add them in Dropdown Manager first.")
            selected_values['technology'] = ''
        
        # Work Item - Show ALL work items (no technology filter) 
        st.markdown("**📋 Work Item**")
        all_work_items = []
        # Get all work items from both manual + auto-populated
        all_techs_list = [tech['name'] for tech in self.db.get_all_tech_stack()]
        for tech in all_techs_list:
            all_work_items.extend(self.db.get_work_items_by_technology(tech))
        # Remove duplicates
        all_work_items = sorted(list(set(all_work_items)))
        
        if all_work_items:
            work_item = st.selectbox(
                "work_item_dropdown",
                options=[""] + all_work_items,  # Allow empty selection
                key=f"work_item_simple_{key_suffix}",
                label_visibility="collapsed",
                help="Select a work item or leave empty"
            )
            selected_values['work_item'] = work_item if work_item else ''
        else:
            selected_values['work_item'] = ''
        
        # Skill/Topic - Freeform text input
        st.markdown("**🎯 Skill / Topic**")
        skill = st.text_input(
            "skill_topic_input",
            placeholder="Type the skill or topic you worked on...",
            key=f"skill_topic_simple_{key_suffix}",
            label_visibility="collapsed",
            help="Enter any skill or topic - this is freeform text"
        )
        selected_values['skill_topic'] = skill.strip() if skill else ''
        
        # Auto-pair category in background (lookup from technology)
        if selected_values['technology']:
            # Find the category for this technology
            tech_stack = self.db.get_all_tech_stack()
            for tech in tech_stack:
                if tech['name'] == selected_values['technology']:
                    selected_values['category_name'] = tech.get('category', '')
                    break
        else:
            selected_values['category_name'] = ''
        
        return selected_values
    
    def render_hierarchical_form(self, key_suffix: str = "") -> Dict[str, str]:
        """Render complete hierarchical dropdown form with state-based clearing.
        
        Updated design:
        - Category, Technology, Work Item: Dropdown only (no text input)
        - Skill/Topic: Text input only (no dropdown)
        """
        
        selected_values = {}
        state_key = f"dropdown_state_{key_suffix}"
        
        # Initialize state if not exists
        if state_key not in st.session_state:
            st.session_state[state_key] = {
                'category_name': '',
                'technology': '',
                'work_item': '',
                'skill_topic': ''
            }
        
        prev_state = st.session_state[state_key].copy()
        
        # Category Name (root) - Dropdown only (no text input for new values)
        category = self.render_cascading_dropdown('category_name', key_suffix=key_suffix, allow_new=False)
        selected_values['category_name'] = category
        
        # Clear children if category changed
        if category != prev_state['category_name']:
            st.session_state[state_key]['technology'] = ''
            st.session_state[state_key]['work_item'] = ''
            st.session_state[state_key]['skill_topic'] = ''
        
        # Technology (depends on Category) - Dropdown only (no text input for new values)
        technology = self.render_cascading_dropdown('technology', parent_value=category if category else None, key_suffix=key_suffix, allow_new=False)
        selected_values['technology'] = technology
        
        # Clear children if technology changed
        if technology != prev_state['technology']:
            st.session_state[state_key]['work_item'] = ''
            st.session_state[state_key]['skill_topic'] = ''
        
        # Work Item (depends on Technology) - Dropdown only (no text input for new values)
        work_item = self.render_cascading_dropdown('work_item', parent_value=technology if technology else None, key_suffix=key_suffix, allow_new=False)
        selected_values['work_item'] = work_item
        
        # Clear children if work_item changed
        if work_item != prev_state['work_item']:
            st.session_state[state_key]['skill_topic'] = ''
        
        # Skill/Topic (freeform text input - no dropdown)
        st.markdown("**🎯 Skill / Topic**")
        skill = st.text_input(
            "skill_topic_input",
            placeholder="Type the skill or topic you worked on...",
            key=f"skill_topic_text_{key_suffix}",
            label_visibility="collapsed",
            help="Enter any skill or topic - this is freeform text"
        )
        selected_values['skill_topic'] = skill.strip() if skill else ''
        
        # Update state
        st.session_state[state_key] = selected_values.copy()
        
        return selected_values
    
    def save_pending_dropdowns(self, key_suffix: str = "") -> bool:
        """Save all pending dropdown values collected during form interaction."""
        saved_count = 0
        
        # Find all pending dropdown values in session state
        for key in list(st.session_state.keys()):
            # Check if key is string before calling string methods
            if isinstance(key, str) and key.startswith(f"pending_") and key.endswith(f"_{key_suffix}"):
                pending_data = st.session_state[key]
                
                # Save to database
                self.db.add_dropdown_value(
                    field_name=pending_data['field_name'],
                    field_value=pending_data['field_value'],
                    parent_field=pending_data.get('parent_field'),
                    parent_value=pending_data.get('parent_value')
                )
                
                # Clear from session state
                del st.session_state[key]
                saved_count += 1
        
        return saved_count > 0
    
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
            # Text input with auto-populate suggestions (NO AUTO-SAVE)
            existing = self.db.get_dropdown_values(field_name)
            
            value = st.text_input(
                field_config['label'],
                placeholder=field_config.get('placeholder', ''),
                key=f"{field_name}_indep_{key_suffix}"
            )
            
            # Show suggestions if available
            if existing and not value:
                st.caption(f"💡 Recent: {', '.join(existing[:5])}")
            
            # Store for later save
            if value and value.strip():
                st.session_state[f"pending_{field_name}_{key_suffix}"] = {
                    'field_name': field_name,
                    'field_value': value.strip(),
                    'parent_field': None,
                    'parent_value': None
                }
            
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
