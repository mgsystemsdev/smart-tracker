"""
Data storage module for Smart Tracker.
Handles saving and loading session data to/from JSON files.
"""

import json
from pathlib import Path
from typing import List, Dict, Any, Optional

SKILL_DOMAINS = [
    "🌐 Core Full-Stack Development",
    "📊 Data Science & Machine Learning",
    "📑 Excel Automation & Data Handling",
    "⚙️ Core Automation (Support Layer)",
    "🔒 Reliability & Security",
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
        """Load tech stack from JSON file with automatic migration for domain field."""
        try:
            if self.tech_stack_file.exists():
                with open(self.tech_stack_file, 'r') as f:
                    tech_stack = json.load(f)
                
                needs_save = False
                for tech in tech_stack:
                    if "domain" not in tech:
                        tech["domain"] = "❓ Uncategorized"
                        needs_save = True
                    if "subsection" not in tech:
                        tech["subsection"] = None
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
