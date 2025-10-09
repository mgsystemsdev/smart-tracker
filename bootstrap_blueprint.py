#!/usr/bin/env python3
"""
Bootstrap Blueprint Migration
Loads PLANNING_BLUEPRINT categories and technologies into the database.
This creates a single source of truth by moving hardcoded data into the database.
"""

import sys
from database.operations import DatabaseStorage
from services.sync_service import TechnologySyncService, CategorySyncService
from services.cached_queries import CachedQueryService
import logging

# Setup logging
logging.basicConfig(level=logging.INFO, format="%(asctime)s | %(levelname)s | %(message)s")

# Import the planning blueprint from app.py
PLANNING_BLUEPRINT = {
    "🌐 Core Full-Stack Development": {
        "subsections": [
            {
                "name": "🖥️ Front-End",
                "tools": [
                    {"name": "HTML", "min_hours": 20, "max_hours": 30},
                    {"name": "CSS", "min_hours": 20, "max_hours": 30},
                    {"name": "JavaScript (ES6+)", "min_hours": 60, "max_hours": 80},
                    {"name": "React", "min_hours": 70, "max_hours": 90},
                    {"name": "Tailwind CSS", "min_hours": 15, "max_hours": 25}
                ]
            },
            {
                "name": "⚙️ Back-End",
                "tools": [
                    {"name": "Django", "min_hours": 80, "max_hours": 100},
                    {"name": "PostgreSQL", "min_hours": 40, "max_hours": 50}
                ]
            },
            {
                "name": "🔗 Lightweight APIs / Model Serving",
                "tools": [
                    {"name": "FastAPI", "min_hours": 40, "max_hours": 60}
                ]
            },
            {
                "name": "🌉 Integration (optional)",
                "tools": [
                    {"name": "Next.js", "min_hours": 40, "max_hours": 60}
                ]
            },
            {
                "name": "☁️ Deployment",
                "tools": [
                    {"name": "AWS (S3 + EC2 + Lambda)", "min_hours": 80, "max_hours": 100},
                    {"name": "GitHub Actions", "min_hours": 25, "max_hours": 40}
                ]
            }
        ]
    },
    "📊 Data Science & Machine Learning": {
        "subsections": [
            {
                "name": "🧮 Core Libraries",
                "tools": [
                    {"name": "Pandas", "min_hours": 80, "max_hours": 100},
                    {"name": "NumPy", "min_hours": 25, "max_hours": 35},
                    {"name": "SciPy", "min_hours": 15, "max_hours": 20}
                ]
            },
            {
                "name": "📈 Visualization",
                "tools": [
                    {"name": "Matplotlib", "min_hours": 25, "max_hours": 35},
                    {"name": "Seaborn", "min_hours": 20, "max_hours": 25},
                    {"name": "Streamlit", "min_hours": 50, "max_hours": 70}
                ]
            },
            {
                "name": "🤖 Machine Learning",
                "tools": [
                    {"name": "scikit-learn", "min_hours": 60, "max_hours": 80},
                    {"name": "PyTorch", "min_hours": 60, "max_hours": 80},
                    {"name": "TensorFlow", "min_hours": 60, "max_hours": 80},
                    {"name": "CUDA (optional)", "min_hours": 20, "max_hours": 30}
                ]
            },
            {
                "name": "🔄 Pipelines",
                "tools": [
                    {"name": "Apache Airflow", "min_hours": 50, "max_hours": 70}
                ]
            },
            {
                "name": "🗄️ Databases (for data work)",
                "tools": [
                    {"name": "PostgreSQL", "min_hours": 40, "max_hours": 60}
                ]
            }
        ]
    },
    "📑 Excel Automation & Data Handling": {
        "subsections": [
            {
                "name": "",
                "tools": [
                    {"name": "OpenPyXL", "min_hours": 20, "max_hours": 30},
                    {"name": "xlwings", "min_hours": 25, "max_hours": 40}
                ]
            }
        ]
    },
    "⚙️ Core Automation (Support Layer)": {
        "subsections": [
            {
                "name": "",
                "tools": [
                    {"name": "Python (automation scripting)", "min_hours": 50, "max_hours": 70},
                    {"name": "Cron Jobs + Airflow", "min_hours": 20, "max_hours": 30},
                    {"name": "Selenium / Playwright", "min_hours": 40, "max_hours": 60},
                    {"name": "Requests + aiohttp", "min_hours": 25, "max_hours": 40},
                    {"name": "GitHub Actions (CI/CD automation)", "min_hours": 20, "max_hours": 30}
                ]
            }
        ]
    },
    "🔒 Reliability & Security": {
        "subsections": [
            {
                "name": "",
                "tools": [
                    {"name": "pytest (testing)", "min_hours": 30, "max_hours": 50},
                    {"name": "OAuth 2.0 + Web App Security", "min_hours": 40, "max_hours": 60}
                ]
            }
        ]
    },
    "🧰 Supporting Skills": {
        "subsections": [
            {
                "name": "",
                "tools": [
                    {"name": "Git (version control)", "min_hours": 25, "max_hours": 40},
                    {"name": "REST + GraphQL APIs", "min_hours": 40, "max_hours": 60},
                    {"name": "Jira + Agile Collaboration", "min_hours": 20, "max_hours": 30}
                ]
            }
        ]
    },
    "🧠 AI & NLP Engineering": {
        "subsections": [
            {
                "name": "",
                "tools": [
                    {"name": "OpenAI API + LangChain", "min_hours": 60, "max_hours": 80},
                    {"name": "HuggingFace Transformers", "min_hours": 50, "max_hours": 70},
                    {"name": "Pinecone / FAISS (vector DBs)", "min_hours": 30, "max_hours": 50}
                ]
            }
        ]
    }
}

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
