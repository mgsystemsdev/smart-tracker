"""
Data storage module for Smart Tracker.
Handles saving and loading session data to/from JSON files.
"""

import json
from pathlib import Path
from typing import List, Dict, Any, Optional

TECH_CATEGORIES = [
    "🖥️ Front-End",
    "⚙️ Back-End",
    "🔗 Lightweight APIs / Model Serving",
    "🌉 Integration",
    "☁️ Deployment",
    "🧮 Core Libraries",
    "📈 Visualization",
    "🤖 Machine Learning",
    "🔄 Pipelines",
    "🗄️ Databases",
    "📑 Excel Automation",
    "⚙️ Automation",
    "🔒 Security & Testing",
    "🧰 Supporting Skills",
    "❓ Uncategorized"
]


class JSONStorage:
    """Handles JSON-based storage for learning sessions and configuration."""
    
    def __init__(self, data_dir: str = "data"):
        """Initialize storage with data directory."""
        self.data_dir = Path(data_dir)
        self.data_dir.mkdir(exist_ok=True)
        
        self.sessions_file = self.data_dir / "learning_sessions.json"
        self.tech_stack_file = self.data_dir / "tech_stack.json"
        self.custom_categories_file = self.data_dir / "custom_categories.json"
    
    def save_sessions(self, sessions: List[Dict[str, Any]]) -> bool:
        """Save learning sessions to JSON file."""
        try:
            with open(self.sessions_file, 'w') as f:
                json.dump(sessions, f, indent=2)
            return True
        except Exception as e:
            print(f"Error saving sessions: {e}")
            return False
    
    def load_sessions(self) -> List[Dict[str, Any]]:
        """Load learning sessions from JSON file."""
        try:
            if self.sessions_file.exists():
                with open(self.sessions_file, 'r') as f:
                    return json.load(f)
            return []
        except Exception as e:
            print(f"Error loading sessions: {e}")
            return []
    
    def save_tech_stack(self, tech_stack: List[Dict[str, Any]]) -> bool:
        """Save tech stack to JSON file."""
        try:
            with open(self.tech_stack_file, 'w') as f:
                json.dump(tech_stack, f, indent=2)
            return True
        except Exception as e:
            print(f"Error saving tech stack: {e}")
            return False
    
    def load_tech_stack(self) -> List[Dict[str, Any]]:
        """Load tech stack from JSON file with automatic migration to category field."""
        try:
            if self.tech_stack_file.exists():
                with open(self.tech_stack_file, 'r') as f:
                    tech_stack = json.load(f)
                
                all_categories = self.get_all_categories()
                needs_save = False
                for tech in tech_stack:
                    current_category = tech.get("category", "")
                    
                    if current_category not in all_categories:
                        tech["category"] = "❓ Uncategorized"
                        needs_save = True
                    
                    if "domain" in tech:
                        del tech["domain"]
                        needs_save = True
                    
                    if "subsection" in tech:
                        del tech["subsection"]
                        needs_save = True
                
                if needs_save:
                    self.save_tech_stack(tech_stack)
                
                return tech_stack
            return []
        except Exception as e:
            print(f"Error loading tech stack: {e}")
            return []
    
    def backup_data(self, backup_name: Optional[str] = None) -> str:
        """Create a backup of all data files."""
        import shutil
        from datetime import datetime
        
        if backup_name is None:
            backup_name = f"backup_{datetime.now().strftime('%Y%m%d_%H%M%S')}"
        
        backup_dir = self.data_dir / "backups" / backup_name
        backup_dir.mkdir(parents=True, exist_ok=True)
        
        # Backup sessions
        if self.sessions_file.exists():
            shutil.copy2(self.sessions_file, backup_dir / "learning_sessions.json")
        
        # Backup tech stack
        if self.tech_stack_file.exists():
            shutil.copy2(self.tech_stack_file, backup_dir / "tech_stack.json")
        
        return str(backup_dir)
    
    def save_custom_categories(self, custom_categories: List[str]) -> bool:
        """Save custom categories to JSON file."""
        try:
            with open(self.custom_categories_file, 'w') as f:
                json.dump(custom_categories, f, indent=2)
            return True
        except Exception as e:
            print(f"Error saving custom categories: {e}")
            return False
    
    def load_custom_categories(self) -> List[str]:
        """Load custom categories from JSON file."""
        try:
            if self.custom_categories_file.exists():
                with open(self.custom_categories_file, 'r') as f:
                    return json.load(f)
            return []
        except Exception as e:
            print(f"Error loading custom categories: {e}")
            return []
    
    def get_all_categories(self) -> List[str]:
        """Get all categories: hardcoded TECH_CATEGORIES + custom categories."""
        custom_cats = self.load_custom_categories()
        all_cats = TECH_CATEGORIES.copy()
        
        for cat in custom_cats:
            if cat not in all_cats:
                all_cats.insert(-1, cat)
        
        return all_cats
    
    def add_custom_category(self, category_name: str) -> bool:
        """Add a new custom category if it doesn't exist."""
        if not category_name or not category_name.strip():
            return False
        
        category_name = category_name.strip()
        
        all_categories = self.get_all_categories()
        if category_name in all_categories:
            return False
        
        custom_categories = self.load_custom_categories()
        custom_categories.append(category_name)
        return self.save_custom_categories(custom_categories)
    
    def rename_custom_category(self, old_name: str, new_name: str) -> bool:
        """Rename a custom category and update all technologies using it."""
        if not old_name or not new_name or not old_name.strip() or not new_name.strip():
            return False
        
        old_name = old_name.strip()
        new_name = new_name.strip()
        
        if old_name in TECH_CATEGORIES:
            return False
        
        custom_categories = self.load_custom_categories()
        if old_name not in custom_categories:
            return False
        
        if new_name in self.get_all_categories():
            return False
        
        custom_categories = [new_name if cat == old_name else cat for cat in custom_categories]
        self.save_custom_categories(custom_categories)
        
        tech_stack = self.load_tech_stack()
        updated = False
        for tech in tech_stack:
            if tech.get('category') == old_name:
                tech['category'] = new_name
                updated = True
        
        if updated:
            self.save_tech_stack(tech_stack)
        
        return True
    
    def delete_custom_category(self, category_name: str) -> bool:
        """Delete a custom category and reassign technologies to Uncategorized."""
        if not category_name or not category_name.strip():
            return False
        
        category_name = category_name.strip()
        
        if category_name in TECH_CATEGORIES:
            return False
        
        custom_categories = self.load_custom_categories()
        if category_name not in custom_categories:
            return False
        
        custom_categories = [cat for cat in custom_categories if cat != category_name]
        self.save_custom_categories(custom_categories)
        
        tech_stack = self.load_tech_stack()
        updated = False
        for tech in tech_stack:
            if tech.get('category') == category_name:
                tech['category'] = "❓ Uncategorized"
                updated = True
        
        if updated:
            self.save_tech_stack(tech_stack)
        
        return True
    
    def merge_categories(self, source_category: str, target_category: str) -> bool:
        """Merge source category into target category, updating all technologies."""
        if not source_category or not target_category:
            return False
        
        source_category = source_category.strip()
        target_category = target_category.strip()
        
        all_categories = self.get_all_categories()
        if source_category not in all_categories or target_category not in all_categories:
            return False
        
        if source_category == target_category:
            return False
        
        tech_stack = self.load_tech_stack()
        updated = False
        for tech in tech_stack:
            if tech.get('category') == source_category:
                tech['category'] = target_category
                updated = True
        
        if updated:
            self.save_tech_stack(tech_stack)
        
        if source_category not in TECH_CATEGORIES:
            custom_categories = self.load_custom_categories()
            custom_categories = [cat for cat in custom_categories if cat != source_category]
            self.save_custom_categories(custom_categories)
        
        return True
