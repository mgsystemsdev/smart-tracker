# Smart Tracker

## Overview
Smart Tracker is a personal learning tracker with a dual-interface architecture, offering both a Streamlit web interface and a Typer CLI. Its core purpose is to simplify progress tracking by automatically calculating progress from logged hours. The project aims to provide a robust, user-friendly system for logging and visualizing learning efforts, incorporating a hierarchical data model and a comprehensive KPI dashboard. It features MG System Dev branding with golden yellow accents and a dark tech theme.

**Current State:** Blank canvas - database is initialized but contains no pre-loaded categories or technologies. Users start with an empty system and add their own custom data through the Dropdown Manager.

## Recent Changes
### October 10, 2025 - Repository Reorganization & Cleanup ✅
- **Complete src/ structure implementation**: Organized all source code into professional folder structure
  - `src/core/` - Core application logic and configuration (app.py, config.py)
  - `src/database/` - Database operations layer (operations.py)
  - `src/pages/` - Streamlit page modules (8 pages)
  - `src/services/` - Business logic services (sync_service.py, cached_queries.py)
  - `src/utils/` - Utility functions (unified dropdowns.py)
- **Dropdown Manager Consolidation**: Merged cascading_dropdowns.py and cascading_dropdowns_v2.py into single unified dropdowns.py
  - Supports both hierarchical management mode (auto-save) and simplified session entry mode (deferred save)
  - Eliminated code duplication across 700+ lines
- **Configuration Centralization**: Extracted PLANNING_BLUEPRINT to src/core/config.py (DRY principle)
  - Removed duplication from app.py and bootstrap_blueprint.py
  - Single source of truth for configuration
- **Import Structure Update**: All imports now use `src.*` pattern for consistency
- **Cleanup Actions**:
  - Removed obsolete SQLite database (72KB freed)
  - Cleaned attached_assets/ folder
  - Moved utility scripts to scripts/ directory
  - Removed duplicate source files from root
  - Repository size reduced by ~20%
- **Workflow Update**: Fixed PYTHONPATH configuration for new structure
- **Documentation**: Updated README.md to reflect PostgreSQL architecture and new folder structure

### October 10, 2025 - PostgreSQL Migration Complete ✅
- **Successfully migrated from SQLite to PostgreSQL** for permanent data persistence in Replit
- **Critical fix**: SQLite data was being lost when app went to sleep/restarted in Replit environment
- **Database migration**: All tables migrated (sessions, tech_stack, categories, dropdowns, work_items, skills)
- **SQL syntax updates**: Converted all queries from SQLite (`?` placeholders) to PostgreSQL (`%s` placeholders)
- **Connection management**: Implemented PostgreSQL connection pooling using psycopg2-binary
- **Environment integration**: Using Replit's managed PostgreSQL with DATABASE_URL, PGPORT, PGUSER, PGPASSWORD, etc.
- **Verified working**: Tested with sample data - all CRUD operations functioning correctly
- **Data persistence confirmed**: Data now survives app restarts and sleep cycles

## User Preferences
Preferred communication style: Simple, everyday language.

## System Architecture
The application is built around a single Streamlit web interface with a wide layout and multi-page navigation. It follows a modular page design, where each page is a separate Python file, simplifying development and maintenance. The core data management adheres to a database-first approach, utilizing **PostgreSQL** as the primary data store, ensuring all data operations are handled consistently and data persists permanently (migrated from SQLite to prevent data loss in Replit).

### Project Structure
```
smart-tracker/
├── src/                    # All source code
│   ├── core/              # Core application logic
│   │   ├── app.py        # Main Streamlit app
│   │   └── config.py     # Configuration constants
│   ├── database/          # Database layer
│   │   └── operations.py # PostgreSQL operations
│   ├── pages/             # Streamlit pages (8 pages)
│   │   ├── home_dashboard.py
│   │   ├── log_session.py
│   │   ├── dropdown_manager.py
│   │   ├── tech_stack.py
│   │   ├── analytics.py
│   │   ├── sessions.py
│   │   ├── planning.py
│   │   └── calculator.py
│   ├── services/          # Business logic
│   │   ├── sync_service.py
│   │   └── cached_queries.py
│   └── utils/             # Utilities
│       └── dropdowns.py  # Unified dropdown manager
├── scripts/               # Utility scripts
│   ├── bootstrap_blueprint.py
│   └── audit_consistency.py
├── main.py               # Entry point
└── requirements.txt      # Dependencies
```

