"""
Data Synchronization Service - Unified CRUD operations for technologies and categories.
Ensures tech_stack and dropdowns tables stay in sync.
"""

import logging
from typing import Optional, Dict, List, Any
from src.database.operations import DatabaseStorage

class TechnologySyncService:
    """Unified service for technology operations across tech_stack and dropdowns."""
    
    def __init__(self, db: DatabaseStorage):
        self.db = db
    
    def add_technology(self, name: str, category: str, goal_hours: float, date_added: str) -> Dict[str, Any]:
        """Add technology to BOTH tech_stack and dropdowns tables atomically."""
        try:
            # 1. Add to tech_stack table
            tech_id = self.db.add_technology(
                name=name,
                category=category,
                goal_hours=goal_hours,
                date_added=date_added
            )
            
            if tech_id > 0:
                # 2. Add to dropdowns table (for session form dropdowns)
                self.db.add_dropdown_value(
                    field_name='technology',
                    field_value=name,
                    parent_field='category_name',
                    parent_value=category
                )
                
                logging.info(f"TechnologySyncService: Added {name} to both tech_stack and dropdowns")
                return {'success': True, 'tech_id': tech_id, 'message': f'Added {name} successfully'}
            elif tech_id == -1:
                return {'success': False, 'tech_id': -1, 'message': f'{name} already exists'}
            else:
                return {'success': False, 'tech_id': 0, 'message': 'Failed to add technology'}
                
        except Exception as e:
            logging.error(f"TechnologySyncService.add_technology error: {e}")
            return {'success': False, 'tech_id': 0, 'message': str(e)}
    
    def update_technology(self, tech_id: int, name: Optional[str] = None, 
                         category: Optional[str] = None, goal_hours: Optional[float] = None) -> Dict[str, Any]:
        """Update technology in BOTH tables and update all sessions using it."""
        try:
            # Get current tech data
            tech_stack = self.db.get_all_tech_stack()
            current_tech = next((t for t in tech_stack if t['id'] == tech_id), None)
            
            if not current_tech:
                return {'success': False, 'message': 'Technology not found'}
            
            old_name = current_tech['name']
            new_name = name if name else old_name
            new_category = category if category else current_tech['category']
            
            # 1. Update tech_stack table
            if self.db.update_technology(tech_id, name=new_name, category=new_category, goal_hours=goal_hours):
                
                # 2. If name changed, update dropdowns table
                if name and name != old_name:
                    # Delete old dropdown entry
                    self.db.delete_dropdown_value('technology', old_name)
                    
                    # Add new dropdown entry
                    self.db.add_dropdown_value(
                        field_name='technology',
                        field_value=new_name,
                        parent_field='category_name',
                        parent_value=new_category
                    )
                    
                    # 3. Update all sessions using this technology
                    self.db.update_sessions_technology(old_name, new_name)
                    
                    logging.info(f"TechnologySyncService: Renamed {old_name} to {new_name} across all tables")
                
                return {'success': True, 'message': f'Updated {new_name} successfully'}
            else:
                return {'success': False, 'message': 'Failed to update technology'}
                
        except Exception as e:
            logging.error(f"TechnologySyncService.update_technology error: {e}")
            return {'success': False, 'message': str(e)}
    
    def delete_technology(self, tech_id: int) -> Dict[str, Any]:
        """Delete technology with safety checks - verify session usage first."""
        try:
            # Get tech data
            tech_stack = self.db.get_all_tech_stack()
            tech = next((t for t in tech_stack if t['id'] == tech_id), None)
            
            if not tech:
                return {'success': False, 'message': 'Technology not found'}
            
            tech_name = tech['name']
            
            # Check if used in sessions
            session_count = self.db.count_sessions_by_technology(tech_name)
            
            if session_count > 0:
                return {
                    'success': False, 
                    'message': f'Cannot delete: {tech_name} is used in {session_count} session(s)',
                    'session_count': session_count,
                    'requires_confirmation': True
                }
            
            # Safe to delete - delete from BOTH tables
            # 1. Delete from tech_stack
            if self.db.delete_technology(tech_id):
                # 2. Delete from dropdowns
                self.db.delete_dropdown_value('technology', tech_name)
                
                logging.info(f"TechnologySyncService: Deleted {tech_name} from both tables")
                return {'success': True, 'message': f'Deleted {tech_name} successfully'}
            else:
                return {'success': False, 'message': 'Failed to delete technology'}
                
        except Exception as e:
            logging.error(f"TechnologySyncService.delete_technology error: {e}")
            return {'success': False, 'message': str(e)}
    
    def force_delete_technology(self, tech_id: int) -> Dict[str, Any]:
        """Force delete technology even if used in sessions (marks sessions as 'Deleted: <name>')."""
        try:
            tech_stack = self.db.get_all_tech_stack()
            tech = next((t for t in tech_stack if t['id'] == tech_id), None)
            
            if not tech:
                return {'success': False, 'message': 'Technology not found'}
            
            tech_name = tech['name']
            
            # 1. Update sessions to mark technology as deleted
            self.db.update_sessions_technology(tech_name, f"[Deleted] {tech_name}")
            
            # 2. Delete from tech_stack
            self.db.delete_technology(tech_id)
            
            # 3. Delete from dropdowns
            self.db.delete_dropdown_value('technology', tech_name)
            
            logging.info(f"TechnologySyncService: Force deleted {tech_name}")
            return {'success': True, 'message': f'Force deleted {tech_name} and updated sessions'}
            
        except Exception as e:
            logging.error(f"TechnologySyncService.force_delete_technology error: {e}")
            return {'success': False, 'message': str(e)}


