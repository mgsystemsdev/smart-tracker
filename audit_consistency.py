#!/usr/bin/env python3
"""
Data Consistency Audit Script
Compares categories and technologies across all tables to find inconsistencies.
"""

from database.operations import DatabaseStorage
import logging

# Setup logging
logging.basicConfig(level=logging.INFO, format="%(asctime)s | %(levelname)s | %(message)s")

def audit_data_consistency():
    """Audit data consistency across all tables."""
    
    print("=" * 70)
    print(" DATA CONSISTENCY AUDIT")
    print("=" * 70)
    
    db = DatabaseStorage()
    conn = db._get_connection()
    cursor = conn.cursor()
    
    issues = []
    
    # ========== CATEGORIES AUDIT ==========
    print("\n📂 AUDITING CATEGORIES...")
    print("-" * 70)
    
    # Get categories from each source
    cursor.execute("SELECT DISTINCT category_name FROM categories ORDER BY category_name")
    categories_table = set(row[0] for row in cursor.fetchall())
    
    cursor.execute("SELECT DISTINCT field_value FROM dropdowns WHERE field_name='category_name' ORDER BY field_value")
    categories_dropdowns = set(row[0] for row in cursor.fetchall())
    
    cursor.execute("SELECT DISTINCT category FROM tech_stack ORDER BY category")
    categories_tech_stack = set(row[0] for row in cursor.fetchall())
    
    cursor.execute("SELECT DISTINCT category_name FROM sessions ORDER BY category_name")
    categories_sessions = set(row[0] for row in cursor.fetchall())
    
    print(f"  Categories in 'categories' table: {len(categories_table)}")
    print(f"  Categories in 'dropdowns' table:  {len(categories_dropdowns)}")
    print(f"  Categories in 'tech_stack' table: {len(categories_tech_stack)}")
    print(f"  Categories in 'sessions' table:   {len(categories_sessions)}")
    
    # Find inconsistencies
    missing_in_dropdowns = categories_table - categories_dropdowns
    missing_in_categories = categories_dropdowns - categories_table
    
    if missing_in_dropdowns:
        issues.append(f"⚠️  Categories in 'categories' but NOT in 'dropdowns': {missing_in_dropdowns}")
        print(f"\n  ⚠️  Missing in dropdowns: {missing_in_dropdowns}")
    
    if missing_in_categories:
        issues.append(f"⚠️  Categories in 'dropdowns' but NOT in 'categories': {missing_in_categories}")
        print(f"  ⚠️  Missing in categories table: {missing_in_categories}")
    
    # Check tech_stack categories exist in categories table
    orphan_tech_categories = categories_tech_stack - categories_table
    if orphan_tech_categories:
        issues.append(f"⚠️  Categories in 'tech_stack' but NOT in 'categories': {orphan_tech_categories}")
        print(f"  ⚠️  Orphan tech stack categories: {orphan_tech_categories}")
    
    # Check sessions categories exist in categories table
    orphan_session_categories = categories_sessions - categories_table
    if orphan_session_categories:
        issues.append(f"⚠️  Categories in 'sessions' but NOT in 'categories': {orphan_session_categories}")
        print(f"  ⚠️  Orphan session categories: {orphan_session_categories}")
    
    if not missing_in_dropdowns and not missing_in_categories and not orphan_tech_categories and not orphan_session_categories:
        print("  ✅ Categories are consistent across all tables!")
    
    # ========== TECHNOLOGIES AUDIT ==========
    print("\n\n🔧 AUDITING TECHNOLOGIES...")
    print("-" * 70)
    
    # Get technologies from each source
    cursor.execute("SELECT DISTINCT name FROM tech_stack ORDER BY name")
    tech_stack_techs = set(row[0] for row in cursor.fetchall())
    
    cursor.execute("SELECT DISTINCT field_value FROM dropdowns WHERE field_name='technology' ORDER BY field_value")
    tech_dropdowns = set(row[0] for row in cursor.fetchall())
    
    cursor.execute("SELECT DISTINCT technology FROM sessions ORDER BY technology")
    tech_sessions = set(row[0] for row in cursor.fetchall())
    
    print(f"  Technologies in 'tech_stack' table: {len(tech_stack_techs)}")
    print(f"  Technologies in 'dropdowns' table:  {len(tech_dropdowns)}")
    print(f"  Technologies in 'sessions' table:   {len(tech_sessions)}")
    
    # Find inconsistencies
    missing_in_tech_dropdowns = tech_stack_techs - tech_dropdowns
    missing_in_tech_stack = tech_dropdowns - tech_stack_techs
    
    if missing_in_tech_dropdowns:
        issues.append(f"⚠️  Technologies in 'tech_stack' but NOT in 'dropdowns': {missing_in_tech_dropdowns}")
        print(f"\n  ⚠️  Missing in dropdowns: {missing_in_tech_dropdowns}")
    
    if missing_in_tech_stack:
        issues.append(f"⚠️  Technologies in 'dropdowns' but NOT in 'tech_stack': {missing_in_tech_stack}")
        print(f"  ⚠️  Missing in tech_stack: {missing_in_tech_stack}")
    
    # Check sessions technologies exist in tech_stack
    orphan_session_techs = tech_sessions - tech_stack_techs
    if orphan_session_techs:
        issues.append(f"⚠️  Technologies in 'sessions' but NOT in 'tech_stack': {orphan_session_techs}")
        print(f"  ⚠️  Orphan session technologies: {orphan_session_techs}")
    
    if not missing_in_tech_dropdowns and not missing_in_tech_stack and not orphan_session_techs:
        print("  ✅ Technologies are consistent across all tables!")
    
    # ========== SUMMARY ==========
    print("\n\n" + "=" * 70)
    print(" AUDIT SUMMARY")
    print("=" * 70)
    
    if issues:
        print(f"\n❌ Found {len(issues)} inconsistencies:")
        for i, issue in enumerate(issues, 1):
            print(f"{i}. {issue}")
        print("\n💡 Recommendation: Use sync services (TechnologySyncService, CategorySyncService) to fix these issues.")
    else:
        print("\n✅ ALL DATA IS CONSISTENT!")
        print("   Categories and technologies are properly synced across all tables.")
    
    print("\n" + "=" * 70)
    
    return len(issues)

if __name__ == "__main__":
    import sys
    issue_count = audit_data_consistency()
    sys.exit(0 if issue_count == 0 else 1)
