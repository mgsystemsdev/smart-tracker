#!/usr/bin/env python3
"""
Bootstrap Blueprint Migration
Loads PLANNING_BLUEPRINT categories and technologies into the database.
This creates a single source of truth by moving hardcoded data into the database.
"""

import sys
from src.database.operations import DatabaseStorage
from src.services.sync_service import TechnologySyncService, CategorySyncService
from src.services.cached_queries import CachedQueryService
from src.core.config import PLANNING_BLUEPRINT
import logging

# Setup logging
logging.basicConfig(level=logging.INFO, format="%(asctime)s | %(levelname)s | %(message)s")

def bootstrap_planning_blueprint():
    """Load PLANNING_BLUEPRINT into database using sync services."""
    
    print("=" * 60)
    print("BOOTSTRAP MIGRATION: Loading Planning Blueprint")
    print("=" * 60)
    
    # Initialize database and services
    db = DatabaseStorage()
    tech_service = TechnologySyncService(db)
    category_service = CategorySyncService(db)
    
    categories_added = 0
    technologies_added = 0
    categories_skipped = 0
    technologies_skipped = 0
    
    # Process each category in the blueprint
    for category_name, category_data in PLANNING_BLUEPRINT.items():
        print(f"\n📂 Processing category: {category_name}")
        
        # Add category as built-in (is_custom=0)
        result = category_service.add_category(category_name, is_custom=False)
        
        if result['success']:
            categories_added += 1
            print(f"   ✅ Added category: {category_name}")
        else:
            categories_skipped += 1
            print(f"   ⏭️  Skipped (already exists): {category_name}")
        
        # Process subsections and tools
        for subsection in category_data.get('subsections', []):
            subsection_name = subsection.get('name', '')
            
            for tool in subsection.get('tools', []):
                tech_name = tool['name']
                # Use average of min and max hours as goal_hours
                goal_hours = (tool['min_hours'] + tool['max_hours']) / 2
                
                # Add technology using sync service
                from datetime import date
                tech_result = tech_service.add_technology(
                    name=tech_name,
                    category=category_name,
                    goal_hours=goal_hours,
                    date_added=str(date.today())
                )
                
                if tech_result['success']:
                    technologies_added += 1
                    print(f"      ✅ Added tech: {tech_name} ({goal_hours:.0f}h goal)")
                else:
                    technologies_skipped += 1
                    print(f"      ⏭️  Skipped: {tech_name}")
    
    # Invalidate cache to refresh all queries
    CachedQueryService.invalidate_cache()
    
    # Summary
    print("\n" + "=" * 60)
    print("BOOTSTRAP COMPLETE")
    print("=" * 60)
    print(f"✅ Categories added: {categories_added}")
    print(f"⏭️  Categories skipped: {categories_skipped}")
    print(f"✅ Technologies added: {technologies_added}")
    print(f"⏭️  Technologies skipped: {technologies_skipped}")
    print("\n🎯 All planning blueprint data is now in the database!")
    print("   Categories and technologies will appear in all dropdowns.")
    
    return {
        'categories_added': categories_added,
        'technologies_added': technologies_added,
        'categories_skipped': categories_skipped,
        'technologies_skipped': technologies_skipped
    }

if __name__ == "__main__":
    try:
        bootstrap_planning_blueprint()
        sys.exit(0)
    except Exception as e:
        logging.error(f"Bootstrap migration failed: {e}")
        print(f"\n❌ ERROR: {e}")
        sys.exit(1)
