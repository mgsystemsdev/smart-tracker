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
    def get_dropdown_values_cached(_db: DatabaseStorage, field_name: str, parent_field: str = "", 
                                   parent_value: str = "", show_all: bool = False) -> List[str]:
        """Cached dropdown values query."""
        p_field = parent_field if parent_field else None
        p_value = parent_value if parent_value else None
        return _db.get_dropdown_values(field_name, p_field, p_value, show_all)
    
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
            LIMIT %s OFFSET %s
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
    
    @staticmethod
    @st.cache_data(ttl=60, show_spinner=False)
    def get_category_hours_aggregated(_db: DatabaseStorage) -> Dict[str, float]:
        """Get hours by category using true aggregation (no row limit)."""
        conn = _db._get_connection()
        cursor = conn.cursor()
        
        cursor.execute('''
            SELECT 
                category_name,
                SUM(hours_spent) as total_hours
            FROM sessions
            GROUP BY category_name
        ''')
        
        return {row[0]: row[1] for row in cursor.fetchall()}
    
    @staticmethod
    @st.cache_data(ttl=60, show_spinner=False)
    def get_category_analytics(_db: DatabaseStorage) -> List[Dict[str, Any]]:
        """Get category analytics with technology breakdown."""
        conn = _db._get_connection()
        cursor = conn.cursor()
        
        # Get category totals with technology breakdown
        cursor.execute('''
            SELECT 
                s.category_name,
                s.technology,
                SUM(s.hours_spent) as hours,
                COUNT(s.session_id) as sessions
            FROM sessions s
            WHERE s.category_name != ''
            GROUP BY s.category_name, s.technology
            ORDER BY s.category_name, hours DESC
        ''')
        
        # Organize by category
        category_data = {}
        for row in cursor.fetchall():
            cat_name = row[0]
            tech_name = row[1]
            hours = row[2]
            sessions = row[3]
            
            if cat_name not in category_data:
                category_data[cat_name] = {
                    'category': cat_name,
                    'total_hours': 0,
                    'total_sessions': 0,
                    'technologies': []
                }
            
            category_data[cat_name]['total_hours'] += hours
            category_data[cat_name]['total_sessions'] += sessions
            category_data[cat_name]['technologies'].append({
                'name': tech_name,
                'hours': hours,
                'sessions': sessions
            })
        
        return list(category_data.values())
    
    @staticmethod
    @st.cache_data(ttl=60, show_spinner=False)
    def get_technology_analytics(_db: DatabaseStorage) -> List[Dict[str, Any]]:
        """Get technology analytics with work item breakdown."""
        conn = _db._get_connection()
        cursor = conn.cursor()
        
        # Get technology totals with work item breakdown
        cursor.execute('''
            SELECT 
                s.technology,
                s.category_name,
                s.work_item,
                SUM(s.hours_spent) as hours,
                COUNT(s.session_id) as sessions
            FROM sessions s
            WHERE s.technology != ''
            GROUP BY s.technology, s.category_name, s.work_item
            ORDER BY s.technology, hours DESC
        ''')
        
        # Organize by technology
        tech_data = {}
        for row in cursor.fetchall():
            tech_name = row[0]
            cat_name = row[1]
            work_item = row[2] if row[2] else 'General Practice'
            hours = row[3]
            sessions = row[4]
            
            if tech_name not in tech_data:
                tech_data[tech_name] = {
                    'technology': tech_name,
                    'category': cat_name,
                    'total_hours': 0,
                    'total_sessions': 0,
                    'work_items': []
                }
            
            tech_data[tech_name]['total_hours'] += hours
            tech_data[tech_name]['total_sessions'] += sessions
            tech_data[tech_name]['work_items'].append({
                'name': work_item,
                'hours': hours,
                'sessions': sessions
            })
        
        return list(tech_data.values())
    
    @staticmethod
    @st.cache_data(ttl=60, show_spinner=False)
    def get_work_item_analytics(_db: DatabaseStorage) -> List[Dict[str, Any]]:
        """Get work item analytics with skill breakdown."""
        conn = _db._get_connection()
        cursor = conn.cursor()
        
        # Get work item totals with skill breakdown
        cursor.execute('''
            SELECT 
                s.work_item,
                s.technology,
                s.skill_topic,
                s.session_type,
                SUM(s.hours_spent) as hours,
                COUNT(s.session_id) as sessions
            FROM sessions s
            WHERE s.work_item != '' AND s.work_item IS NOT NULL
            GROUP BY s.work_item, s.technology, s.skill_topic, s.session_type
            ORDER BY s.work_item, hours DESC
        ''')
        
        # Organize by work item
        work_item_data = {}
        for row in cursor.fetchall():
            work_item = row[0]
            tech_name = row[1]
            skill = row[2] if row[2] else 'General'
            session_type = row[3]
            hours = row[4]
            sessions = row[5]
            
            if work_item not in work_item_data:
                work_item_data[work_item] = {
                    'work_item': work_item,
                    'technology': tech_name,
                    'total_hours': 0,
                    'total_sessions': 0,
                    'studying_hours': 0,
                    'practice_hours': 0,
                    'skills': []
                }
            
            work_item_data[work_item]['total_hours'] += hours
            work_item_data[work_item]['total_sessions'] += sessions
            
            if session_type == 'Studying':
                work_item_data[work_item]['studying_hours'] += hours
            elif session_type == 'Practice':
                work_item_data[work_item]['practice_hours'] += hours
            
            # Add skill if not already there
            existing_skill = next((s for s in work_item_data[work_item]['skills'] if s['name'] == skill), None)
            if existing_skill:
                existing_skill['hours'] += hours
                existing_skill['sessions'] += sessions
            else:
                work_item_data[work_item]['skills'].append({
                    'name': skill,
                    'hours': hours,
                    'sessions': sessions
                })
        
        return list(work_item_data.values())
