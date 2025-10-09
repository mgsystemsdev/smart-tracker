"""
Repair Script: Fix dropdown parent-child relationships
This script syncs technologies from tech_stack into dropdowns table WITH proper parent relationships.
"""

import sqlite3
import logging

logging.basicConfig(level=logging.INFO, format='%(levelname)s: %(message)s')

def repair_dropdown_relationships():
    """Sync technologies from tech_stack to dropdowns table with proper parent relationships."""
    
    conn = sqlite3.connect('data/smart_tracker.db')
    cursor = conn.cursor()
    
    print("\n" + "="*60)
    print("DROPDOWN RELATIONSHIP REPAIR SCRIPT")
    print("="*60)
    
    # Step 1: Check current state
    print("\n📊 CHECKING CURRENT STATE...")
    
    cursor.execute("SELECT COUNT(*) FROM dropdowns WHERE field_name = 'technology'")
    tech_count = cursor.fetchone()[0]
    print(f"   Technologies in dropdowns table: {tech_count}")
    
    cursor.execute("SELECT COUNT(*) FROM dropdowns WHERE field_name = 'technology' AND parent_field = 'category_name'")
    tech_with_parent = cursor.fetchone()[0]
    print(f"   Technologies WITH parent category link: {tech_with_parent}")
    print(f"   Technologies MISSING parent link: {tech_count - tech_with_parent}")
    
    if tech_count == tech_with_parent:
        print("\n✅ All technologies already have proper parent relationships!")
        conn.close()
        return
    
    # Step 2: Get all technologies from tech_stack
    cursor.execute("SELECT name, category FROM tech_stack")
    tech_stack_data = cursor.fetchall()
    print(f"\n📦 Found {len(tech_stack_data)} technologies in tech_stack table")
    
    # Step 3: Clear old technology entries from dropdowns
    print("\n🗑️  CLEARING old technology entries from dropdowns...")
    cursor.execute("DELETE FROM dropdowns WHERE field_name = 'technology'")
    deleted_count = cursor.rowcount
    print(f"   Deleted {deleted_count} old entries")
    
    # Step 4: Re-insert technologies WITH proper parent relationships
    print("\n➕ INSERTING technologies with parent relationships...")
    
    inserted = 0
    for tech_name, category in tech_stack_data:
        try:
            cursor.execute('''
                INSERT INTO dropdowns (field_name, field_value, parent_field, parent_value)
                VALUES (?, ?, ?, ?)
            ''', ('technology', tech_name, 'category_name', category))
            inserted += 1
            print(f"   ✓ {tech_name} → {category}")
        except sqlite3.IntegrityError:
            print(f"   ⚠ Skipped duplicate: {tech_name}")
    
    conn.commit()
    print(f"\n✅ Successfully inserted {inserted} technologies with parent relationships")
    
    # Step 5: Verify the fix
    print("\n🔍 VERIFYING REPAIR...")
    cursor.execute("""
        SELECT field_value, parent_value 
        FROM dropdowns 
        WHERE field_name = 'technology' 
        ORDER BY parent_value, field_value
        LIMIT 10
    """)
    
    samples = cursor.fetchall()
    print("\n   Sample entries (first 10):")
    for tech, cat in samples:
        print(f"      {tech} → {cat}")
    
    cursor.execute("SELECT COUNT(*) FROM dropdowns WHERE field_name = 'technology' AND parent_field = 'category_name'")
    final_count = cursor.fetchone()[0]
    print(f"\n   Total technologies with parent links: {final_count}")
    
    conn.close()
    
    print("\n" + "="*60)
    print("✅ REPAIR COMPLETE!")
    print("="*60)
    print("\n🎯 Next steps:")
    print("   1. Restart the Streamlit app")
    print("   2. Go to Log Session page")
    print("   3. Select a Category - Technology dropdown should now filter correctly!")
    print()

if __name__ == "__main__":
    repair_dropdown_relationships()
