"""
Data migration utility to convert JSON storage to SQLite database.
Transforms old data model to new 13-field hierarchical structure.
"""

import json
import logging
from pathlib import Path
from datetime import datetime
from typing import Dict, List, Any
from smarttracker.domain.db_storage import DatabaseStorage

logging.basicConfig(level=logging.INFO)

class DataMigration:
    """Handles migration from JSON to SQLite database."""
    
    def __init__(self, data_dir: str = "data"):
        self.data_dir = Path(data_dir)
        self.sessions_file = self.data_dir / "learning_sessions.json"
        self.tech_stack_file = self.data_dir / "tech_stack.json"
        self.custom_cat_file = self.data_dir / "custom_categories.json"
        self.db = DatabaseStorage()
    
    def load_json_data(self) -> tuple[List[Dict], List[Dict], List[str]]:
        """Load existing JSON data."""
        sessions = []
        tech_stack = []
        custom_categories = []
        
        # Load sessions
        if self.sessions_file.exists():
            with open(self.sessions_file, 'r') as f:
                sessions = json.load(f)
                logging.info(f"Loaded {len(sessions)} sessions from JSON")
        
        # Load tech stack
        if self.tech_stack_file.exists():
            with open(self.tech_stack_file, 'r') as f:
                tech_stack = json.load(f)
                logging.info(f"Loaded {len(tech_stack)} technologies from JSON")
        
        # Load custom categories
        if self.custom_cat_file.exists():
            with open(self.custom_cat_file, 'r') as f:
                data = json.load(f)
                custom_categories = data.get('categories', [])
                logging.info(f"Loaded {len(custom_categories)} custom categories from JSON")
        
        return sessions, tech_stack, custom_categories
    
    def initialize_base_categories(self):
        """Initialize the base category system."""
        base_categories = [
            "🌐 Front-End",
            "⚙️ Back-End",
            "📚 Core Libraries",
            "📊 Visualization",
            "🤖 Machine Learning",
            "🔄 Pipelines",
            "🗄️ Databases",
            "🚀 Deployment",
            "📊 Excel",
            "🤖 Automation",
            "🔒 Security",
            "🧰 Supporting Skills",
            "❓ Uncategorized"
        ]
        
        for category in base_categories:
            self.db.add_category(category, is_custom=False)
            logging.info(f"Added base category: {category}")
    
    def migrate_custom_categories(self, custom_categories: List[str]):
        """Migrate custom categories."""
        for category in custom_categories:
            self.db.add_category(category, is_custom=True)
            logging.info(f"Migrated custom category: {category}")
    
    def transform_session(self, old_session: Dict[str, Any]) -> Dict[str, Any]:
        """Transform old session format to new 13-field structure."""
        
        # Map old fields to new structure
        new_session = {
            'session_date': old_session.get('date', datetime.now().strftime('%Y-%m-%d')),
            'session_type': old_session.get('type', 'Practice'),  # Default to Practice
            'category_name': old_session.get('category_name', '❓ Uncategorized'),
            'technology': old_session.get('technology', 'Unknown'),
            'work_item': old_session.get('work_item', old_session.get('topic', '')),
            'skill_topic': old_session.get('skill', old_session.get('topic', '')),
            'category_source': old_session.get('category_source', ''),
            'difficulty': old_session.get('difficulty', 'Intermediate'),
            'status': old_session.get('status', 'Completed'),
            'hours_spent': old_session.get('hours', 1.0),
            'tags': old_session.get('tags', ''),
            'notes': old_session.get('notes', '')
        }
        
        return new_session
    
    def migrate_sessions(self, sessions: List[Dict]):
        """Migrate all sessions to database."""
        migrated_count = 0
        
        for session in sessions:
            try:
                new_session = self.transform_session(session)
                session_id = self.db.add_session(new_session)
                
                if session_id > 0:
                    migrated_count += 1
                    
                    # Auto-populate dropdowns from session data
                    self._add_to_dropdowns(new_session)
                    
            except Exception as e:
                logging.error(f"Error migrating session: {e}")
                logging.error(f"Session data: {session}")
        
        logging.info(f"Migrated {migrated_count}/{len(sessions)} sessions successfully")
    
    def migrate_tech_stack(self, tech_stack: List[Dict]):
        """Migrate tech stack to database."""
        migrated_count = 0
        
        for tech in tech_stack:
            try:
                tech_id = self.db.add_technology(
                    name=tech.get('name', 'Unknown'),
                    category=tech.get('category', '❓ Uncategorized'),
                    goal_hours=tech.get('goal_hours', 50),
                    date_added=tech.get('date_added', datetime.now().strftime('%Y-%m-%d'))
                )
                
                if tech_id > 0:
                    migrated_count += 1
            except Exception as e:
                logging.error(f"Error migrating technology: {e}")
                logging.error(f"Tech data: {tech}")
        
        logging.info(f"Migrated {migrated_count}/{len(tech_stack)} technologies successfully")
    
    def _add_to_dropdowns(self, session: Dict[str, Any]):
        """Populate dropdown tables from session data."""
        # Add Category Name (root)
        if session['category_name']:
            self.db.add_dropdown_value('category_name', session['category_name'])
        
        # Add Technology (depends on Category)
        if session['technology'] and session['category_name']:
            self.db.add_dropdown_value(
                'technology', 
                session['technology'],
                parent_field='category_name',
                parent_value=session['category_name']
            )
        
        # Add Work Item (depends on Technology)
        if session['work_item'] and session['technology']:
            self.db.add_dropdown_value(
                'work_item',
                session['work_item'],
                parent_field='technology',
                parent_value=session['technology']
            )
        
        # Add Skill/Topic (depends on Work Item)
        if session['skill_topic'] and session['work_item']:
            self.db.add_dropdown_value(
                'skill_topic',
                session['skill_topic'],
                parent_field='work_item',
                parent_value=session['work_item']
            )
        
        # Add other dropdown values without dependencies
        if session['category_source']:
            self.db.add_dropdown_value('category_source', session['category_source'])
        
        if session['difficulty']:
            self.db.add_dropdown_value('difficulty', session['difficulty'])
        
        if session['status']:
            self.db.add_dropdown_value('status', session['status'])
    
    def create_backup(self):
        """Create backup of JSON files before migration."""
        timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
        backup_dir = self.data_dir / f"backup_{timestamp}"
        backup_dir.mkdir(exist_ok=True)
        
        if self.sessions_file.exists():
            import shutil
            shutil.copy2(self.sessions_file, backup_dir / "learning_sessions.json")
            logging.info(f"Backed up sessions to {backup_dir}")
        
        if self.tech_stack_file.exists():
            import shutil
            shutil.copy2(self.tech_stack_file, backup_dir / "tech_stack.json")
            logging.info(f"Backed up tech stack to {backup_dir}")
    
    def run_migration(self, create_backup: bool = True):
        """Execute complete migration process."""
        logging.info("=" * 60)
        logging.info("Starting Smart Tracker v2.0 Data Migration")
        logging.info("=" * 60)
        
        # Create backup if requested
        if create_backup:
            self.create_backup()
        
        # Load JSON data
        sessions, tech_stack, custom_categories = self.load_json_data()
        
        # Initialize base categories
        logging.info("Initializing base category system...")
        self.initialize_base_categories()
        
        # Migrate custom categories
        if custom_categories:
            logging.info("Migrating custom categories...")
            self.migrate_custom_categories(custom_categories)
        
        # Migrate tech stack
        if tech_stack:
            logging.info("Migrating tech stack...")
            self.migrate_tech_stack(tech_stack)
        
        # Migrate sessions
        if sessions:
            logging.info("Migrating learning sessions...")
            self.migrate_sessions(sessions)
        
        logging.info("=" * 60)
        logging.info("Migration completed successfully!")
        logging.info("=" * 60)
        
        # Print summary
        total_sessions = len(self.db.get_all_sessions())
        total_tech = len(self.db.get_all_tech_stack())
        total_categories = len(self.db.get_all_categories())
        
        logging.info(f"Database Summary:")
        logging.info(f"  - Total Sessions: {total_sessions}")
        logging.info(f"  - Total Technologies: {total_tech}")
        logging.info(f"  - Total Categories: {total_categories}")
        logging.info(f"  - Total Hours: {self.db.get_total_hours():.1f}")
        
        # Close database connection
        self.db.close()

def main():
    """Run migration from command line."""
    migration = DataMigration()
    migration.run_migration(create_backup=True)

if __name__ == "__main__":
    main()