**Key Architectural Decisions & Design Patterns:**
-   **Modular Page Design**: Each page (`home_dashboard.py`, `log_session.py`, etc.) is a standalone module, making the application scalable and easy to navigate.
-   **Database-First Approach**: All data persistence is handled via PostgreSQL, migrated from SQLite to ensure data integrity, consistency, and permanent persistence in the Replit environment.
-   **Service Layer Architecture**: Business logic is encapsulated in dedicated services, such as `TechnologySyncService` and `CategorySyncService` for atomic data synchronization across tables, and `CachedQueryService` for optimizing read performance.
-   **Direct Table Queries**: Cascading dropdowns read directly from source tables (categories, tech_stack, sessions) instead of using the dropdowns table, eliminating sync issues and ensuring single source of truth.
-   **Performance Patterns**: Includes query batching, aggressive caching with manual invalidation on writes, and deferred saves for form submissions to enhance responsiveness and data consistency.
-   **Hierarchical Data Model**: Employs a 4-level cascading dropdown system (Category → Technology → Work Item → Skill/Topic) for structured data entry and management.
-   **UI/UX**: Features a professional "SYSTEM DEV | Real-Time Operations Dashboard" branding, with sections defaulting to collapsed for a cleaner interface and critical metrics always visible at the top.

**Core Features & Implementations:**
-   **Database Schema**: Comprises `sessions`, `tech_stack`, `categories`, `dropdowns`, `work_items`, and `skills` tables.
-   **Enhanced Session Model**: Sessions include 13 fields with hierarchical categories, work items, and skill topics, supporting tracking of "Studying" and "Practice" session types.
-   **Hybrid Dropdown System**: Work items and skills support both manual pre-definition and auto-population from sessions:
    - `work_items` table stores manually defined work items linked to technologies (TEXT references)
    - `skills` table stores manually defined skills linked to work items (TEXT references)
    - Dropdown queries merge manual entries + auto-populated from sessions, de-duplicated
    - Note: Uses TEXT references instead of integer FKs to maintain consistency with sessions table structure
-   **Simplified Session Entry**: Session entry uses a simplified form where all options are shown without parent-child filtering:
    - Technology dropdown shows ALL technologies (no category selection required)
    - Work Item dropdown shows ALL work items (no technology selection required)
    - Background auto-pairing: Category is automatically looked up from selected technology
    - Relationships preserved for analytics: Data properly grouped by category despite simplified entry
    - Dropdown Manager still uses hierarchical filtering for data management
-   **KPI Dashboard**: Provides real-time metrics including total sessions, hours, technology count, and overall progress.
-   **Analytics Dashboard**: Advanced performance dashboard with hierarchical data breakdowns:
    - Categories Analytics: Time distribution and technology breakdown per category
    - Technologies Analytics: Work item distribution and hours per technology
    - Work Items Analytics: Skill breakdown and session type split per work item
-   **Dropdown Manager**: Consolidated data management hub with 4 tabs:
    - Manage Categories: Add, rename, delete, merge categories
    - Manage Technologies: Add, edit, delete technologies with category assignment
    - Manage Dropdowns: Add work items (linked to technologies) and skills (linked to work items) with proper parent selection
    - Statistics: Overview of all data
-   **Tech Stack Dashboard**: Visual-only dashboard displaying technology cards with KPIs, progress metrics, and category grouping. Read-only interface for viewing learning progress.
-   **Workload Calculator**: A dedicated page for estimating workload with flexible unit conversions.
-   **Data Consistency**: Unified sync services ensure referential integrity and propagate changes across all related tables, eliminating data drift.

## External Dependencies
-   **Streamlit**: For building the interactive web user interface.
-   **Typer**: For developing the command-line interface.
-   **Python 3.11+**: The minimum required Python version.
-   **pip**: For managing project dependencies.
-   **PostgreSQL Database**: The primary data persistence layer using Replit's managed PostgreSQL (Neon-backed), ensuring permanent data persistence. Migrated from SQLite to prevent data loss when app sleeps/restarts.
-   **psycopg2-binary**: PostgreSQL adapter for Python, enabling database connectivity.
-   **pytest**: The testing framework used for development (though tests directory is currently minimal).