class CategorySyncService:
    """Unified service for category operations across categories and dropdowns."""
    
    def __init__(self, db: DatabaseStorage):
        self.db = db
    
    def add_category(self, category_name: str, is_custom: bool = True) -> Dict[str, Any]:
        """Add category to BOTH categories and dropdowns tables."""
        try:
            # 1. Add to categories table
            if self.db.add_category(category_name, is_custom=is_custom):
                
                # 2. Add to dropdowns table (for session form)
                self.db.add_dropdown_value(
                    field_name='category_name',
                    field_value=category_name
                )
                
                logging.info(f"CategorySyncService: Added {category_name} to both tables")
                return {'success': True, 'message': f'Added {category_name} successfully'}
            else:
                return {'success': False, 'message': f'{category_name} already exists'}
                
        except Exception as e:
            logging.error(f"CategorySyncService.add_category error: {e}")
            return {'success': False, 'message': str(e)}
    
    def rename_category(self, old_name: str, new_name: str) -> Dict[str, Any]:
        """Rename category everywhere: categories table, dropdowns, tech_stack, sessions."""
        try:
            # 1. Rename in categories table
            if self.db.rename_category(old_name, new_name):
                
                # 2. Update dropdowns table
                self.db.delete_dropdown_value('category_name', old_name)
                self.db.add_dropdown_value('category_name', new_name)
                
                # 3. Update all tech_stack entries
                self.db.update_tech_stack_category(old_name, new_name)
                
                # 4. Update all sessions
                self.db.update_sessions_category(old_name, new_name)
                
                logging.info(f"CategorySyncService: Renamed {old_name} to {new_name} across all tables")
                return {'success': True, 'message': f'Renamed to {new_name} successfully'}
            else:
                return {'success': False, 'message': 'Failed to rename category'}
                
        except Exception as e:
            logging.error(f"CategorySyncService.rename_category error: {e}")
            return {'success': False, 'message': str(e)}
    
    def delete_category(self, category_name: str) -> Dict[str, Any]:
        """Delete category and migrate technologies/sessions to 'Uncategorized'."""
        try:
            # 1. Migrate tech_stack entries to Uncategorized
            tech_stack = self.db.get_all_tech_stack()
            tech_count = sum(1 for t in tech_stack if t.get('category') == category_name)
            
            if tech_count > 0:
                self.db.update_tech_stack_category(category_name, '❓ Uncategorized')
            
            # 2. Migrate sessions to Uncategorized
            session_count = self.db.count_sessions_by_category(category_name)
            if session_count > 0:
                self.db.update_sessions_category(category_name, '❓ Uncategorized')
            
            # 3. Delete from categories table
            if self.db.delete_category(category_name):
                
                # 4. Delete from dropdowns table
                self.db.delete_dropdown_value('category_name', category_name)
                
                logging.info(f"CategorySyncService: Deleted {category_name}, migrated {tech_count} techs and {session_count} sessions")
                return {
                    'success': True, 
                    'message': f'Deleted {category_name}. Migrated {tech_count} technologies and {session_count} sessions to Uncategorized'
                }
            else:
                return {'success': False, 'message': 'Failed to delete category'}
                
        except Exception as e:
            logging.error(f"CategorySyncService.delete_category error: {e}")
            return {'success': False, 'message': str(e)}
