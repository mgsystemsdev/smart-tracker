# Smart Tracker

## Overview

Smart Tracker is a minimal personal learning tracker featuring a simplified workflow: just log your work and see your progress automatically. Built with a dual-interface architecture, it provides both a modern Streamlit web interface and a Typer CLI. The tracker eliminates manual progress tracking - progress is automatically calculated from hours logged. Features MG System Dev branding with golden yellow accents and a dark tech theme.

## User Preferences

Preferred communication style: Simple, everyday language.

## Recent Changes

### October 9, 2025 - Architecture Simplification
**Beginner-Friendly Restructure**: Complete reorganization from nested smarttracker/app/ to flat, intuitive structure
- **Page Extraction**: Moved all page functions from monolithic app.py (1365 lines) to dedicated modules in pages/ directory
- **Clean Routing**: app.py reduced to 374 lines, now serves as lightweight router with page imports
- **Legacy Cleanup**: Removed smarttracker/ folder, JSON files, backup folders, empty tests/ directory
- **Documentation Update**: Updated replit.md to reflect new beginner-friendly architecture
- **Verified**: All 7 pages (Home, Sessions, Log Session, Tech Stack, Planning, Calculator, Dropdown Manager) working correctly

### October 8, 2025 - Smart Tracker v2.0 Platform Redesign
Major architectural upgrade transitioning from JSON-based storage to SQLite database with enhanced hierarchical data model and comprehensive KPI dashboard system.

#### Database Migration & Infrastructure
- **SQLite Database**: Migrated from JSON files to SQLite (`data/smart_tracker.db`) with 4-table schema (sessions, tech_stack, categories, dropdowns)
- **Threading Fix**: Implemented `check_same_thread=False` for Streamlit multi-threaded compatibility
- **Data Migration**: Successfully migrated existing data (5 sessions, 3 technologies, 13.2 hours) from JSON to SQLite
- **Auto Backup**: Migration creates timestamped backups before conversion for data safety

#### Enhanced Session Model (13 Fields)
- **Hierarchical Structure**: Category Name → Technology → Work Item → Skill/Topic cascade system
- **New Fields**: session_id, session_date, category_name, technology, work_item, skill_topic, notes, tags, session_type, difficulty, status, hours_logged, date_added
- **Session Types**: Integrated "Studying" and "Practice" tracking for 20/80 rule monitoring
- **Smart Validation**: Hours (0-12), no future dates, required technology field

#### New Page Architecture
- **Home KPI Dashboard** (`home_kpi_dashboard.py`): Real-time metrics with Total Sessions, Total Hours, Technologies count, Overall Progress percentage
- **Tech Stack CRUD** (`tech_stack_crud_page.py`): Dedicated technology management interface (removed from Home)
- **Calculator** (`calculator_page.py`): Workload estimation with flexible unit conversion (hours/days/weeks/months) and scenario planning
- **Dropdown Manager** (`dropdown_manager_page.py`): Centralized dropdown data management for cascading selectors with type-to-add functionality

#### Cascading Dropdown System
- **4-Level Hierarchy**: Category Name (root) → Technology → Work Item → Skill/Topic (leaf)
- **Auto-Population**: Child dropdowns populate based on parent selection
- **Type-to-Add**: Create new dropdown options on-the-fly during session entry
- **Centralized Management**: Single source of truth in dropdown_manager page

#### UI/UX Improvements
- **Professional Branding**: "SYSTEM DEV | Real-Time Operations Dashboard" subtitle on header
- **Default Collapsed**: All sections start collapsed except Grand Total for cleaner interface
- **Top-Load Behavior**: Critical metrics and controls always visible at page top
- **Cross-Page Sync**: Database ensures data consistency across all pages automatically

#### Navigation Structure
New streamlined navigation with dedicated pages:
1. 🏠 Home Dashboard (KPI metrics only)
2. 📚 Sessions (view/manage)
3. 📝 Log Session (create new)
4. 🎯 Tech Stack CRUD (manage technologies)
5. 📋 Planning (roadmap view)
6. 🧮 Calculator (workload estimation)
7. ⚙️ Dropdown Manager (data management)

## System Architecture

### Beginner-Friendly Folder Structure
The application uses a simple, flat structure that's easy to understand:

```
smart-tracker/
├── app.py                    # Main Streamlit application
├── main.py                   # Entry point (workflow runner)
├── database/
│   └── operations.py         # All database operations
├── pages/
│   ├── home_dashboard.py     # KPI dashboard
│   ├── sessions.py           # View/edit sessions
│   ├── log_session.py        # Create new session
│   ├── tech_stack.py         # Tech stack management
│   ├── planning.py           # Planning & roadmap
│   ├── calculator.py         # Workload calculator
│   └── dropdown_manager.py   # Dropdown data manager
├── utils/
│   └── cascading_dropdowns.py # Hierarchical dropdown logic
├── data/                     # SQLite database
└── logs/                     # Application logs
```

### Interface Architecture
**Single Streamlit Interface**: The application is a web-based Streamlit app with:
- Wide layout with expandable sidebar
- Port 5000 binding with external accessibility (0.0.0.0)
- Multi-page navigation system
- MG System Dev branding with golden yellow accents

### Design Patterns
**Modular Page Design**: Each page is a separate Python file with a single function that renders that page. This makes it easy to:
- Find and edit specific features
- Understand what each page does
- Add new pages without touching existing code

**Database-First Approach**: All data operations go through the `DatabaseStorage` class in `database/operations.py`. No JSON files, no legacy storage - just clean SQLite operations.

## External Dependencies

### Core Frameworks
- **Streamlit**: Web application framework for the visual interface
- **Typer**: Modern CLI framework for command-line interface

### Runtime Environment
- **Python 3.11+**: Minimum required Python version
- **pip**: Package management for dependency installation

### Development Tools
- **pytest**: Testing framework (structure prepared in `tests/` directory)

### Data Persistence & Management
- **SQLite Database**: Primary storage in `data/smart_tracker.db` with 4-table relational schema
- **Database Tables**: 
  - `sessions`: Learning session records with 13 fields
  - `tech_stack`: Technology inventory with goals and progress tracking
  - `categories`: Category definitions with emojis and metadata
  - `dropdowns`: Hierarchical dropdown options for cascading selectors
- **Threading Support**: Configured with `check_same_thread=False` for Streamlit multi-threading
- **Automatic Backup**: Migration utility creates timestamped JSON backups before database conversion
- **Data Migration**: Built-in utility (`migrate_to_db.py`) converts legacy JSON data to SQLite

### CRUD Operations (Database-Driven)
- **Create**: Add sessions via Log Session page with cascading dropdowns and auto-save to database
- **Read**: View sessions in Sessions page with real-time database queries
- **Update**: Edit sessions/technologies through dedicated CRUD pages with instant database sync
- **Delete**: Remove records with database cascade handling for referential integrity
- **Export**: CSV export functionality for external analysis and reporting