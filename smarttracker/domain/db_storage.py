"""
SQLite database storage layer for Smart Tracker v2.0.
Provides persistent storage with structured tables and relationships.
"""

import sqlite3
import json
from pathlib import Path
from typing import List, Dict, Any, Optional, Tuple
from datetime import datetime
import logging

class DatabaseStorage:
    """SQLite database storage manager for Smart Tracker."""
    
    def __init__(self, db_path: str = "data/smart_tracker.db"):
        """Initialize database connection and create tables if needed."""
        self.db_path = Path(db_path)
        self.db_path.parent.mkdir(exist_ok=True)
        self.conn = None
        self._initialize_database()
    
    def _get_connection(self) -> sqlite3.Connection:
        """Get database connection with row factory."""
        if self.conn is None:
            # Use check_same_thread=False for Streamlit compatibility (multi-threaded environment)
            self.conn = sqlite3.connect(self.db_path, check_same_thread=False)
            self.conn.row_factory = sqlite3.Row
        return self.conn
    
    def _initialize_database(self):
        """Create database tables if they don't exist."""
        conn = self._get_connection()
        cursor = conn.cursor()
        
        # Sessions table - main learning session data
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS sessions (
                session_id INTEGER PRIMARY KEY AUTOINCREMENT,
                session_date TEXT NOT NULL,
                session_type TEXT NOT NULL,
                category_name TEXT NOT NULL,
                technology TEXT NOT NULL,
                work_item TEXT,
                skill_topic TEXT,
                category_source TEXT,
                difficulty TEXT,
                status TEXT,
                hours_spent REAL NOT NULL,
                tags TEXT,
                notes TEXT,
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
            )
        ''')
        
        # Tech stack table
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS tech_stack (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                name TEXT UNIQUE NOT NULL,
                category TEXT NOT NULL,
                goal_hours REAL DEFAULT 50,
                date_added TEXT NOT NULL,
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
            )
        ''')
        
        # Dropdowns table - hierarchical dropdown values
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS dropdowns (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                field_name TEXT NOT NULL,
                field_value TEXT NOT NULL,
                parent_field TEXT,
                parent_value TEXT,
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                UNIQUE(field_name, field_value, parent_field, parent_value)
            )
        ''')
        
        # Categories table
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS categories (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                category_name TEXT UNIQUE NOT NULL,
                is_custom INTEGER DEFAULT 0,
                date_added TEXT NOT NULL,
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
            )
        ''')
        
        # Create indexes for better query performance
        cursor.execute('CREATE INDEX IF NOT EXISTS idx_sessions_date ON sessions(session_date)')
        cursor.execute('CREATE INDEX IF NOT EXISTS idx_sessions_tech ON sessions(technology)')
        cursor.execute('CREATE INDEX IF NOT EXISTS idx_sessions_category ON sessions(category_name)')
        cursor.execute('CREATE INDEX IF NOT EXISTS idx_dropdowns_field ON dropdowns(field_name)')
        cursor.execute('CREATE INDEX IF NOT EXISTS idx_dropdowns_parent ON dropdowns(parent_field, parent_value)')
        
        conn.commit()
        logging.info("Database initialized successfully")
    
    # ==================== SESSION OPERATIONS ====================
    
    def add_session(self, session_data: Dict[str, Any]) -> int:
        """Add a new learning session and return its ID."""
        conn = self._get_connection()
        cursor = conn.cursor()
        
        cursor.execute('''
            INSERT INTO sessions (
                session_date, session_type, category_name, technology,
                work_item, skill_topic, category_source, difficulty,
                status, hours_spent, tags, notes
            ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
        ''', (
            session_data.get('session_date'),
            session_data.get('session_type'),
            session_data.get('category_name'),
            session_data.get('technology'),
            session_data.get('work_item'),
            session_data.get('skill_topic'),
            session_data.get('category_source'),
            session_data.get('difficulty'),
            session_data.get('status'),
            session_data.get('hours_spent'),
            session_data.get('tags'),
            session_data.get('notes')
        ))
        
        conn.commit()
        session_id = cursor.lastrowid
        logging.info(f"Added session ID {session_id}: {session_data.get('technology')} - {session_data.get('skill_topic')}")
        return session_id if session_id else 0
    
    def get_all_sessions(self) -> List[Dict[str, Any]]:
        """Retrieve all learning sessions."""
        conn = self._get_connection()
        cursor = conn.cursor()
        cursor.execute('SELECT * FROM sessions ORDER BY session_date DESC')
        
        rows = cursor.fetchall()
        return [dict(row) for row in rows]
    
    def get_session_by_id(self, session_id: int) -> Optional[Dict[str, Any]]:
        """Get a specific session by ID."""
        conn = self._get_connection()
        cursor = conn.cursor()
        cursor.execute('SELECT * FROM sessions WHERE session_id = ?', (session_id,))
        
        row = cursor.fetchone()
        return dict(row) if row else None
    
    def update_session(self, session_id: int, session_data: Dict[str, Any]) -> bool:
        """Update an existing session."""
        conn = self._get_connection()
        cursor = conn.cursor()
        
        cursor.execute('''
            UPDATE sessions SET
                session_date = ?,
                session_type = ?,
                category_name = ?,
                technology = ?,
                work_item = ?,
                skill_topic = ?,
                category_source = ?,
                difficulty = ?,
                status = ?,
                hours_spent = ?,
                tags = ?,
                notes = ?,
                updated_at = CURRENT_TIMESTAMP
            WHERE session_id = ?
        ''', (
            session_data.get('session_date'),
            session_data.get('session_type'),
            session_data.get('category_name'),
            session_data.get('technology'),
            session_data.get('work_item'),
            session_data.get('skill_topic'),
            session_data.get('category_source'),
            session_data.get('difficulty'),
            session_data.get('status'),
            session_data.get('hours_spent'),
            session_data.get('tags'),
            session_data.get('notes'),
            session_id
        ))
        
        conn.commit()
        logging.info(f"Updated session ID {session_id}")
        return cursor.rowcount > 0
    
    def delete_session(self, session_id: int) -> bool:
        """Delete a session."""
        conn = self._get_connection()
        cursor = conn.cursor()
        cursor.execute('DELETE FROM sessions WHERE session_id = ?', (session_id,))
        conn.commit()
        
        logging.info(f"Deleted session ID {session_id}")
        return cursor.rowcount > 0
    
    # ==================== TECH STACK OPERATIONS ====================
    
    def add_technology(self, name: str, category: str, goal_hours: float = 50, date_added: Optional[str] = None) -> int:
        """Add a new technology to the stack."""
        if date_added is None:
            date_added = datetime.now().strftime('%Y-%m-%d')
        
        conn = self._get_connection()
        cursor = conn.cursor()
        
        try:
            cursor.execute('''
                INSERT INTO tech_stack (name, category, goal_hours, date_added)
                VALUES (?, ?, ?, ?)
            ''', (name, category, goal_hours, date_added))
            
            conn.commit()
            tech_id = cursor.lastrowid
            logging.info(f"Added technology: {name} in category: {category}")
            return tech_id if tech_id else 0
        except sqlite3.IntegrityError:
            logging.warning(f"Technology {name} already exists")
            return -1
    
    def get_all_tech_stack(self) -> List[Dict[str, Any]]:
        """Get all technologies in the stack."""
        conn = self._get_connection()
        cursor = conn.cursor()
        cursor.execute('SELECT * FROM tech_stack ORDER BY category, name')
        
        rows = cursor.fetchall()
        return [dict(row) for row in rows]
    
    def update_technology(self, tech_id: int, name: Optional[str] = None, category: Optional[str] = None, goal_hours: Optional[float] = None) -> bool:
        """Update a technology's details."""
        conn = self._get_connection()
        cursor = conn.cursor()
        
        updates = []
        params = []
        
        if name is not None:
            updates.append('name = ?')
            params.append(name)
        if category is not None:
            updates.append('category = ?')
            params.append(category)
        if goal_hours is not None:
            updates.append('goal_hours = ?')
            params.append(goal_hours)
        
        if not updates:
            return False
        
        params.append(tech_id)
        query = f"UPDATE tech_stack SET {', '.join(updates)} WHERE id = ?"
        
        cursor.execute(query, params)
        conn.commit()
        
        logging.info(f"Updated technology ID {tech_id}")
        return cursor.rowcount > 0
    
    def delete_technology(self, tech_id: int) -> bool:
        """Delete a technology from the stack."""
        conn = self._get_connection()
        cursor = conn.cursor()
        cursor.execute('DELETE FROM tech_stack WHERE id = ?', (tech_id,))
        conn.commit()
        
        logging.info(f"Deleted technology ID {tech_id}")
        return cursor.rowcount > 0
    
    # ==================== DROPDOWN OPERATIONS ====================
    
    def add_dropdown_value(self, field_name: str, field_value: str, parent_field: Optional[str] = None, parent_value: Optional[str] = None) -> bool:
        """Add a new dropdown value with optional parent dependency."""
        conn = self._get_connection()
        cursor = conn.cursor()
        
        try:
            cursor.execute('''
                INSERT INTO dropdowns (field_name, field_value, parent_field, parent_value)
                VALUES (?, ?, ?, ?)
            ''', (field_name, field_value, parent_field, parent_value))
            
            conn.commit()
            logging.info(f"Added dropdown: {field_name} = {field_value}")
            return True
        except sqlite3.IntegrityError:
            logging.debug(f"Dropdown value already exists: {field_name} = {field_value}")
            return False
    
    def get_dropdown_values(self, field_name: str, parent_field: Optional[str] = None, parent_value: Optional[str] = None) -> List[str]:
        """Get dropdown values for a field, optionally filtered by parent."""
        conn = self._get_connection()
        cursor = conn.cursor()
        
        if parent_field and parent_value:
            cursor.execute('''
                SELECT DISTINCT field_value FROM dropdowns
                WHERE field_name = ? AND parent_field = ? AND parent_value = ?
                ORDER BY field_value
            ''', (field_name, parent_field, parent_value))
        else:
            cursor.execute('''
                SELECT DISTINCT field_value FROM dropdowns
                WHERE field_name = ? AND (parent_field IS NULL OR parent_field = '')
                ORDER BY field_value
            ''', (field_name,))
        
        return [row[0] for row in cursor.fetchall()]
    
    def delete_dropdown_value(self, field_name: str, field_value: str) -> bool:
        """Delete a dropdown value."""
        conn = self._get_connection()
        cursor = conn.cursor()
        cursor.execute('DELETE FROM dropdowns WHERE field_name = ? AND field_value = ?', (field_name, field_value))
        conn.commit()
        
        logging.info(f"Deleted dropdown: {field_name} = {field_value}")
        return cursor.rowcount > 0
    
    # ==================== CATEGORY OPERATIONS ====================
    
    def add_category(self, category_name: str, is_custom: bool = True) -> bool:
        """Add a new category."""
        date_added = datetime.now().strftime('%Y-%m-%d')
        conn = self._get_connection()
        cursor = conn.cursor()
        
        try:
            cursor.execute('''
                INSERT INTO categories (category_name, is_custom, date_added)
                VALUES (?, ?, ?)
            ''', (category_name, 1 if is_custom else 0, date_added))
            
            conn.commit()
            logging.info(f"Added category: {category_name}")
            return True
        except sqlite3.IntegrityError:
            logging.warning(f"Category {category_name} already exists")
            return False
    
    def get_all_categories(self) -> List[str]:
        """Get all category names."""
        conn = self._get_connection()
        cursor = conn.cursor()
        cursor.execute('SELECT category_name FROM categories ORDER BY is_custom, category_name')
        
        return [row[0] for row in cursor.fetchall()]
    
    def delete_category(self, category_name: str) -> bool:
        """Delete a category."""
        conn = self._get_connection()
        cursor = conn.cursor()
        cursor.execute('DELETE FROM categories WHERE category_name = ?', (category_name,))
        conn.commit()
        
        logging.info(f"Deleted category: {category_name}")
        return cursor.rowcount > 0
    
    # ==================== ANALYTICS & KPI OPERATIONS ====================
    
    def get_total_hours(self) -> float:
        """Get total hours across all sessions."""
        conn = self._get_connection()
        cursor = conn.cursor()
        cursor.execute('SELECT SUM(hours_spent) FROM sessions')
        result = cursor.fetchone()[0]
        return result if result else 0.0
    
    def get_hours_by_technology(self, technology: str) -> float:
        """Get total hours for a specific technology."""
        conn = self._get_connection()
        cursor = conn.cursor()
        cursor.execute('SELECT SUM(hours_spent) FROM sessions WHERE technology = ?', (technology,))
        result = cursor.fetchone()[0]
        return result if result else 0.0
    
    def get_hours_by_category(self, category: str) -> float:
        """Get total hours for a category."""
        conn = self._get_connection()
        cursor = conn.cursor()
        cursor.execute('SELECT SUM(hours_spent) FROM sessions WHERE category_name = ?', (category,))
        result = cursor.fetchone()[0]
        return result if result else 0.0
    
    def get_session_type_breakdown(self, technology: Optional[str] = None) -> Dict[str, float]:
        """Get studying vs practice hours breakdown."""
        conn = self._get_connection()
        cursor = conn.cursor()
        
        if technology:
            cursor.execute('''
                SELECT session_type, SUM(hours_spent) as total
                FROM sessions
                WHERE technology = ?
                GROUP BY session_type
            ''', (technology,))
        else:
            cursor.execute('''
                SELECT session_type, SUM(hours_spent) as total
                FROM sessions
                GROUP BY session_type
            ''')
        
        breakdown = {}
        for row in cursor.fetchall():
            breakdown[row[0]] = row[1]
        
        return breakdown
    
    def close(self):
        """Close database connection."""
        if self.conn:
            self.conn.close()
            self.conn = None
