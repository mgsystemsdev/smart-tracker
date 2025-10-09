"""
Cached Query Service - Eliminates N+1 queries with batch operations and caching.
Uses Streamlit's @st.cache_data decorator for performance optimization.
"""

import streamlit as st
from typing import Dict, List, Any
from database.operations import DatabaseStorage
import logging

class CachedQueryService:
    """Provides cached and batched database queries."""
    
    def __init__(self, db: DatabaseStorage):
        self.db = db
    
    @staticmethod
    @st.cache_data(ttl=60, show_spinner=False)
    def get_tech_stack_with_metrics(_db: DatabaseStorage) -> List[Dict[str, Any]]:
        """
        Get tech stack with logged hours in ONE batch query.
        Eliminates N+1 query pattern.
        """
        conn = _db._get_connection()
        cursor = conn.cursor()
        
        # Single JOIN query instead of N individual queries
        cursor.execute('''
            SELECT 
                ts.id,
                ts.name,
                ts.category,
                ts.goal_hours,
                ts.date_added,
                COALESCE(SUM(s.hours_spent), 0) as logged_hours,
                COUNT(s.session_id) as session_count
            FROM tech_stack ts
            LEFT JOIN sessions s ON ts.name = s.technology
            GROUP BY ts.id, ts.name, ts.category, ts.goal_hours, ts.date_added
            ORDER BY ts.category, ts.name
        ''')
        
        results = []
        for row in cursor.fetchall():
            results.append({
                'id': row[0],
                'name': row[1],
                'category': row[2],
                'goal_hours': row[3],
                'date_added': row[4],
                'logged_hours': row[5],
                'session_count': row[6],
                'progress_pct': (row[5] / row[3] * 100) if row[3] > 0 else 0
            })
        
        logging.info(f"CachedQueryService: Fetched {len(results)} tech stack entries with metrics (cached)")
        return results
    
    @staticmethod
    @st.cache_data(ttl=60, show_spinner=False)
    def get_dropdown_values_cached(_db: DatabaseStorage, field_name: str, parent_field: str = None, 
                                   parent_value: str = None, show_all: bool = False) -> List[str]:
        """Cached dropdown values query."""
        return _db.get_dropdown_values(field_name, parent_field, parent_value, show_all)
    
    @staticmethod
    @st.cache_data(ttl=60, show_spinner=False)
    def get_all_dropdown_data(_db: DatabaseStorage) -> Dict[str, List[str]]:
        """Get all dropdown data at once (cached)."""
        conn = _db._get_connection()
        cursor = conn.cursor()
        
        cursor.execute('''
            SELECT field_name, field_value 
            FROM dropdowns 
            ORDER BY field_name, field_value
        ''')
        
        all_data = {}
        for row in cursor.fetchall():
            field_name = row[0]
            field_value = row[1]
            
            if field_name not in all_data:
                all_data[field_name] = []
            
            if field_value not in all_data[field_name]:
                all_data[field_name].append(field_value)
        
        return all_data
    
    @staticmethod
    @st.cache_data(ttl=30, show_spinner=False)
    def get_dashboard_metrics(_db: DatabaseStorage) -> Dict[str, Any]:
        """Get all dashboard metrics in one batch query."""
        conn = _db._get_connection()
        cursor = conn.cursor()
        
        # Get aggregated stats
        cursor.execute('''
            SELECT 
                COUNT(DISTINCT session_id) as total_sessions,
                SUM(hours_spent) as total_hours,
                COUNT(DISTINCT technology) as tech_count,
                COUNT(DISTINCT category_name) as category_count
            FROM sessions
        ''')
        
        row = cursor.fetchone()
        
        return {
            'total_sessions': row[0] or 0,
            'total_hours': row[1] or 0.0,
            'tech_count': row[2] or 0,
            'category_count': row[3] or 0
        }
    
    @staticmethod
    def invalidate_cache():
        """Clear all cached data (call after database writes)."""
        st.cache_data.clear()
        logging.info("CachedQueryService: Cache invalidated")
    
    @staticmethod
    @st.cache_data(ttl=60, show_spinner=False)
    def get_sessions_with_details(_db: DatabaseStorage, limit: int = 100, offset: int = 0) -> List[Dict[str, Any]]:
        """Get sessions with pagination (cached)."""
        conn = _db._get_connection()
        cursor = conn.cursor()
        
        cursor.execute('''
            SELECT * FROM sessions 
            ORDER BY session_date DESC, created_at DESC
            LIMIT ? OFFSET ?
        ''', (limit, offset))
        
        rows = cursor.fetchall()
        return [dict(row) for row in rows]
    
    @staticmethod
    @st.cache_data(ttl=60, show_spinner=False)
    def get_technology_session_counts(_db: DatabaseStorage) -> Dict[str, int]:
        """Get session counts by technology (for delete safety checks)."""
        conn = _db._get_connection()
        cursor = conn.cursor()
        
        cursor.execute('''
            SELECT technology, COUNT(*) as count
            FROM sessions
            GROUP BY technology
        ''')
        
        return {row[0]: row[1] for row in cursor.fetchall()}
    
    @staticmethod
    @st.cache_data(ttl=60, show_spinner=False)
    def get_category_usage_stats(_db: DatabaseStorage) -> Dict[str, Dict[str, int]]:
        """Get usage statistics for categories."""
        conn = _db._get_connection()
        cursor = conn.cursor()
        
        # Get tech count and session count per category
        cursor.execute('''
            SELECT 
                category,
                COUNT(*) as tech_count
            FROM tech_stack
            GROUP BY category
        ''')
        
        tech_counts = {row[0]: row[1] for row in cursor.fetchall()}
        
        cursor.execute('''
            SELECT 
                category_name,
                COUNT(*) as session_count
            FROM sessions
            GROUP BY category_name
        ''')
        
        session_counts = {row[0]: row[1] for row in cursor.fetchall()}
        
        # Combine results
        all_categories = set(tech_counts.keys()) | set(session_counts.keys())
        
        return {
            cat: {
                'tech_count': tech_counts.get(cat, 0),
                'session_count': session_counts.get(cat, 0)
            }
            for cat in all_categories
        }
